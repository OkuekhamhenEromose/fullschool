import React from 'react';
import { useAuth } from '../context/AuthContext';

const StaffDashboard = () => {
  const { currentUser, logout } = useAuth();

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Staff Dashboard</h1>
      <p className="text-lg mb-8">Welcome, {currentUser?.name}!</p>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-2">Manage Students</h3>
          <p className="text-gray-600">View and manage student records</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-2">Grade Submission</h3>
          <p className="text-gray-600">Submit and manage student grades</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-2">Attendance</h3>
          <p className="text-gray-600">Record and view student attendance</p>
        </div>
      </div>
      
      <button
        onClick={logout}
        className="bg-red-500 hover:bg-red-600 text-white py-2 px-6 rounded-md"
      >
        Logout
      </button>
    </div>
  );
};

export default StaffDashboard;