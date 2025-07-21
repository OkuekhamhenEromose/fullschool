// context/AuthContext.js
import { createContext, useContext } from 'react';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  // Your auth state and methods here
  const value = {
    currentUser: null, // or your actual user state
    login: async () => {}, // your login function
    logout: async () => {}, // your logout function
    register: async () => {}, // your register function
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}