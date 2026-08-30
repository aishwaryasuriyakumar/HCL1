import axios from 'axios';
import type { 
  LearnerProfileCreate, LearnerProfileResponse, LearningPathResult,
  AssessmentStartResponse, AssessmentSubmitRequest, AssessmentResult, AssessmentHistoryResponse,
  SkillGapResult,
  DomainInfo,
  MasteryStartResponse, MasterySubmitRequest, MasteryResult, MasteryAttemptHistoryItem,
  CuratedPathResources
} from '../types/schemas';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const domainService = {
  getDomains: async (): Promise<DomainInfo[]> => {
    // The backend may return data in several possible formats:
    // 1. An array of DomainInfo objects.
    // 2. An object with a "domains" key containing the array.
    // 3. A plain dictionary where each key maps to a DomainInfo.
    const response = await api.get<any>('/domains');
    const data = response.data;
    if (Array.isArray(data)) {
      return data as DomainInfo[];
    }
    if (data && Array.isArray(data.domains)) {
      return data.domains as DomainInfo[];
    }
    // Fallback: treat the object as a map of id -> DomainInfo
    return Object.values(data) as DomainInfo[];
  }
};

export const profileService = {
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
  generatePath: async (userId: string): Promise<LearningPathResult> => {
    const response = await api.post<LearningPathResult>('/learning-path/generate', { user_id: userId });
    return response.data;
  },
  
  getPath: async (pathId: string): Promise<LearningPathResult> => {
    const response = await api.get<LearningPathResult>(`/learning-path/${pathId}`);
    return response.data;
  },

  getLatestPath: async (userId: string): Promise<LearningPathResult> => {
    const response = await api.get<LearningPathResult>(`/learning-path/user/${userId}`);
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
