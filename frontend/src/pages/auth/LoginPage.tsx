import { useState } from 'react';
import { motion } from 'framer-motion';
import { Link, useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Separator } from '@/components/ui/separator';
import { useAuth } from '@/contexts/AuthContext';
import { 
  Globe, 
  Mail, 
  Lock, 
  Eye, 
  EyeOff,
  ArrowRight,
  Chrome,
  Github,
  Linkedin
} from 'lucide-react';

const LoginPage = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    rememberMe: false
  });
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      await login(formData.username, formData.password);
      navigate('/app/dashboard');
    } catch (error) {
      console.error('Login failed:', error);
      setError('Invalid username or password. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const socialLogins = [
    { name: 'Google', icon: Chrome, color: 'hover:bg-red-50 hover:border-red-200' },
    { name: 'GitHub', icon: Github, color: 'hover:bg-gray-50 hover:border-gray-200' },
    { name: 'LinkedIn', icon: Linkedin, color: 'hover:bg-blue-50 hover:border-blue-200' }
  ];

  return (
    <div className="min-h-screen bg-gradient-main flex">
      {/* Left Side - Hero */}
      <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-accent-gradient-from/20 to-accent-gradient-to/20" />
        
        <div className="relative z-10 flex flex-col justify-center px-12 text-white">
          <motion.div
            initial={{ opacity: 0, x: -40 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
          >
            <Link to="/" className="flex items-center space-x-3 mb-12">
              <div className="relative">
                <Globe className="h-10 w-10 text-accent-gradient-from" />
                <div className="absolute -inset-1 bg-gradient-accent rounded-full opacity-20 blur" />
              </div>
              <span className="text-2xl font-bold gradient-text">Unarchived</span>
            </Link>

            <h1 className="text-4xl font-bold mb-6">
              Welcome back to the future of sourcing
            </h1>
            <p className="text-xl text-text-secondary mb-8 leading-relaxed">
              Access your AI-powered sourcing dashboard and continue building 
              your global supply chain with confidence.
            </p>

            <div className="space-y-4">
              {[
                'AI-powered supplier matching',
                'Secure escrow payments',
                'Real-time order tracking',
                'Global supplier network'
              ].map((feature, index) => (
                <motion.div
                  key={feature}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.5, delay: 0.2 + index * 0.1 }}
                  className="flex items-center space-x-3"
                >
                  <div className="w-2 h-2 bg-accent-gradient-from rounded-full" />
                  <span className="text-text-primary">{feature}</span>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Floating Elements */}
        <motion.div
          className="absolute top-20 right-20 w-32 h-32 rounded-full bg-gradient-accent opacity-10 blur-xl"
          animate={{ 
            scale: [1, 1.2, 1],
            rotate: [0, 180, 360]
          }}
          transition={{ 
            duration: 20,
            repeat: Infinity,
            ease: "linear"
          }}
        />
        <motion.div
          className="absolute bottom-20 left-20 w-24 h-24 rounded-full bg-accent-gradient-to opacity-10 blur-xl"
          animate={{ 
            scale: [1.2, 1, 1.2],
            rotate: [360, 180, 0]
          }}
          transition={{ 
            duration: 15,
            repeat: Infinity,
            ease: "linear"
          }}
        />
      </div>

      {/* Right Side - Login Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="w-full max-w-md"
        >
          <Card className="glass-effect border-surface-border">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl font-bold text-text-primary">
                Sign In
              </CardTitle>
              <p className="text-text-secondary">
                Enter your credentials to access your account
              </p>
            </CardHeader>

            <CardContent className="space-y-6">
              {/* Social Login */}
              <div className="space-y-3">
                {socialLogins.map((social) => (
                  <Button
                    key={social.name}
                    variant="outline"
                    className={`w-full justify-center ${social.color} transition-colors`}
                  >
                    <social.icon className="w-5 h-5 mr-3" />
                    Continue with {social.name}
                  </Button>
                ))}
              </div>

              <div className="relative">
                <Separator />
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="bg-surface-glass px-3 text-sm text-text-secondary">
                    Or continue with email
                  </span>
                </div>
              </div>

              {/* Email/Password Form */}
              <form onSubmit={handleSubmit} className="space-y-4">
                {error && (
                  <div className="p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-md">
                    {error}
                  </div>
                )}
                
                <div>
                  <label className="block text-sm font-medium text-text-primary mb-2">
                    Username
                  </label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-text-secondary" />
                    <Input
                      type="text"
                      name="username"
                      value={formData.username}
                      onChange={handleChange}
                      placeholder="Enter your username"
                      className="pl-10"
                      required
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-text-primary mb-2">
                    Password
                  </label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-text-secondary" />
                    <Input
                      type={showPassword ? 'text' : 'password'}
                      name="password"
                      value={formData.password}
                      onChange={handleChange}
                      placeholder="Enter your password"
                      className="pl-10 pr-10"
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-1/2 transform -translate-y-1/2 text-text-secondary hover:text-text-primary"
                    >
                      {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                    </button>
                  </div>
                </div>

                <div className="flex items-center justify-between">
                  <label className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      name="rememberMe"
                      checked={formData.rememberMe}
                      onChange={handleChange}
                      className="rounded border-surface-border"
                    />
                    <span className="text-sm text-text-secondary">Remember me</span>
                  </label>
                  <Link 
                    to="/reset-password" 
                    className="text-sm text-accent-gradient-from hover:text-accent-gradient-to transition-colors"
                  >
                    Forgot password?
                  </Link>
                </div>

                <Button type="submit" className="w-full group" disabled={isLoading}>
                  Sign In
                  <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                </Button>
              </form>

              <div className="text-center">
                <span className="text-text-secondary">Don't have an account? </span>
                <Link 
                  to="/signup" 
                  className="text-accent-gradient-from hover:text-accent-gradient-to font-medium transition-colors"
                >
                  Sign up
                </Link>
              </div>
            </CardContent>
          </Card>

          {/* Additional Links */}
          <div className="mt-8 text-center space-y-2">
            <p className="text-sm text-text-secondary">
              By signing in, you agree to our{' '}
              <Link to="/terms" className="text-accent-gradient-from hover:underline">
                Terms of Service
              </Link>{' '}
              and{' '}
              <Link to="/privacy" className="text-accent-gradient-from hover:underline">
                Privacy Policy
              </Link>
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default LoginPage;