import { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(false);

  const register = async (userData) => {
    setLoading(true);
    try {
      // Determine user type based on role selection
      let userType;
      switch(userData.role) {
        case 'staff':
          userType = 2; // STAFF
          break;
        case 'hod':
          userType = 1; // HOD
          break;
        default:
          userType = 3; // STUDENT
      }

      // Prepare data matching Django model requirements
      const registrationData = {
        username: userData.email.split('@')[0], // Generate username from email
        email: userData.email,
        first_name: userData.name.split(' ')[0],
        last_name: userData.name.split(' ').slice(1).join(' ') || '',
        password: userData.password,
        confirm_password: userData.confirmPassword,
        user_type: userType,
        // Additional fields for student profile if needed
        ...(userType === 3 && {
          gender: 'other', // Default value
          address: '', // Empty by default
          course_id: 1, // Default course
          session_year_id: 1 // Default session
        })
      };

      const response = await fetch('http://127.0.0.1:8000/api/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || 'Registration failed');
      }
      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      console.error('Registration error:', error);
      return { 
        success: false, 
        error: error.message,
      };
    } finally {
      setLoading(false);
    }
  };

  const value = {
    currentUser,
    loading,
    register,
    // login and logout would be implemented similarly
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}