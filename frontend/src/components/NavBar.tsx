import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion, useScroll, useMotionValueEvent } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Menu, X, Globe } from 'lucide-react';
import { cn } from '@/lib/utils';

const NavBar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const { scrollY } = useScroll();
  const location = useLocation();

  useMotionValueEvent(scrollY, 'change', (latest) => {
    setIsScrolled(latest > 10);
  });

  const navItems = [
    { label: 'Features', href: '/features' },
    { label: 'Pricing', href: '/pricing' },
    { label: 'Contact', href: '/contact' },
  ];

  const isActive = (path: string) => location.pathname === path;

  return (
    <motion.nav
      className={cn(
        'fixed top-0 left-0 right-0 z-50 transition-all duration-300',
        isScrolled 
          ? 'glass-effect border-b border-surface-border shadow-lg' 
          : 'bg-transparent'
      )}
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2 group">
            <div className="relative">
              <Globe className="h-8 w-8 text-accent-gradient-from group-hover:text-accent-gradient-to transition-colors" />
              <div className="absolute -inset-1 bg-gradient-accent rounded-full opacity-0 group-hover:opacity-20 blur transition-opacity" />
            </div>
            <span className="text-xl font-bold gradient-text">Unarchived</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navItems.map((item) => (
              <Link
                key={item.href}
                to={item.href}
                className={cn(
                  'text-sm font-medium transition-colors hover:text-text-accent relative',
                  isActive(item.href) ? 'text-text-accent' : 'text-text-secondary'
                )}
              >
                {item.label}
                {isActive(item.href) && (
                  <motion.div
                    className="absolute -bottom-1 left-0 right-0 h-0.5 bg-gradient-accent rounded-full"
                    layoutId="navbar-indicator"
                  />
                )}
              </Link>
            ))}
          </div>

          {/* Desktop Auth Buttons */}
          <div className="hidden md:flex items-center space-x-4">
            <Link to="/login">
              <Button variant="ghost" size="sm">Login</Button>
            </Link>
            <Link to="/signup">
              <Button size="sm">Start Free</Button>
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden text-text-primary hover:text-text-accent transition-colors"
            onClick={() => setIsOpen(!isOpen)}
            aria-label="Toggle menu"
          >
            {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      <motion.div
        className={cn(
          'md:hidden glass-effect border-t border-surface-border',
          isOpen ? 'block' : 'hidden'
        )}
        initial={{ opacity: 0, height: 0 }}
        animate={{ 
          opacity: isOpen ? 1 : 0, 
          height: isOpen ? 'auto' : 0 
        }}
        transition={{ duration: 0.2 }}
      >
        <div className="px-4 py-4 space-y-3">
          {navItems.map((item) => (
            <Link
              key={item.href}
              to={item.href}
              className={cn(
                'block py-2 text-sm font-medium transition-colors',
                isActive(item.href) ? 'text-text-accent' : 'text-text-secondary hover:text-text-accent'
              )}
              onClick={() => setIsOpen(false)}
            >
              {item.label}
            </Link>
          ))}
          <div className="pt-4 space-y-2">
            <Link to="/login" onClick={() => setIsOpen(false)}>
              <Button variant="ghost" className="w-full">Login</Button>
            </Link>
            <Link to="/signup" onClick={() => setIsOpen(false)}>
              <Button className="w-full">Start Free</Button>
            </Link>
          </div>
        </div>
      </motion.div>
    </motion.nav>
  );
};

export default NavBar;