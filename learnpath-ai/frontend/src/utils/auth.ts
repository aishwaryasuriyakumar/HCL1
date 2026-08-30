const USER_ID_KEY = 'learnpath_user_id';

export const auth = {
  getCurrentUserId: (): string | null => {
    return localStorage.getItem(USER_ID_KEY);
  },
  
  setCurrentUserId: (userId: string): void => {
    localStorage.setItem(USER_ID_KEY, userId);
  },
  
  clearUser: (): void => {
    localStorage.removeItem(USER_ID_KEY);
  },
  
  isAuthenticated: (): boolean => {
    return !!localStorage.getItem(USER_ID_KEY);
  }
};
