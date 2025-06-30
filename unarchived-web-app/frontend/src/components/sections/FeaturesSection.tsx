import { motion } from 'framer-motion';
import { Card, CardContent } from '@/components/ui/card';
import { 
  MessageSquare, 
  Search, 
  Shield, 
  TrendingUp, 
  Globe, 
  Zap,
  Award,
  BarChart3,
  Clock
} from 'lucide-react';

const FeaturesSection = () => {
  const features = [
    {
      icon: MessageSquare,
      title: 'AI-Powered Chat',
      description: 'Natural language sourcing requests with intelligent supplier matching and automated quote generation.',
      color: 'text-blue-400'
    },
    {
      icon: Search,
      title: 'Global Supplier Network',
      description: 'Access to 50,000+ verified suppliers across 40+ countries with real-time capability matching.',
      color: 'text-green-400'
    },
    {
      icon: Shield,
      title: 'Escrow Protection',
      description: 'Milestone-based payments with built-in escrow service ensuring secure transactions.',
      color: 'text-purple-400'
    },
    {
      icon: TrendingUp,
      title: 'Quote Comparison',
      description: 'Side-by-side analysis of supplier quotes with automated cost optimization recommendations.',
      color: 'text-yellow-400'
    },
    {
      icon: Globe,
      title: 'Global Logistics',
      description: 'End-to-end shipment tracking with freight rate optimization and customs handling.',
      color: 'text-cyan-400'
    },
    {
      icon: Zap,
      title: '72-Hour Quotes',
      description: 'Guaranteed supplier responses within 72 hours or your money back.',
      color: 'text-orange-400'
    },
    {
      icon: Award,
      title: 'Quality Assurance',
      description: 'Automated quality control checks and supplier verification before every order.',
      color: 'text-red-400'
    },
    {
      icon: BarChart3,
      title: 'Analytics Dashboard',
      description: 'Real-time insights on cost savings, supplier performance, and procurement metrics.',
      color: 'text-indigo-400'
    },
    {
      icon: Clock,
      title: '24/7 Support',
      description: 'Round-the-clock assistance from our global sourcing experts and AI agents.',
      color: 'text-pink-400'
    }
  ];

  return (
    <section className="py-20 px-4">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-5xl font-bold mb-6">
            Everything You Need for <span className="gradient-text">Global Sourcing</span>
          </h2>
          <p className="text-lg text-text-secondary max-w-3xl mx-auto">
            From initial product research to final delivery, our AI-powered platform handles 
            every aspect of your global sourcing journey.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <Card className="h-full hover:shadow-2xl transition-all duration-300 group">
                <CardContent className="p-6 h-full flex flex-col">
                  <div className={`w-12 h-12 rounded-lg bg-surface-glass flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                    <feature.icon className={`w-6 h-6 ${feature.color}`} />
                  </div>
                  <h3 className="text-xl font-semibold text-text-primary mb-3">
                    {feature.title}
                  </h3>
                  <p className="text-text-secondary flex-1">
                    {feature.description}
                  </p>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Call to Action */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="text-center mt-16"
        >
          <div className="inline-flex items-center space-x-2 px-4 py-2 rounded-full glass-effect border border-surface-border mb-6">
            <Zap className="w-4 h-4 text-text-accent" />
            <span className="text-sm text-text-accent font-medium">Get started in minutes</span>
          </div>
          <h3 className="text-2xl font-bold text-text-primary mb-4">
            Ready to revolutionize your sourcing?
          </h3>
          <p className="text-text-secondary mb-6">
            Join 1,000+ companies already saving time and money with Unarchived.
          </p>
        </motion.div>
      </div>
    </section>
  );
};

export default FeaturesSection;