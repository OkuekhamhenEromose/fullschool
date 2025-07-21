import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import Contact from './pages/Contact';
import Login from './pages/Login';
import Registration from './pages/Registration';
import StudentDashboard from './pages/StudentDashboard';
import StaffDashboard from './pages/StaffDashboard';
import PrivateRoute from './components/PrivateRoute';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="contact" element={<Contact />} />
          <Route path="login" element={<Login />} />
          <Route path="registration" element={<Registration />} />
          <Route path="student" element={<PrivateRoute><StudentDashboard /></PrivateRoute>} />
          <Route path="staff" element={<PrivateRoute><StaffDashboard /></PrivateRoute>} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;