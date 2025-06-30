import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import AuthLayout from '../components/AuthLayout';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Add authentication logic here
    navigate('/app');
  };

  return (
    <AuthLayout
      title="Welcome back"
      subtitle="Sign in to your account to continue"
    >
      <form onSubmit={handleSubmit} className="space-y-6">
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
            placeholder="Enter your password"
            required
          />
        </div>
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <input
              type="checkbox"
              id="remember"
              className="w-4 h-4 bg-white/5 border border-white/10 rounded"
            />
            <label htmlFor="remember" className="ml-2 text-sm text-white/70">
              Remember me
            </label>
          </div>
          <Link to="/forgot-password" className="text-sm text-white hover:text-white/80 transition-colors">
            Forgot password?
          </Link>
        </div>
        <button
          type="submit"
          className="w-full py-3 bg-white text-black rounded-xl font-medium hover:bg-white/90 transition-colors"
        >
          Sign in
        </button>
        <p className="text-center text-white/70">
          Don't have an account?{' '}
          <Link to="/signup" className="text-white hover:text-white/80 transition-colors">
            Sign up
          </Link>
        </p>
      </form>
    </AuthLayout>
  );
};

export default Login;