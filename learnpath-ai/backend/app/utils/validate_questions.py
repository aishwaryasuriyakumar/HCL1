import os
import json
from app.data.domains import DOMAINS

def validate_question_bank(questions_dir):
    expected_files = [
        "machine_learning.json",
        "data_science.json",
        "generative_ai.json",
        "web_development.json",
        "cloud_devops.json"
    ]
    
    # 1. Verify files exist
    for f in expected_files:
        path = os.path.join(questions_dir, f)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing expected question bank file: {f}")
            
    all_questions = []
    domain_counts = {}
    globally_unique_ids = set()
    
    # Load and pool all questions
    for f in expected_files:
        path = os.path.join(questions_dir, f)
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            domain_id = f.replace(".json", "")
            domain_counts[domain_id] = len(data)
            all_questions.extend(data)
            
    # 2. Check total question count
    if len(all_questions) != 150:
        raise ValueError(f"Expected exactly 150 questions total, found {len(all_questions)}")
        
    # 3. Check question count per domain
    for domain_id, count in domain_counts.items():
        if count != 30:
            raise ValueError(f"Expected exactly 30 questions for domain '{domain_id}', found {count}")
            
    # 4. Detailed validation of each question
    for idx, q in enumerate(all_questions):
        q_id = q.get("id")
        domain = q.get("domain")
        skill = q.get("skill")
        difficulty = q.get("difficulty")
        question_text = q.get("question")
        options = q.get("options")
        correct_option_id = q.get("correct_option_id")
        explanation = q.get("explanation")
        weight = q.get("weight")
        
        # Check required fields
        if not q_id or not isinstance(q_id, str):
            raise ValueError(f"Invalid or missing 'id' at index {idx}")
        if not domain or not isinstance(domain, str):
            raise ValueError(f"Invalid or missing 'domain' in question '{q_id}'")
        if not skill or not isinstance(skill, str):
            raise ValueError(f"Invalid or missing 'skill' in question '{q_id}'")
        if difficulty not in ["easy", "medium", "hard"]:
            raise ValueError(f"Invalid 'difficulty' in question '{q_id}': {difficulty}")
        if not question_text or not isinstance(question_text, str):
            raise ValueError(f"Invalid or missing 'question' text in question '{q_id}'")
        if not explanation or not isinstance(explanation, str):
            raise ValueError(f"Invalid or missing 'explanation' in question '{q_id}'")
        if not isinstance(weight, (int, float)) or weight <= 0:
            raise ValueError(f"Invalid 'weight' in question '{q_id}': {weight}")
            
        # Global uniqueness of IDs
        if q_id in globally_unique_ids:
            raise ValueError(f"Duplicate question ID found: '{q_id}'")
        globally_unique_ids.add(q_id)
        
        # Validate domain exists in main configuration
        if domain not in DOMAINS:
            raise ValueError(f"Domain '{domain}' in question '{q_id}' is not in central domains.py configuration")
            
        # Validate skill exists in that domain
        allowed_skills = DOMAINS[domain]["skills"]
        if skill not in allowed_skills:
            raise ValueError(f"Skill '{skill}' in question '{q_id}' is not a valid skill for domain '{domain}'")
            
        # Validate options
        if not isinstance(options, list) or len(options) != 4:
            raise ValueError(f"Expected exactly 4 options in question '{q_id}'")
            
        option_ids = []
        for opt in options:
            opt_id = opt.get("id")
            opt_text = opt.get("text")
            if not opt_id or not isinstance(opt_id, str):
                raise ValueError(f"Invalid 'id' in option for question '{q_id}'")
            if not opt_text or not isinstance(opt_text, str):
                raise ValueError(f"Invalid 'text' in option for question '{q_id}'")
            option_ids.append(opt_id)
            
        # Option ID uniqueness within question
        if len(set(option_ids)) != 4:
            raise ValueError(f"Option IDs are not unique in question '{q_id}': {option_ids}")
            
        # Correct option must exist
        if correct_option_id not in option_ids:
            raise ValueError(f"correct_option_id '{correct_option_id}' does not match any option IDs in question '{q_id}': {option_ids}")
            
    # 5. Skill-level distributions per domain
    for domain_id, domain_info in DOMAINS.items():
        domain_skills = domain_info["skills"]
        domain_qs = [q for q in all_questions if q["domain"] == domain_id]
        
        # Verify 10 skills per domain represented
        represented_skills = set(q["skill"] for q in domain_qs)
        if len(represented_skills) != 10:
            raise ValueError(f"Domain '{domain_id}' does not represent exactly 10 skills. Found: {list(represented_skills)}")
            
        for s in domain_skills:
            skill_qs = [q for q in domain_qs if q["skill"] == s]
            if len(skill_qs) != 3:
                raise ValueError(f"Skill '{s}' in domain '{domain_id}' must have exactly 3 questions. Found: {len(skill_qs)}")
                
            # Check difficulty distribution (1 easy, 1 medium, 1 hard)
            diffs = [q["difficulty"] for q in skill_qs]
            if sorted(diffs) != ["easy", "hard", "medium"]:
                raise ValueError(f"Skill '{s}' in domain '{domain_id}' does not have exactly 1 easy, 1 medium, 1 hard. Found: {diffs}")
                
    print("Question bank validation successful! All rules satisfied.")
    return True

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    questions_path = os.path.join(base_dir, 'data', 'questions')
    validate_question_bank(questions_path)
