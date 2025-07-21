import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const Registration = () => {
  const { register, loading } = useAuth();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    role: 'student', // Default role
    // Additional fields for student registration
    gender: 'other',
    courseId: '1',
  });
  const [courses, setCourses] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [error, setError] = useState('');
  const [fieldErrors, setFieldErrors] = useState({});
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  // Fetch courses and sessions on component mount
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        // Fetch courses
        const coursesResponse = await fetch('http://127.0.0.1:8000/api/courses/');
        const coursesData = await coursesResponse.json();
        setCourses(coursesData);

        // Fetch sessions
        const sessionsResponse = await fetch('http://127.0.0.1:8000/api/sessions/');
        const sessionsData = await sessionsResponse.json();
        setSessions(sessionsData);
      } catch (err) {
        console.error('Failed to fetch initial data:', err);
      }
    };

    fetchInitialData();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    // Clear field error when user types
    if (fieldErrors[name]) {
      setFieldErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setFieldErrors({});

    // Frontend validation
    if (formData.password !== formData.confirmPassword) {
      setFieldErrors({ confirmPassword: 'Passwords do not match' });
      return;
    }

    const result = await register(formData);

    if (result?.success) {
      setSuccess(true);
      setTimeout(() => navigate('/login'), 3000);
    } else {
      if (result?.fieldErrors) {
        setFieldErrors(result.fieldErrors);
      }
      setError(result?.error || 'Registration failed');
    }
  };

  return (
    <div className="max-w-md mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6 text-center">Registration</h1>
      
      {success ? (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
          Registration successful! Redirecting to login page...
        </div>
      ) : (
        <>
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}
          
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Name Field */}
            <div>
              <label className="block text-gray-700 mb-1">Full Name*</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                className={`w-full px-3 py-2 border ${fieldErrors.name ? 'border-red-500' : 'border-gray-300'} rounded-md`}
                required
              />
              {fieldErrors.name && <p className="text-red-500 text-sm mt-1">{fieldErrors.name}</p>}
            </div>

            {/* Email Field */}
            <div>
              <label className="block text-gray-700 mb-1">Email*</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className={`w-full px-3 py-2 border ${fieldErrors.email ? 'border-red-500' : 'border-gray-300'} rounded-md`}
                required
              />
              {fieldErrors.email && <p className="text-red-500 text-sm mt-1">{fieldErrors.email}</p>}
            </div>

            {/* Password Fields */}
            <div>
              <label className="block text-gray-700 mb-1">Password*</label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className={`w-full px-3 py-2 border ${fieldErrors.password ? 'border-red-500' : 'border-gray-300'} rounded-md`}
                required
              />
              {fieldErrors.password && <p className="text-red-500 text-sm mt-1">{fieldErrors.password}</p>}
            </div>

            <div>
              <label className="block text-gray-700 mb-1">Confirm Password*</label>
              <input
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                className={`w-full px-3 py-2 border ${fieldErrors.confirmPassword ? 'border-red-500' : 'border-gray-300'} rounded-md`}
                required
              />
              {fieldErrors.confirmPassword && <p className="text-red-500 text-sm mt-1">{fieldErrors.confirmPassword}</p>}
            </div>

            {/* Role Selection */}
            <div>
              <label className="block text-gray-700 mb-1">Role*</label>
              <select
                name="role"
                value={formData.role}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
              >
                <option value="student">Student</option>
                <option value="staff">Staff</option>
                <option value="hod">HOD</option>
              </select>
            </div>

            {/* Additional fields for students */}
            {formData.role === 'student' && (
              <>
                <div>
                  <label className="block text-gray-700 mb-1">Gender</label>
                  <select
                    name="gender"
                    value={formData.gender}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  >
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                  </select>
                </div>

                <div>
                  <label className="block text-gray-700 mb-1">Course</label>
                  <select
                    name="courseId"
                    value={formData.courseId}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  >
                    {courses.map(course => (
                      <option key={course.id} value={course.id}>{course.course_name}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-gray-700 mb-1">Session Year</label>
                  <select
                    name="sessionYearId"
                    value={formData.sessionYearId}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  >
                    {sessions.map(session => (
                      <option key={session.id} value={session.id}>
                        {session.session_start_year} - {session.session_end_year}
                      </option>
                    ))}
                  </select>
                </div>
              </>
            )}

            <button
              type="submit"
              disabled={loading}
              className={`w-full bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-md ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              {loading ? 'Registering...' : 'Register'}
            </button>
          </form>

          <p className="mt-4 text-center">
            Already have an account?{' '}
            <span
              onClick={() => navigate('/login')}
              className="text-blue-500 hover:text-blue-700 cursor-pointer"
            >
              Login here
            </span>
          </p>
        </>
      )}
    </div>
  );
};

export default Registration;