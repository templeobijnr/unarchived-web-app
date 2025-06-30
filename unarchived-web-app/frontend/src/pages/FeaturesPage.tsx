import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { 
  MessageSquare, 
  Search, 
  Shield, 
  TrendingUp, 
  Globe, 
  Zap,
  Award,
  BarChart3,
  Clock,
  ArrowRight,
  CheckCircle,
  PlayCircle
} from 'lucide-react';
import { Link } from 'react-router-dom';

const FeaturesPage = () => {
  const mainFeatures = [
    {
      icon: MessageSquare,
      title: 'AI-Powered Sourcing Assistant',
      description: 'Natural language processing that understands your sourcing needs and matches you with the right suppliers instantly.',
      benefits: [
        'Conversational interface - no forms to fill',
        'Intelligent supplier matching algorithms',
        'Automated RFQ generation and distribution',
        'Real-time supplier availability checking'
      ],
      demo: 'Chat with our AI to source custom phone cases',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      icon: Search,
      title: 'Global Supplier Network',
      description: 'Access to 50,000+ verified suppliers across 40+ countries with comprehensive capability matching.',
      benefits: [
        'Multi-tier supplier verification process',
        'Real-time capability and capacity data',
        'Compliance and certification tracking',
        'Performance history and ratings'
      ],
      demo: 'Explore our supplier database',
      color: 'from-green-500 to-emerald-500'
    },
    {
      icon: Shield,
      title: 'Milestone-Based Escrow',
      description: 'Secure payment protection with milestone-based releases, ensuring quality and delivery compliance.',
      benefits: [
        'Licensed escrow service protection',
        'Customizable milestone definitions',
        'Automated quality checkpoints',
        'Dispute resolution support'
      ],
      demo: 'See escrow protection in action',
      color: 'from-purple-500 to-indigo-500'
    },
    {
      icon: TrendingUp,
      title: 'Advanced Quote Comparison',
      description: 'Side-by-side analysis with automated cost optimization and supplier performance insights.',
      benefits: [
        'Multi-currency comparison tools',
        'Total cost of ownership analysis',
        'Lead time and quality scoring',
        'Negotiation recommendations'
      ],
      demo: 'Compare quotes from 3 suppliers',
      color: 'from-yellow-500 to-orange-500'
    },
    {
      icon: Globe,
      title: 'End-to-End Logistics',
      description: 'Complete shipment tracking with freight optimization and customs handling support.',
      benefits: [
        'Real-time shipment tracking',
        'Freight rate optimization',
        'Customs documentation support',
        'Delivery milestone notifications'
      ],
      demo: 'Track a shipment from China to USA',
      color: 'from-cyan-500 to-blue-500'
    },
    {
      icon: BarChart3,
      title: 'Analytics & Insights',
      description: 'Comprehensive dashboards with cost savings analysis and supplier performance metrics.',
      benefits: [
        'Cost savings tracking and reporting',
        'Supplier performance analytics',
        'Procurement trend analysis',
        'Custom KPI dashboards'
      ],
      demo: 'View analytics dashboard',
      color: 'from-indigo-500 to-purple-500'
    }
  ];

  const workflow = [
    {
      step: 1,
      title: 'Describe Your Needs',
      description: 'Chat with our AI assistant about your sourcing requirements',
      icon: MessageSquare
    },
    {
      step: 2,
      title: 'AI Matches Suppliers',
      description: 'Our algorithm finds and verifies the best suppliers for your needs',
      icon: Search
    },
    {
      step: 3,
      title: 'Compare Quotes',
      description: 'Review and compare detailed quotes side-by-side',
      icon: TrendingUp
    },
    {
      step: 4,
      title: 'Secure Payment',
      description: 'Use milestone-based escrow for secure transactions',
      icon: Shield
    },
    {
      step: 5,
      title: 'Track & Deliver',
      description: 'Monitor your order from production to delivery',
      icon: Globe
    }
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
              <Zap className="w-4 h-4 mr-2" />
              Revolutionary Sourcing Technology
            </Badge>
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Features Built for <span className="gradient-text">Modern Sourcing</span>
            </h1>
            <p className="text-xl text-text-secondary max-w-3xl mx-auto mb-8">
              Discover how our AI-powered platform transforms global sourcing with intelligent 
              automation, secure transactions, and comprehensive supplier management.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/signup">
                <Button size="xl">
                  Start Free Trial
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Button variant="glass" size="xl">
                <PlayCircle className="mr-2 h-5 w-5" />
                Watch Demo
              </Button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Main Features */}
      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="space-y-20">
            {mainFeatures.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                className={`flex flex-col ${index % 2 === 0 ? 'lg:flex-row' : 'lg:flex-row-reverse'} items-center gap-12`}
              >
                {/* Content */}
                <div className="flex-1 space-y-6">
                  <div className="flex items-center space-x-4">
                    <div className={`w-16 h-16 rounded-2xl bg-gradient-to-r ${feature.color} p-4 flex items-center justify-center`}>
                      <feature.icon className="w-8 h-8 text-white" />
                    </div>
                    <div>
                      <h2 className="text-3xl font-bold text-text-primary">{feature.title}</h2>
                      <p className="text-text-secondary text-lg">{feature.description}</p>
                    </div>
                  </div>

                  <ul className="space-y-3">
                    {feature.benefits.map((benefit, benefitIndex) => (
                      <li key={benefitIndex} className="flex items-start space-x-3">
                        <CheckCircle className="w-5 h-5 text-success shrink-0 mt-1" />
                        <span className="text-text-primary">{benefit}</span>
                      </li>
                    ))}
                  </ul>

                  <Button variant="outline" className="group">
                    {feature.demo}
                    <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                  </Button>
                </div>

                {/* Visual */}
                <div className="flex-1">
                  <Card className="p-8 glass-effect">
                    <div className={`h-64 rounded-lg bg-gradient-to-r ${feature.color} opacity-20 flex items-center justify-center`}>
                      <feature.icon className="w-24 h-24 text-white opacity-50" />
                    </div>
                  </Card>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Workflow Section */}
      <section className="py-20 px-4 bg-surface-glass/30">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-5xl font-bold mb-6">
              From Idea to <span className="gradient-text">Delivery</span>
            </h2>
            <p className="text-lg text-text-secondary max-w-3xl mx-auto">
              Our streamlined workflow takes you from initial concept to final delivery 
              with complete transparency and security at every step.
            </p>
          </motion.div>

          <div className="relative">
            {/* Connection Lines */}
            <div className="hidden md:block absolute top-1/2 left-0 right-0 h-0.5 bg-gradient-accent opacity-20" />
            
            <div className="grid md:grid-cols-5 gap-8">
              {workflow.map((item, index) => (
                <motion.div
                  key={item.step}
                  initial={{ opacity: 0, y: 40 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="relative"
                >
                  <Card className="text-center p-6 hover:shadow-xl transition-all duration-300 relative z-10">
                    <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-accent flex items-center justify-center">
                      <item.icon className="w-8 h-8 text-white" />
                    </div>
                    <div className="text-sm font-bold text-accent-gradient-from mb-2">
                      STEP {item.step}
                    </div>
                    <h3 className="font-semibold text-text-primary mb-2">{item.title}</h3>
                    <p className="text-sm text-text-secondary">{item.description}</p>
                  </Card>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="glass-effect rounded-2xl p-12 border border-surface-border"
          >
            <h2 className="text-3xl font-bold text-text-primary mb-6">
              Ready to Transform Your Sourcing?
            </h2>
            <p className="text-lg text-text-secondary mb-8">
              Join thousands of companies already saving time and money with intelligent sourcing.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/signup">
                <Button size="xl" className="group">
                  Start Free Trial
                  <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
                </Button>
              </Link>
              <Link to="/contact">
                <Button variant="outline" size="xl">
                  Talk to Sales
                </Button>
              </Link>
            </div>
            <p className="text-sm text-text-secondary mt-4">
              No credit card required • 14-day free trial • Cancel anytime
            </p>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default FeaturesPage;