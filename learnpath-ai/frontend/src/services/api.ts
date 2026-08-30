import axios from 'axios';
import type { 
  LearnerProfileCreate, LearnerProfileResponse, LearningPathResult,
  AssessmentStartResponse, AssessmentSubmitRequest, AssessmentResult, AssessmentHistoryResponse,
  SkillGapResult,
  DomainInfo,
  MasteryStartResponse, MasterySubmitRequest, MasteryResult, MasteryAttemptHistoryItem,
  CuratedPathResources,
  UserLearningPathsResponse
} from '../types/schemas';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Payload type for learning‑path generation
export interface GeneratePathPayload {
  user_id: string;
  selected_domain: string;
  experience_level: string;
  learning_goal: string;
  career_goal: string;
}

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

import { DEFAULT_DOMAINS } from '../data/domains';

export const domainService = {
  getDomains: async (): Promise<DomainInfo[]> => {
    try {
      const response = await api.get<any>('/domains');
      const data = response.data;
      if (Array.isArray(data) && data.length > 0) {
        return data as DomainInfo[];
      }
      if (data && Array.isArray(data.domains) && data.domains.length > 0) {
        return data.domains as DomainInfo[];
      }
      if (data && typeof data === 'object' && Object.keys(data).length > 0) {
        const values = Object.values(data) as DomainInfo[];
        if (values.length > 0 && values[0].id) {
          return values;
        }
      }
      return DEFAULT_DOMAINS;
    } catch (err) {
      console.warn('Failed to fetch domains from API, using default domain catalogue', err);
      return DEFAULT_DOMAINS;
    }
  }
};

export const profileService = {
  updateProfile: async (userId: string, data: any) => {
    const response = await api.put(`/profiles/${userId}`, data);
    return response.data;
  },
  createProfile: async (profile: LearnerProfileCreate): Promise<LearnerProfileResponse> => {
    const response = await api.post<LearnerProfileResponse>('/profiles', profile);
    return response.data;
  },
  
  getProfile: async (userId: string): Promise<LearnerProfileResponse> => {
    const response = await api.get<LearnerProfileResponse>(`/profiles/${userId}`);
    return response.data;
  }
};

export const assessmentService = {
  start: async (userId: string): Promise<AssessmentStartResponse> => {
    const response = await api.post<AssessmentStartResponse>('/assessments/start', { user_id: userId });
    return response.data;
  },
  
  getAttempt: async (attemptId: string): Promise<AssessmentStartResponse> => {
    const response = await api.get<AssessmentStartResponse>(`/assessments/${attemptId}`);
    return response.data;
  },
  
  submit: async (attemptId: string, submission: AssessmentSubmitRequest): Promise<AssessmentResult> => {
    const response = await api.post<AssessmentResult>(`/assessments/${attemptId}/submit`, submission);
    return response.data;
  },
  
  getResult: async (attemptId: string): Promise<AssessmentResult> => {
    const response = await api.get<AssessmentResult>(`/assessments/${attemptId}/result`);
    return response.data;
  },
  
  getUserHistory: async (userId: string): Promise<AssessmentHistoryResponse> => {
    const response = await api.get<AssessmentHistoryResponse>(`/assessments/user/${userId}`);
    return response.data;
  }
};

export const skillGapService = {
  analyzeSkillGaps: async (userId: string): Promise<SkillGapResult> => {
    const response = await api.post<SkillGapResult>('/skill-gap/analyze', { user_id: userId });
    return response.data;
  },
  
  getLatestAnalysis: async (userId: string): Promise<SkillGapResult> => {
    const response = await api.get<SkillGapResult>(`/skill-gap/user/${userId}`);
    return response.data;
  }
};

export const learningPathService = {
  // Generate a learning path using the full payload
  generatePath: async (payload: GeneratePathPayload): Promise<LearningPathResult> => {
    const response = await api.post<LearningPathResult>('/learning-path/generate', payload);
    return response.data;
  },
  
  getPath: async (pathId: string): Promise<LearningPathResult> => {
    const response = await api.get<LearningPathResult>(`/learning-path/${pathId}`);
    return response.data;
  },

  // Retrieve ALL learning paths belonging to the user
  getUserPaths: async (userId: string): Promise<UserLearningPathsResponse> => {
    const response = await api.get<any>(`/learning-path/user/${userId}`);
    const data = response.data;
    if (data && Array.isArray(data.paths)) {
      return data as UserLearningPathsResponse;
    }
    if (data && data.path_id) {
      const phases = data.phases || [];
      const completed = phases.filter((ph: any) => ph.status === 'completed').length;
      const total = phases.length;
      const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
      return {
        user_id: userId,
        paths: [{
          path_id: data.path_id,
          domain: data.domain,
          title: data.title,
          description: data.description,
          learning_goal: data.learning_goal,
          career_goal: data.career_goal,
          experience_level: data.overall_level || 'intermediate',
          status: completed === total && total > 0 ? 'completed' : 'in_progress',
          progress_percentage: pct,
          completed_phases: completed,
          total_phases: total,
          phases: phases,
          created_at: data.generated_at
        }]
      };
    }
    return { user_id: userId, paths: [] };
  },

  getLatestPath: async (userId: string): Promise<LearningPathResult> => {
    const response = await api.get<any>(`/learning-path/user/${userId}/latest`);
    return response.data;
  }
};

export const resourceService = {
  curateForPath: async (pathId: string): Promise<CuratedPathResources> => {
    const response = await api.post<CuratedPathResources>(`/resources/curate/${pathId}`);
    return response.data;
  },
  
  getPathResources: async (pathId: string): Promise<CuratedPathResources> => {
    const response = await api.get<CuratedPathResources>(`/resources/path/${pathId}`);
    return response.data;
  }
};

export const masteryService = {
  start: async (userId: string, phaseId: string): Promise<MasteryStartResponse> => {
    const response = await api.post<MasteryStartResponse>('/mastery/start', { user_id: userId, phase_id: phaseId });
    return response.data;
  },
  
  submit: async (attemptId: string, submission: MasterySubmitRequest): Promise<MasteryResult> => {
    const response = await api.post<MasteryResult>(`/mastery/${attemptId}/submit`, submission);
    return response.data;
  },
  
  getResult: async (attemptId: string): Promise<MasteryResult> => {
    const response = await api.get<MasteryResult>(`/mastery/${attemptId}/result`);
    return response.data;
  },
  
  getHistory: async (userId: string, phaseId: string): Promise<MasteryAttemptHistoryItem[]> => {
    const response = await api.get<MasteryAttemptHistoryItem[]>(`/mastery/user/${userId}/phase/${phaseId}`);
    return response.data;
  },
  
  completeRemediation: async (attemptId: string): Promise<any> => {
    const response = await api.post(`/mastery/${attemptId}/remediation-complete`);
    return response.data;
  }
};
