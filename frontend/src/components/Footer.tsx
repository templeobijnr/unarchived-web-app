import { Link } from 'react-router-dom';
import { Globe, Mail, Phone, MapPin, Twitter, Linkedin, Github } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  const footerLinks = {
    product: [
      { label: 'Features', href: '/features' },
      { label: 'Pricing', href: '/pricing' },
      { label: 'API Documentation', href: '/docs' },
      { label: 'Integrations', href: '/integrations' }
    ],
    company: [
      { label: 'About Us', href: '/about' },
      { label: 'Careers', href: '/careers' },
      { label: 'Press', href: '/press' },
      { label: 'Blog', href: '/blog' }
    ],
    support: [
      { label: 'Contact', href: '/contact' },
      { label: 'Help Center', href: '/help' },
      { label: 'Status', href: '/status' },
      { label: 'Security', href: '/security' }
    ],
    legal: [
      { label: 'Privacy Policy', href: '/privacy' },
      { label: 'Terms of Service', href: '/terms' },
      { label: 'Cookie Policy', href: '/cookies' },
      { label: 'GDPR', href: '/gdpr' }
    ]
  };

  const socialLinks = [
    { icon: Twitter, href: 'https://twitter.com/unarchived', label: 'Twitter' },
    { icon: Linkedin, href: 'https://linkedin.com/company/unarchived', label: 'LinkedIn' },
    { icon: Github, href: 'https://github.com/unarchived', label: 'GitHub' }
  ];

  return (
    <footer className="relative border-t border-surface-border">
      {/* Gradient Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-bg-gradient-to via-bg-gradient-via to-transparent opacity-50" />
      
      <div className="relative max-w-7xl mx-auto px-4 py-16">
        {/* Newsletter Section */}
        <div className="mb-16 text-center">
          <h3 className="text-2xl font-bold text-text-primary mb-4">
            Stay Updated on Global Sourcing Trends
          </h3>
          <p className="text-text-secondary mb-6 max-w-2xl mx-auto">
            Get weekly insights on supply chain optimization, new supplier networks, 
            and industry best practices delivered to your inbox.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
            <Input 
              type="email" 
              placeholder="Enter your email" 
              className="flex-1"
            />
            <Button>Subscribe</Button>
          </div>
          <p className="text-xs text-text-secondary mt-2">
            No spam. Unsubscribe at any time.
          </p>
        </div>

        {/* Main Footer Content */}
        <div className="grid md:grid-cols-2 lg:grid-cols-6 gap-8 mb-12">
          {/* Brand Column */}
          <div className="lg:col-span-2">
            <Link to="/" className="flex items-center space-x-2 mb-4">
              <div className="relative">
                <Globe className="h-8 w-8 text-accent-gradient-from" />
                <div className="absolute -inset-1 bg-gradient-accent rounded-full opacity-20 blur" />
              </div>
              <span className="text-xl font-bold gradient-text">Unarchived</span>
            </Link>
            <p className="text-text-secondary mb-6 max-w-sm">
              AI-powered global sourcing platform connecting businesses with verified suppliers worldwide. 
              Streamline your procurement process with intelligence and security.
            </p>
            
            {/* Contact Info */}
            <div className="space-y-2 text-sm text-text-secondary">
              <div className="flex items-center space-x-2">
                <Mail className="w-4 h-4" />
                <span>hello@unarchived.com</span>
              </div>
              <div className="flex items-center space-x-2">
                <Phone className="w-4 h-4" />
                <span>+1 (555) 123-4567</span>
              </div>
              <div className="flex items-center space-x-2">
                <MapPin className="w-4 h-4" />
                <span>San Francisco, CA</span>
              </div>
            </div>
          </div>

          {/* Product Links */}
          <div>
            <h4 className="font-semibold text-text-primary mb-4">Product</h4>
            <ul className="space-y-2">
              {footerLinks.product.map((link) => (
                <li key={link.label}>
                  <Link 
                    to={link.href}
                    className="text-text-secondary hover:text-text-accent transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Company Links */}
          <div>
            <h4 className="font-semibold text-text-primary mb-4">Company</h4>
            <ul className="space-y-2">
              {footerLinks.company.map((link) => (
                <li key={link.label}>
                  <Link 
                    to={link.href}
                    className="text-text-secondary hover:text-text-accent transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Support Links */}
          <div>
            <h4 className="font-semibold text-text-primary mb-4">Support</h4>
            <ul className="space-y-2">
              {footerLinks.support.map((link) => (
                <li key={link.label}>
                  <Link 
                    to={link.href}
                    className="text-text-secondary hover:text-text-accent transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal Links */}
          <div>
            <h4 className="font-semibold text-text-primary mb-4">Legal</h4>
            <ul className="space-y-2">
              {footerLinks.legal.map((link) => (
                <li key={link.label}>
                  <Link 
                    to={link.href}
                    className="text-text-secondary hover:text-text-accent transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="pt-8 border-t border-surface-border">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-text-secondary text-sm mb-4 md:mb-0">
              © {currentYear} Unarchived. All rights reserved.
            </div>
            
            {/* Social Links */}
            <div className="flex items-center space-x-4">
              {socialLinks.map((social) => (
                <a
                  key={social.label}
                  href={social.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-text-secondary hover:text-text-accent transition-colors"
                  aria-label={social.label}
                >
                  <social.icon className="w-5 h-5" />
                </a>
              ))}
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;