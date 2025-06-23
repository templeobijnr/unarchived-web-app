import { useState } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { 
  Mail, 
  Phone, 
  MapPin, 
  MessageSquare,
  Clock,
  Globe,
  Users,
  ArrowRight,
  CheckCircle
} from 'lucide-react';

const ContactPage = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    company: '',
    phone: '',
    subject: '',
    message: '',
    inquiryType: 'general'
  });
  
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle form submission
    console.log('Form submitted:', formData);
    setIsSubmitted(true);
    setTimeout(() => setIsSubmitted(false), 3000);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const contactMethods = [
    {
      icon: Mail,
      title: 'Email Us',
      description: 'Get in touch via email',
      value: 'hello@unarchived.com',
      action: 'mailto:hello@unarchived.com',
      actionText: 'Send Email',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      icon: Phone,
      title: 'Call Us',
      description: 'Speak with our team',
      value: '+1 (555) 123-4567',
      action: 'tel:+15551234567',
      actionText: 'Call Now',
      color: 'from-green-500 to-emerald-500'
    },
    {
      icon: MessageSquare,
      title: 'Live Chat',
      description: 'Chat with support',
      value: 'Available 24/7',
      action: '#',
      actionText: 'Start Chat',
      color: 'from-purple-500 to-indigo-500'
    },
    {
      icon: MapPin,
      title: 'Visit Us',
      description: 'Our headquarters',
      value: 'San Francisco, CA',
      action: '#',
      actionText: 'Get Directions',
      color: 'from-orange-500 to-red-500'
    }
  ];

  const officeLocations = [
    {
      city: 'San Francisco',
      country: 'United States',
      address: '123 Market Street, Suite 100, San Francisco, CA 94105',
      phone: '+1 (555) 123-4567',
      email: 'us@unarchived.com',
      timezone: 'PST (UTC-8)',
      isHeadquarters: true
    },
    {
      city: 'London',
      country: 'United Kingdom',
      address: '456 Oxford Street, London W1C 1AP, UK',
      phone: '+44 20 7123 4567',
      email: 'uk@unarchived.com',
      timezone: 'GMT (UTC+0)'
    },
    {
      city: 'Singapore',
      country: 'Singapore',
      address: '789 Marina Bay, Singapore 018956',
      phone: '+65 6123 4567',
      email: 'sg@unarchived.com',
      timezone: 'SGT (UTC+8)'
    }
  ];

  const inquiryTypes = [
    { value: 'general', label: 'General Inquiry' },
    { value: 'sales', label: 'Sales & Pricing' },
    { value: 'support', label: 'Technical Support' },
    { value: 'partnership', label: 'Partnership' },
    { value: 'press', label: 'Press & Media' }
  ];

  return (
    <div className="min-h-screen bg-gradient-main">
      {/* Hero Section */}
      <section className="pt-24 pb-16 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <Badge className="mb-6 bg-gradient-accent text-white px-4 py-2">
              <Users className="w-4 h-4 mr-2" />
              We're Here to Help
            </Badge>
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Get in <span className="gradient-text">Touch</span>
            </h1>
            <p className="text-xl text-text-secondary max-w-3xl mx-auto">
              Have questions about our platform? Want to discuss enterprise solutions? 
              Our team is ready to help you transform your global sourcing operations.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Contact Methods */}
      <section className="pb-16 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {contactMethods.map((method, index) => (
              <motion.div
                key={method.title}
                initial={{ opacity: 0, y: 40 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <Card className="text-center hover:shadow-xl transition-all duration-300 group">
                  <CardContent className="p-6">
                    <div className={`w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-r ${method.color} p-4 flex items-center justify-center group-hover:scale-110 transition-transform`}>
                      <method.icon className="w-8 h-8 text-white" />
                    </div>
                    <h3 className="font-semibold text-text-primary mb-2">{method.title}</h3>
                    <p className="text-text-secondary text-sm mb-3">{method.description}</p>
                    <p className="font-medium text-text-primary mb-4">{method.value}</p>
                    <a href={method.action}>
                      <Button variant="outline" size="sm" className="group">
                        {method.actionText}
                        <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                      </Button>
                    </a>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Main Content */}
      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12">
            {/* Contact Form */}
            <motion.div
              initial={{ opacity: 0, x: -40 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
            >
              <Card>
                <CardHeader>
                  <CardTitle className="text-2xl">Send us a Message</CardTitle>
                  <p className="text-text-secondary">
                    Fill out the form below and we'll get back to you within 24 hours.
                  </p>
                </CardHeader>
                <CardContent>
                  {isSubmitted ? (
                    <motion.div
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      className="text-center py-8"
                    >
                      <CheckCircle className="w-16 h-16 text-success mx-auto mb-4" />
                      <h3 className="text-xl font-semibold text-text-primary mb-2">
                        Message Sent!
                      </h3>
                      <p className="text-text-secondary">
                        Thank you for reaching out. We'll get back to you soon.
                      </p>
                    </motion.div>
                  ) : (
                    <form onSubmit={handleSubmit} className="space-y-6">
                      <div className="grid md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-text-primary mb-2">
                            Full Name *
                          </label>
                          <Input
                            name="name"
                            value={formData.name}
                            onChange={handleChange}
                            required
                            placeholder="John Doe"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-text-primary mb-2">
                            Email Address *
                          </label>
                          <Input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            required
                            placeholder="john@company.com"
                          />
                        </div>
                      </div>

                      <div className="grid md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-text-primary mb-2">
                            Company
                          </label>
                          <Input
                            name="company"
                            value={formData.company}
                            onChange={handleChange}
                            placeholder="Your Company"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-text-primary mb-2">
                            Phone Number
                          </label>
                          <Input
                            type="tel"
                            name="phone"
                            value={formData.phone}
                            onChange={handleChange}
                            placeholder="+1 (555) 123-4567"
                          />
                        </div>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-text-primary mb-2">
                          Inquiry Type
                        </label>
                        <select
                          name="inquiryType"
                          value={formData.inquiryType}
                          onChange={handleChange}
                          className="w-full bg-surface-glass border border-surface-border rounded-md px-3 py-2 text-text-primary"
                        >
                          {inquiryTypes.map((type) => (
                            <option key={type.value} value={type.value}>
                              {type.label}
                            </option>
                          ))}
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-text-primary mb-2">
                          Subject *
                        </label>
                        <Input
                          name="subject"
                          value={formData.subject}
                          onChange={handleChange}
                          required
                          placeholder="How can we help you?"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-text-primary mb-2">
                          Message *
                        </label>
                        <textarea
                          name="message"
                          value={formData.message}
                          onChange={handleChange}
                          required
                          rows={6}
                          className="w-full bg-surface-glass border border-surface-border rounded-md px-3 py-2 text-text-primary resize-none"
                          placeholder="Tell us more about your needs..."
                        />
                      </div>

                      <Button type="submit" className="w-full">
                        Send Message
                        <ArrowRight className="ml-2 h-4 w-4" />
                      </Button>
                    </form>
                  )}
                </CardContent>
              </Card>
            </motion.div>

            {/* Office Locations */}
            <motion.div
              initial={{ opacity: 0, x: 40 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="space-y-8"
            >
              <div>
                <h2 className="text-2xl font-bold text-text-primary mb-4">
                  Our Global Offices
                </h2>
                <p className="text-text-secondary mb-6">
                  We have teams around the world ready to support your sourcing needs.
                </p>
              </div>

              <div className="space-y-6">
                {officeLocations.map((office, index) => (
                  <motion.div
                    key={office.city}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.5, delay: index * 0.1 }}
                  >
                    <Card>
                      <CardContent className="p-6">
                        <div className="flex items-start justify-between mb-4">
                          <div>
                            <h3 className="font-semibold text-text-primary text-lg">
                              {office.city}, {office.country}
                            </h3>
                            {office.isHeadquarters && (
                              <Badge variant="outline" className="mt-1">
                                Headquarters
                              </Badge>
                            )}
                          </div>
                          <Globe className="w-5 h-5 text-text-accent" />
                        </div>
                        
                        <div className="space-y-3 text-sm">
                          <div className="flex items-start space-x-2">
                            <MapPin className="w-4 h-4 text-text-accent mt-0.5 shrink-0" />
                            <span className="text-text-primary">{office.address}</span>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Phone className="w-4 h-4 text-text-accent" />
                            <span className="text-text-primary">{office.phone}</span>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Mail className="w-4 h-4 text-text-accent" />
                            <span className="text-text-primary">{office.email}</span>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Clock className="w-4 h-4 text-text-accent" />
                            <span className="text-text-secondary">{office.timezone}</span>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </motion.div>
                ))}
              </div>

              {/* Additional Info */}
              <Card className="bg-gradient-to-r from-accent-gradient-from/10 to-accent-gradient-to/10 border-accent-gradient-from/20">
                <CardContent className="p-6">
                  <h3 className="font-semibold text-text-primary mb-3">
                    Enterprise Support
                  </h3>
                  <p className="text-text-secondary text-sm mb-4">
                    Need dedicated support for your enterprise? Our team provides 24/7 assistance 
                    for enterprise customers with dedicated account managers and priority support.
                  </p>
                  <Button variant="outline" size="sm">
                    Learn More
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </CardContent>
              </Card>
            </motion.div>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-20 px-4 bg-surface-glass/30">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl font-bold text-text-primary mb-6">
              Quick <span className="gradient-text">Answers</span>
            </h2>
            <p className="text-lg text-text-secondary">
              Common questions about getting started with Unarchived.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 gap-6">
            {[
              {
                question: 'How quickly can I get started?',
                answer: 'You can start sourcing within minutes. Sign up, describe your needs to our AI, and get matched with suppliers instantly.'
              },
              {
                question: 'Do you offer custom integrations?',
                answer: 'Yes, we provide API access and custom integrations for enterprise customers to connect with existing systems.'
              },
              {
                question: 'What regions do you cover?',
                answer: 'We have verified suppliers in 40+ countries, with strong networks in Asia, Europe, and North America.'
              },
              {
                question: 'Is there a minimum order value?',
                answer: 'No minimum order value. Our platform works for everything from prototypes to large-scale production runs.'
              }
            ].map((faq, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <Card>
                  <CardContent className="p-6">
                    <h3 className="font-semibold text-text-primary mb-3">{faq.question}</h3>
                    <p className="text-text-secondary">{faq.answer}</p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default ContactPage;