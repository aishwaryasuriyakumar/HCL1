export interface LearnerProfile {
  user_id: string;
  full_name: string;
  email: string;
  selected_domain: string;
  experience_level: string;
  career_goal: string;
  learning_goal: string;
  motivation: string;
  current_skills: string[];
  interests: string[];
  projects: string[];
  certifications: string[];
  completed_courses: string[];
  preferred_learning_formats: string[];
  daily_learning_time?: number;
}

export interface AssessmentResult {
  attempt_id: string;
  user_id: string;
  domain: string;
  overall: {
    total_questions: number;
    correct_answers: number;
    score: number;
    proficiency: string;
  };
  skill_results: Array<{
    skill: string;
    questions_attempted: number;
    correct_answers: number;
    score: number;
    proficiency: string;
    confidence: string;
  }>;
}

export interface SkillGapResult {
  user_id: string;
  domain: string;
  career_goal: string;
  overall_score: number;
  skills: Array<{
    skill: string;
    score: number;
    proficiency: string;
    confidence: string;
    status: string;
  }>;
  strong_skills: string[];
  moderate_skills: string[];
  skill_gaps: string[];
  critical_gaps: string[];
  recommended_focus: string[];
  summary: string;
}

export interface LearningPathResult {
  user_id: string;
  domain: string;
  goal: string;
  phases: Array<{
    phase_id: string;
    order: number;
    title: string;
    description: string;
    skills: string[];
    prerequisites: string[];
    estimated_hours: number;
    status: string;
  }>;
}

export interface RecommendedResource {
  resource_id: string;
  phase_id: string;
  title: string;
  provider: string;
  url: string;
  resource_type: string;
  is_free: boolean;
  availability_status: string;
  relevance_score: number;
  quality_score: number;
  why_recommended: string;
  learning_outcome: string;
}

export interface MasteryResult {
  user_id: string;
  phase_id: string;
  score: number;
  passed: boolean;
  weak_topics: string[];
  next_action: string;
}

export interface ProgressSummary {
  user_id: string;
  overall_progress: number;
  completed_phases: number;
  total_phases: number;
  current_phase_id: string;
  average_score: number;
  completed_modules: string[];
  remaining_modules: string[];
  learning_speed: string;
}
