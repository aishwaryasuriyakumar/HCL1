export interface DomainInfo {
  id: string;
  name: string;
  description?: string;
  skills?: string[];
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

// --- Assessment ---

export interface OptionPublic {
  id: string;
  text: string;
}

export interface QuestionPublic {
  id: string;
  skill: string;
  difficulty: string;
  question: string;
  options: OptionPublic[];
}

export interface AssessmentStartResponse {
  attempt_id: string;
  user_id: string;
  domain: string;
  status: string;
  total_questions: number;
  questions: QuestionPublic[];
  started_at: string;
}

export interface AnswerSubmit {
  question_id: string;
  selected_option_id: string;
}

export interface AssessmentSubmitRequest {
  answers: AnswerSubmit[];
}

export interface SkillResult {
  skill: string;
  questions_attempted: number;
  correct_answers: number;
  score: number;
  proficiency: string;
  confidence: string;
}

export interface OverallResult {
  total_questions: number;
  correct_answers: number;
  incorrect_answers: number;
  score: number;
  proficiency: string;
}

export interface AssessmentResult {
  attempt_id: string;
  user_id: string;
  domain: string;
  status: string;
  overall: OverallResult;
  skill_results: SkillResult[];
  started_at: string;
  submitted_at: string;
}

export interface AssessmentHistoryItem {
  attempt_id: string;
  domain: string;
  status: string;
  score?: number;
  proficiency?: string;
  started_at: string;
  submitted_at?: string;
}
// Response type for user assessment history (array of items)
export type AssessmentHistoryResponse = AssessmentHistoryItem[];
// --- Skill Gap ---

export interface SkillGapItem {
  skill: string;
  current_score: number;
  current_proficiency: string;
  target_score: number;
  gap_score: number;
  severity: string;
  confidence: string;
  priority_score: number;
  priority: string;
  prerequisites: string[];
  reason: string;
}

export interface RecommendedFocusItem {
  order: number;
  skill: string;
  reason: string;
}

export interface SkillGapResult {
  analysis_id: string;
  user_id: string;
  assessment_attempt_id: string;
  domain: string;
  career_goal: string;
  learning_goal: string;
  overall_assessment_score: number;
  overall_proficiency: string;
  skills: SkillGapItem[];
  strong_skills: string[];
  minor_gaps: string[];
  moderate_gaps: string[];
  high_gaps: string[];
  critical_gaps: string[];
  recommended_focus: RecommendedFocusItem[];
  summary: string;
  generated_at: string;
}

// --- Learning Path ---

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

export interface UserPathSummary {
  path_id: string;
  domain: string;
  title: string;
  description: string;
  learning_goal: string;
  career_goal: string;
  experience_level: string;
  status: string;
  progress_percentage: number;
  completed_phases: number;
  total_phases: number;
  phases: PhaseSpec[];
  created_at?: string;
}

export interface UserLearningPathsResponse {
  user_id: string;
  paths: UserPathSummary[];
}

// --- Resources ---

export interface ResourceCardData {
  resource_id: string;
  title: string;
  platform: string;
  description: string;
  resource_type: string;
  difficulty: string;
  is_free: boolean;
  access_type: string;
  duration_minutes?: number;
  rating?: number;
  review_count?: number;
  overall_score: number;
  why_recommended: string;
  original_url: string;
  is_active: boolean;
  last_verified_at: string;
}

export interface PhaseResources {
  phase_id: string;
  resources: ResourceCardData[];
}

export interface CuratedPathResources {
  path_id: string;
  phases: PhaseResources[];
  curated_at: string;
}

// --- Mastery ---

export interface MasteryQuestionOption {
  id: string;
  text: string;
}

export interface MasteryQuestionPublic {
  id: string;
  question_id: string;
  topic: string;
  difficulty: string;
  question: string;
  options: MasteryQuestionOption[];
}

export interface MasteryStartResponse {
  mastery_attempt_id: string;
  user_id: string;
  phase_id: string;
  attempt_number: number;
  total_questions: number;
  questions: MasteryQuestionPublic[];
}

export interface MasteryAnswerSubmission {
  question_id: string;
  selected_option_id: string;
}

// Request payload for submitting mastery answers
export interface MasterySubmitRequest {
  answers: MasteryAnswerSubmission[];
}

export interface MasteryTopicResult {
  topic: string;
  questions_attempted: number;
  correct_answers: number;
  score: number;
  status: string;
}

export interface WeakTopicInfo {
  topic: string;
  score: number;
  reason?: string;
}

export interface MasteryResult {
  mastery_attempt_id: string;
  user_id: string;
  learning_path_id: string;
  phase_id: string;
  phase_title: string;
  score: number;
  pass_threshold: number;
  passed: boolean;
  topic_results: MasteryTopicResult[];
  weak_topics: WeakTopicInfo[];
  next_action: string;
  attempt_number: number;
  submitted_at: string;
  explanation?: string;
}

export interface MasteryAttemptHistoryItem {
  mastery_attempt_id: string;
  attempt_number: number;
  score?: number;
  passed?: boolean;
  weak_topics: string[];
  submitted_at?: string;
}
