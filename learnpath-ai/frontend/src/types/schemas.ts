export interface DomainInfo {
  id: string;
  name: string;
}

export type ExperienceLevel = 'beginner' | 'intermediate' | 'advanced' | 'professional';
export type YearsOfExperience = 'none' | 'less_than_1' | '1_2' | '3_5' | '5_plus';
export type CourseStatus = 'completed' | 'in_progress';
export type LearningFormat = 'video' | 'reading' | 'hands_on' | 'interactive' | 'mixed';
export type DailyLearningTime = '15_30_min' | '30_60_min' | '1_2_hours' | '2_plus_hours';

export interface ProjectInput {
  name: string;
  description?: string;
  technologies: string[];
  url?: string;
}

export interface CertificationInput {
  name: string;
  issuing_organization: string;
  year?: number;
}

export interface CompletedCourseInput {
  name: string;
  platform: string;
  status: CourseStatus;
}

export interface LearnerProfileCreate {
  full_name: string;
  email: string;
  selected_domain: string;
  experience_level: ExperienceLevel;
  years_of_experience?: YearsOfExperience;
  learning_goal: string;
  career_goal: string;
  motivation?: string;
  current_skills?: string[];
  interests?: string[];
  projects?: ProjectInput[];
  certifications?: CertificationInput[];
  completed_courses?: CompletedCourseInput[];
  preferred_learning_formats?: LearningFormat[];
  daily_learning_time?: DailyLearningTime;
}

export interface LearnerProfileResponse extends Omit<LearnerProfileCreate, 'selected_domain'> {
  user_id: string;
  selected_domain: DomainInfo;
  created_at: string;
  updated_at: string;
}

export interface ProjectSpec {
  title: string;
  description: string;
  deliverable: string;
  estimated_hours: number;
}

export interface CompletionCriteria {
  assessment_required: boolean;
  mastery_threshold: number;
}

export interface PhaseSpec {
  phase_id: string;
  order: number;
  title: string;
  description: string;
  skills: string[];
  prerequisite_phase_ids: string[];
  learning_objectives: string[];
  learning_outcomes: string[];
  resource_topics: string[];
  project: ProjectSpec;
  estimated_hours: number;
  difficulty: string;
  recommendation_reason: string;
  completion_criteria: CompletionCriteria;
  status: string;
}

export interface CapstoneProject {
  title: string;
  description: string;
  deliverables: string[];
  estimated_hours: number;
}

export interface LearningPathResult {
  path_id: string;
  user_id: string;
  skill_gap_analysis_id: string;
  domain: string;
  title: string;
  description: string;
  learning_goal: string;
  career_goal: string;
  overall_level: string;
  total_phases: number;
  estimated_total_hours: number;
  phases: PhaseSpec[];
  capstone_project: CapstoneProject;
  generated_at: string;
}
