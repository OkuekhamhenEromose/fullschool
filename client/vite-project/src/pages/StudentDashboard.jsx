import React from 'react';
import { useAuth } from '../context/AuthContext';

const StudentDashboard = () => {
  const { currentUser, logout } = useAuth();

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Student Dashboard</h1>
      <p className="text-lg mb-8">Welcome, {currentUser?.name}!</p>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-2">My Courses</h3>
          <p className="text-gray-600">View and manage your enrolled courses</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-2">Grades</h3>
          <p className="text-gray-600">Check your academic performance</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-2">Schedule</h3>
          <p className="text-gray-600">View your class timetable</p>
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

export default StudentDashboard;