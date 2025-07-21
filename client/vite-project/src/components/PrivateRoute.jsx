import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const PrivateRoute = ({ children }) => {
  const { currentUser } = useAuth();
  
  if (!currentUser) {
    return <Navigate to="/login" replace />;
  }

  // Check user role and redirect accordingly
  if (currentUser.role === 'student' && window.location.pathname !== '/student') {
    return <Navigate to="/student" replace />;
  }

  if (currentUser.role === 'staff' && window.location.pathname !== '/staff') {
    return <Navigate to="/staff" replace />;
  }

  return children;
};

export default PrivateRoute;