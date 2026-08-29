import pytest
from app.services.question_bank_service import question_bank_service
from app.data.domains import DOMAINS

def test_question_bank_loading():
    # Verify we loaded 150 questions total and 30 per domain
    assert len(question_bank_service._questions_by_id) == 150
    for domain_id in DOMAINS.keys():
        qs = question_bank_service.get_questions_by_domain(domain_id)
        assert len(qs) == 30

def test_balanced_selection_distributions():
    # Test the selection algorithm multiple times for each domain to ensure no statistical crashes
    for domain_id in DOMAINS.keys():
        domain_info = DOMAINS[domain_id]
        expected_skills = set(domain_info["skills"])
        
        for run in range(20):  # Run 20 times per domain
            selection = question_bank_service.select_balanced_questions(domain_id)
            
            # 1. Exactly 15 questions
            assert len(selection) == 15
            
            # 2. Unique question IDs
            ids = [q["id"] for q in selection]
            assert len(set(ids)) == 15
            
            # 3. Correct difficulty distribution: 5 easy, 6 medium, 4 hard
            diffs = [q["difficulty"] for q in selection]
            assert diffs.count("easy") == 5
            assert diffs.count("medium") == 6
            assert diffs.count("hard") == 4
            
            # 4. Covers all 10 skills
            skills = [q["skill"] for q in selection]
            assert set(skills) == expected_skills
            
            # 5. All questions belong to the selected domain
            for q in selection:
                assert q["domain"] == domain_id

def test_get_question_by_id():
    # Fetch a known question and verify structure
    known_id = "ml_python_001"
    q = question_bank_service.get_question(known_id)
    assert q is not None
    assert q["id"] == known_id
    assert q["domain"] == "machine_learning"
    assert q["skill"] == "Python for ML"
    assert q["difficulty"] == "easy"
    assert len(q["options"]) == 4

def test_get_question_invalid_id():
    assert question_bank_service.get_question("invalid_id") is None
