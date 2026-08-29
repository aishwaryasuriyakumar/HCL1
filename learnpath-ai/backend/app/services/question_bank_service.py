import os
import json
import random
from typing import Dict, List, Optional
from app.data.domains import DOMAINS

class QuestionBankService:
    def __init__(self):
        self._questions_by_domain: Dict[str, List[dict]] = {}
        self._questions_by_id: Dict[str, dict] = {}
        self.load_question_bank()

    def load_question_bank(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        questions_dir = os.path.join(base_dir, 'data', 'questions')
        
        expected_files = [
            "machine_learning.json",
            "data_science.json",
            "generative_ai.json",
            "web_development.json",
            "cloud_devops.json"
        ]
        
        for f in expected_files:
            domain_id = f.replace(".json", "")
            path = os.path.join(questions_dir, f)
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as file:
                    questions = json.load(file)
                    self._questions_by_domain[domain_id] = questions
                    for q in questions:
                        self._questions_by_id[q["id"]] = q
            else:
                # Fallback if file doesn't exist yet (should exist after setup)
                self._questions_by_domain[domain_id] = []

    def get_question(self, question_id: str) -> Optional[dict]:
        return self._questions_by_id.get(question_id)

    def get_questions_by_domain(self, domain_id: str) -> List[dict]:
        return self._questions_by_domain.get(domain_id, [])

    def select_balanced_questions(self, domain_id: str) -> List[dict]:
        domain_questions = self.get_questions_by_domain(domain_id)
        if not domain_questions:
            raise ValueError(f"No questions found for domain '{domain_id}'")

        domain_info = DOMAINS.get(domain_id)
        if not domain_info:
            raise ValueError(f"Domain '{domain_id}' not found in domains configuration")
            
        skills = list(domain_info["skills"])  # 10 skills
        
        # We need to pick:
        # - Exactly 15 questions
        # - Covering all 10 skills
        # - Difficulty distribution: 5 Easy, 6 Medium, 4 Hard
        
        # Loop until a valid set is found (to handle any rare selection lock)
        for _ in range(100):
            selected_qs = []
            selected_ids = set()
            skill_usage = {s: 0 for s in skills}
            
            # Step 1: Distribute 10 initial questions, one for each skill
            # Step 1 target difficulties: 3 Easy, 4 Medium, 3 Hard
            step1_diffs = ["easy"] * 3 + ["medium"] * 4 + ["hard"] * 3
            random.shuffle(step1_diffs)
            
            shuffled_skills = list(skills)
            random.shuffle(shuffled_skills)
            
            step1_success = True
            for i, skill in enumerate(shuffled_skills):
                target_diff = step1_diffs[i]
                # Find the question for this skill and difficulty
                candidate = next(
                    (q for q in domain_questions if q["skill"] == skill and q["difficulty"] == target_diff),
                    None
                )
                if not candidate:
                    step1_success = False
                    break
                selected_qs.append(candidate)
                selected_ids.add(candidate["id"])
                skill_usage[skill] += 1
                
            if not step1_success:
                continue
                
            # Step 2: Select 5 extra questions from 5 distinct skills to complete difficulty targets
            # We need 2 more Easy, 2 more Medium, 1 more Hard
            extra_diffs = ["easy", "easy", "medium", "medium", "hard"]
            random.shuffle(extra_diffs)
            
            step2_success = True
            used_extra_skills = set()
            
            for target_diff in extra_diffs:
                # Find a skill that has not been selected for extra questions,
                # and has a question of target_diff that wasn't already picked
                found = False
                # Try picking from skills that didn't get this target_diff in Step 1
                candidate_skills = [s for s in skills if s not in used_extra_skills]
                random.shuffle(candidate_skills)
                
                for skill in candidate_skills:
                    candidate = next(
                        (q for q in domain_questions 
                         if q["skill"] == skill 
                         and q["difficulty"] == target_diff 
                         and q["id"] not in selected_ids),
                        None
                    )
                    if candidate:
                        selected_qs.append(candidate)
                        selected_ids.add(candidate["id"])
                        skill_usage[skill] += 1
                        used_extra_skills.add(skill)
                        found = True
                        break
                if not found:
                    step2_success = False
                    break
                    
            if not step2_success:
                continue
                
            # Final validation check
            diff_counts = {"easy": 0, "medium": 0, "hard": 0}
            for q in selected_qs:
                diff_counts[q["difficulty"]] += 1
                
            if (len(selected_qs) == 15 
                    and diff_counts["easy"] == 5 
                    and diff_counts["medium"] == 6 
                    and diff_counts["hard"] == 4 
                    and all(count >= 1 for count in skill_usage.values())):
                # Shuffle the final 15 questions before returning
                random.shuffle(selected_qs)
                return selected_qs
                
        raise ValueError("Failed to generate a balanced question selection after multiple attempts.")

    @staticmethod
    def serialize_public_question(q: dict) -> dict:
        return {
            "id": q["id"],
            "skill": q["skill"],
            "difficulty": q["difficulty"],
            "question": q["question"],
            "options": q["options"]
        }

question_bank_service = QuestionBankService()
