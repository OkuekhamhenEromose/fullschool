import React from 'react';
import Navbar from './Navbar';
import { Outlet } from 'react-router-dom';

const Layout = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow p-8">
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;