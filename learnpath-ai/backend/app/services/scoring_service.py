class ScoringService:
    @staticmethod
    def calculate_percentage(correct: int, total: int) -> float:
        if total <= 0:
            return 0.0
        return round((correct / total) * 100.0, 2)

    @staticmethod
    def classify_proficiency(score: float) -> str:
        if score >= 90.00:
            return "Expert"
        elif score >= 75.00:
            return "Advanced"
        elif score >= 60.00:
            return "Intermediate"
        elif score >= 40.00:
            return "Beginner"
        else:
            return "Novice"

    @staticmethod
    def calculate_confidence(questions_count: int) -> str:
        if questions_count <= 1:
            return "low"
        elif questions_count == 2:
            return "medium"
        else:
            return "high"

scoring_service = ScoringService()
