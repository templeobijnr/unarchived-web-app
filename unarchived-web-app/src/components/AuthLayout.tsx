import React from 'react';
import { Link } from 'react-router-dom';

interface AuthLayoutProps {
  children: React.ReactNode;
  title: string;
  subtitle: string;
}

const AuthLayout: React.FC<AuthLayoutProps> = ({ children, title, subtitle }) => {
  return (
    <div className="min-h-screen flex">
      {/* Left Side - Form */}
      <div className="w-1/2 flex flex-col justify-center px-20">
        <Link to="/" className="absolute top-8 left-8 flex items-center gap-2">
          <div className="w-10 h-10 bg-gradient-to-br from-white/20 to-white/5 backdrop-blur-lg rounded-xl flex items-center justify-center">
            <span className="text-lg font-bold text-white">UN</span>
          </div>
        </Link>
        <div className="max-w-md w-full mx-auto">
          <h1 className="text-4xl font-bold text-white mb-2">{title}</h1>
          <p className="text-white/70 mb-8">{subtitle}</p>
          {children}
        </div>
      </div>

      {/* Right Side - Image */}
      <div className="w-1/2 relative">
        <div className="absolute inset-0 bg-gradient-to-br from-black/50 to-black mix-blend-multiply" />
        <img
          src="https://images.unsplash.com/photo-1509631179647-0177331693ae?auto=format&fit=crop&w=1200&q=80"
          alt="Fashion"
          className="absolute inset-0 w-full h-full object-cover"
        />
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="max-w-lg text-center">
            <h2 className="text-5xl font-bold text-white mb-6">Join the Future of Fashion</h2>
            <p className="text-xl text-white/80">
              Connect with emerging brands, discover exclusive drops, and be part of the next generation of fashion culture.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthLayout;