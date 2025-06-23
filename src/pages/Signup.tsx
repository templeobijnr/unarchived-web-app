import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import AuthLayout from '../components/AuthLayout';

const Signup = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Add registration logic here
    navigate('/app');
  };

  return (
    <AuthLayout
      title="Create an account"
      subtitle="Join the future of fashion discovery"
    >
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-white/70 mb-2">
            Full Name
          </label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:border-white/20 transition-colors"
            placeholder="Enter your full name"
            required
          />
        </div>
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-white/70 mb-2">
            Email
          </label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:border-white/20 transition-colors"
            placeholder="Enter your email"
            required
          />
        </div>
        <div>
          <label htmlFor="password" className="block text-sm font-medium text-white/70 mb-2">
            Password
          </label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:border-white/20 transition-colors"
            placeholder="Create a password"
            required
          />
        </div>
        <div className="flex items-center">
          <input
            type="checkbox"
            id="terms"
            className="w-4 h-4 bg-white/5 border border-white/10 rounded"
            required
          />
          <label htmlFor="terms" className="ml-2 text-sm text-white/70">
            I agree to the{' '}
            <Link to="/terms" className="text-white hover:text-white/80 transition-colors">
              Terms of Service
            </Link>{' '}
            and{' '}
            <Link to="/privacy" className="text-white hover:text-white/80 transition-colors">
              Privacy Policy
            </Link>
          </label>
        </div>
        <button
          type="submit"
          className="w-full py-3 bg-white text-black rounded-xl font-medium hover:bg-white/90 transition-colors"
        >
          Create account
        </button>
        <p className="text-center text-white/70">
          Already have an account?{' '}
          <Link to="/login" className="text-white hover:text-white/80 transition-colors">
            Sign in
          </Link>
        </p>
      </form>
    </AuthLayout>
  );
};

export default Signup;