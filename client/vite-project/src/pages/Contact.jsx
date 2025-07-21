import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

const Contact = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: '',
  });
  const [submitted, setSubmitted] = useState(false);
  const { currentUser } = useAuth();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          userId: currentUser?.id || null,
        }),
      });

      if (response.ok) {
        setSubmitted(true);
        setFormData({ name: '', email: '', message: '' });
      }
    } catch (error) {
      console.error('Submission failed:', error);
    }
  };

  return (
    <div className="max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-6">Contact Us</h1>
      {submitted ? (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
          Thank you for your message! We'll get back to you soon.
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-gray-700 mb-1">Name</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              required
            />
          </div>
          <div>
            <label className="block text-gray-700 mb-1">Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              required
            />
          </div>
          <div>
            <label className="block text-gray-700 mb-1">Message</label>
            <textarea
              name="message"
              value={formData.message}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              rows="4"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-md"
          >
            Send Message
          </button>
        </form>
      )}
    </div>
  );
};

export default Contact;