import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-gray-800 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <div className="text-xl font-bold">
          <Link to="/" className="hover:text-gray-300">School Management System</Link>
        </div>
        <div className="space-x-4">
          <Link to="/" className="hover:text-gray-300">Home</Link>
          <Link to="/contact" className="hover:text-gray-300">Contact</Link>
          <Link to="/login" className="hover:text-gray-300">Login</Link>
          <Link to="/registration" className="hover:text-gray-300">Registration</Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;