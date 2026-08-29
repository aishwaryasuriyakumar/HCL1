import json
import time
import logging
from typing import Type, TypeVar, Optional, Any
from pydantic import BaseModel, ValidationError
from google import genai
from google.genai import types

from app.core.config import settings

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

class LLMService:
    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or settings.effective_gemini_api_key
        self.model_name = model_name or settings.effective_gemini_model
        self._client: Optional[genai.Client] = None

    @property
    def client(self) -> genai.Client:
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY / LLM_API_KEY is not configured.")
        if self._client is None:
            self._client = genai.Client(api_key=self.api_key)
        return self._client

    def _call_gemini_with_retry(self, prompt: str, config: types.GenerateContentConfig, max_retries: int = 3) -> str:
        models_to_try = [self.model_name]
        if "gemini-3.6-flash" not in models_to_try:
            models_to_try.append("gemini-3.6-flash")

        last_exception = None

        for model in models_to_try:
            for attempt in range(1, max_retries + 1):
                try:
                    logger.info(f"Invoking Gemini model={model} attempt={attempt}")
                    response = self.client.models.generate_content(
                        model=model,
                        contents=prompt,
                        config=config,
                    )
                    return response.text
                except Exception as e:
                    last_exception = e
                    err_msg = str(e)
                    if "503" in err_msg or "UNAVAILABLE" in err_msg or "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                        logger.warning(f"Transient error from Gemini model={model} attempt={attempt}: {err_msg}. Retrying in {attempt * 2}s...")
                        time.sleep(attempt * 2)
                    else:
                        logger.error(f"Permanent error from Gemini model={model}: {e}")
                        break

        raise RuntimeError(f"Gemini API request failed after retries across models: {last_exception}")

    def generate_structured(
        self,
        prompt: str,
        system_instruction: str,
        response_model: Type[T],
    ) -> T:
        """
        Generates structured JSON output from Gemini and validates it against the Pydantic model.
        Performs 1 safe repair attempt if validation fails.
        """
        logger.info(f"llm_generation_started model={self.model_name}")
        
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            temperature=0.2,
        )

        raw_text = self._call_gemini_with_retry(prompt, config)
        logger.info("llm_generation_completed received raw text response")

        # Try parsing JSON & validating model
        parsed_obj, validation_error = self._parse_and_validate(raw_text, response_model)
        if parsed_obj is not None:
            logger.info("llm_validation_completed successfully parsed and validated structured response")
            return parsed_obj

        # 1 safe repair attempt
        logger.warning(f"Initial LLM response validation failed: {validation_error}. Attempting 1 repair retry.")
        repair_prompt = (
            f"The previous response failed schema validation:\n"
            f"Validation Error: {validation_error}\n\n"
            f"Original Input Prompt:\n{prompt}\n\n"
            f"Raw Response to Repair:\n{raw_text}\n\n"
            f"Please output strictly valid JSON matching the required schema."
        )

        try:
            repair_text = self._call_gemini_with_retry(repair_prompt, config)
            repaired_obj, repair_error = self._parse_and_validate(repair_text, response_model)
            if repaired_obj is not None:
                logger.info("llm_validation_completed repaired response successfully validated")
                return repaired_obj
            else:
                logger.error(f"Repair attempt failed: {repair_error}")
                raise ValueError(f"LLM output validation failed after repair retry: {repair_error}")
        except Exception as e:
            logger.error(f"LLM repair attempt exception: {e}")
            raise ValueError(f"LLM structured output validation failed: {e}")

    def _normalize_json_data(self, data: Any) -> Any:
        if isinstance(data, dict):
            # Normalize phases key aliases
            if "phases" not in data or not isinstance(data["phases"], list):
                for alt_key in ["learning_path", "roadmap", "modules", "learning_phases", "phases_list"]:
                    if alt_key in data and isinstance(data[alt_key], list):
                        data["phases"] = data[alt_key]
                        break

            # Normalize capstone key aliases
            if "capstone_project" not in data or not isinstance(data["capstone_project"], dict):
                for alt_cap in ["capstone", "final_project", "capstone_project_spec"]:
                    if alt_cap in data and isinstance(data[alt_cap], dict):
                        data["capstone_project"] = data[alt_cap]
                        break

            # Normalize capstone deliverables
            if "capstone_project" in data and isinstance(data["capstone_project"], dict):
                cap = data["capstone_project"]
                if "deliverable" in cap and "deliverables" not in cap:
                    cap["deliverables"] = [cap["deliverable"]] if isinstance(cap["deliverable"], str) else cap["deliverable"]

            # Normalize phases
            if "phases" in data and isinstance(data["phases"], list):
                for idx, p in enumerate(data["phases"], start=1):
                    if isinstance(p, dict):
                        if "phase_number" in p and "order" not in p:
                            p["order"] = p["phase_number"]
                        if "phase_id" not in p:
                            p["phase_id"] = f"phase_{idx:02d}"
                        if "target_skills" in p and "skills" not in p:
                            p["skills"] = p["target_skills"]
                        if "topics" in p and "resource_topics" not in p:
                            p["resource_topics"] = p["topics"]
                        elif "resources" in p and "resource_topics" not in p:
                            p["resource_topics"] = p["resources"]
                        
                        if "objectives" in p and "learning_objectives" not in p:
                            p["learning_objectives"] = p["objectives"]
                        elif "goals" in p and "learning_objectives" not in p:
                            p["learning_objectives"] = p["goals"]

                        if "outcomes" in p and "learning_outcomes" not in p:
                            p["learning_outcomes"] = p["outcomes"]

                        # If project is returned as a plain string by LLM
                        if "project" in p and isinstance(p["project"], str):
                            p["project"] = {
                                "title": "Practical Phase Project",
                                "description": p["project"],
                                "deliverable": "Source code and project documentation",
                                "estimated_hours": 4.0
                            }
            return data
        return data

    def _parse_and_validate(self, text: str, response_model: Type[T]) -> tuple[Optional[T], Optional[str]]:
        if not text:
            return None, "Empty text response from LLM"
        
        # Clean markdown backticks if present
        clean_text = text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.startswith("```"):
            clean_text = clean_text[3:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
        clean_text = clean_text.strip()

        try:
            json_data = json.loads(clean_text)
            normalized_data = self._normalize_json_data(json_data)
            validated = response_model.model_validate(normalized_data)
            return validated, None
        except json.JSONDecodeError as e:
            return None, f"JSONDecodeError: {e}"
        except ValidationError as e:
            return None, f"ValidationError: {e}"
        except Exception as e:
            return None, f"ParsingException: {e}"

llm_service = LLMService()

