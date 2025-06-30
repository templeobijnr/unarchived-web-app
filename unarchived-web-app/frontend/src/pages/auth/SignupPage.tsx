import { useState } from 'react';
import { motion } from 'framer-motion';
import { Link, useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Separator } from '@/components/ui/separator';
import { Badge } from '@/components/ui/badge';
import { authApi } from '@/lib/api';
import { 
  Globe, 
  Mail, 
  Lock, 
  Eye, 
  EyeOff,
  ArrowRight,
  Chrome,
  Github,
  Linkedin,
  User,
  Building,
  Check,
  Zap
} from 'lucide-react';

const SignupPage = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    agreeToTerms: false
  });
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (!formData.agreeToTerms) {
      setError('Please agree to the terms and conditions');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      // Register the user
      await authApi.register(formData.username, formData.email, formData.password);
      
      // Auto-login after successful registration
      await authApi.login(formData.username, formData.password);
      
      navigate('/app/dashboard');
    } catch (error: any) {
      console.error('Signup failed:', error);
      setError(error.message || 'Failed to create account. Please try again.');
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

  const benefits = [
    'AI-powered supplier matching',
    'Secure milestone-based payments',
    'Global supplier network access',
    'Real-time order tracking',
    '24/7 customer support',
    'Advanced analytics dashboard'
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

            <Badge className="mb-6 bg-gradient-accent text-white px-4 py-2 w-fit">
              <Zap className="w-4 h-4 mr-2" />
              Start Your Free Trial
            </Badge>

            <h1 className="text-4xl font-bold mb-6">
              Transform your sourcing with AI
            </h1>
            <p className="text-xl text-text-secondary mb-8 leading-relaxed">
              Join thousands of companies already saving time and money with 
              intelligent global sourcing. Get started in minutes.
            </p>

            <div className="space-y-4">
              {benefits.map((benefit, index) => (
                <motion.div
                  key={benefit}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.5, delay: 0.2 + index * 0.1 }}
                  className="flex items-center space-x-3"
                >
                  <div className="w-6 h-6 rounded-full bg-gradient-accent flex items-center justify-center">
                    <Check className="w-4 h-4 text-white" />
                  </div>
                  <span className="text-text-primary">{benefit}</span>
                </motion.div>
              ))}
            </div>

            <div className="mt-8 p-6 glass-effect rounded-lg border border-surface-border">
              <p className="text-sm text-text-secondary mb-2">Free Trial Includes:</p>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>• 5 RFQs included</div>
                <div>• 20 supplier connections</div>
                <div>• Full platform access</div>
                <div>• No credit card required</div>
              </div>
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

      {/* Right Side - Signup Form */}
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
                Create Account
              </CardTitle>
              <p className="text-text-secondary">
                Start your free trial today - no credit card required
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
                    Or create with email
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
                    <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-text-secondary" />
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
                    Email Address
                  </label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-text-secondary" />
                    <Input
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      placeholder="john@company.com"
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
                      placeholder="Create a strong password"
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

                <div>
                  <label className="block text-sm font-medium text-text-primary mb-2">
                    Confirm Password
                  </label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-text-secondary" />
                    <Input
                      type={showConfirmPassword ? 'text' : 'password'}
                      name="confirmPassword"
                      value={formData.confirmPassword}
                      onChange={handleChange}
                      placeholder="Confirm your password"
                      className="pl-10 pr-10"
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                      className="absolute right-3 top-1/2 transform -translate-y-1/2 text-text-secondary hover:text-text-primary"
                    >
                      {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                    </button>
                  </div>
                </div>

                <div className="flex items-start space-x-2">
                  <input
                    type="checkbox"
                    name="agreeToTerms"
                    checked={formData.agreeToTerms}
                    onChange={handleChange}
                    className="rounded border-surface-border mt-1"
                    required
                  />
                  <span className="text-sm text-text-secondary">
                    I agree to the{' '}
                    <Link to="/terms" className="text-accent-gradient-from hover:underline">
                      Terms of Service
                    </Link>{' '}
                    and{' '}
                    <Link to="/privacy" className="text-accent-gradient-from hover:underline">
                      Privacy Policy
                    </Link>
                  </span>
                </div>

                <Button type="submit" className="w-full group" disabled={isLoading}>
                  {isLoading ? 'Creating Account...' : 'Start Free Trial'}
                  <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                </Button>
              </form>

              <div className="text-center">
                <span className="text-text-secondary">Already have an account? </span>
                <Link 
                  to="/login" 
                  className="text-accent-gradient-from hover:text-accent-gradient-to font-medium transition-colors"
                >
                  Sign in
                </Link>
              </div>
            </CardContent>
          </Card>

          {/* Trust Indicators */}
          <div className="mt-6 text-center space-y-2">
            <div className="flex items-center justify-center space-x-4 text-xs text-text-secondary">
              <div className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-success rounded-full" />
                <span>SSL Secured</span>
              </div>
              <div className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-success rounded-full" />
                <span>GDPR Compliant</span>
              </div>
              <div className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-success rounded-full" />
                <span>SOC 2 Certified</span>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default SignupPage;