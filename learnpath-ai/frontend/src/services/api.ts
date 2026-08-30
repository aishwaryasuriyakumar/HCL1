import axios from 'axios';
import type { LearnerProfileCreate, LearnerProfileResponse, LearningPathResult } from '../types/schemas';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

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

export const skillGapService = {
  analyzeSkillGaps: async (userId: string): Promise<any> => {
    const response = await api.post('/skill-gap/analyze', { user_id: userId });
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
