import { motion } from 'framer-motion';
import { Card, CardContent } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Star } from 'lucide-react';

const TestimonialsSection = () => {
  const testimonials = [
    {
      id: 1,
      name: 'Sarah Chen',
      role: 'Head of Procurement',
      company: 'TechFlow Industries',
      avatar: 'https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=100&h=100&fit=crop',
      content: 'Unarchived cut our sourcing time from weeks to days. The AI assistant understands exactly what we need and connects us with the right suppliers instantly.',
      rating: 5
    },
    {
      id: 2,
      name: 'Marcus Rodriguez',
      role: 'Supply Chain Director',
      company: 'Global Dynamics Corp',
      avatar: 'https://images.pexels.com/photos/1222271/pexels-photo-1222271.jpeg?auto=compress&cs=tinysrgb&w=100&h=100&fit=crop',
      content: 'The escrow protection gives us complete peace of mind. We\'ve processed over $2M in orders without a single payment issue.',
      rating: 5
    },
    {
      id: 3,
      name: 'Elena Petrov',
      role: 'Founder & CEO',
      company: 'NextGen Products',
      avatar: 'https://images.pexels.com/photos/415829/pexels-photo-415829.jpeg?auto=compress&cs=tinysrgb&w=100&h=100&fit=crop',
      content: 'As a startup, we needed reliable suppliers fast. Unarchived\'s verified network helped us scale from prototype to 10K units in just 3 months.',
      rating: 5
    },
    {
      id: 4,
      name: 'David Kim',
      role: 'Operations Manager',
      company: 'Innovate Solutions',
      avatar: 'https://images.pexels.com/photos/1516680/pexels-photo-1516680.jpeg?auto=compress&cs=tinysrgb&w=100&h=100&fit=crop',
      content: 'The real-time tracking and milestone payments transformed how we manage international orders. Complete transparency from start to finish.',
      rating: 5
    },
    {
      id: 5,
      name: 'Priya Sharma',
      role: 'Product Development Lead',
      company: 'Bright Future Tech',
      avatar: 'https://images.pexels.com/photos/1102341/pexels-photo-1102341.jpeg?auto=compress&cs=tinysrgb&w=100&h=100&fit=crop',
      content: 'We saved 40% on our procurement costs while improving quality. The supplier verification process is incredibly thorough.',
      rating: 5
    },
    {
      id: 6,
      name: 'James Wilson',
      role: 'Manufacturing Director',
      company: 'Precision Industries',
      avatar: 'https://images.pexels.com/photos/1674752/pexels-photo-1674752.jpeg?auto=compress&cs=tinysrgb&w=100&h=100&fit=crop',
      content: 'The quote comparison feature helped us identify cost savings we never knew existed. Unarchived pays for itself within the first order.',
      rating: 5
    }
  ];

  return (
    <section className="py-20 px-4 overflow-hidden">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-5xl font-bold mb-6">
            Trusted by <span className="gradient-text">Industry Leaders</span>
          </h2>
          <p className="text-lg text-text-secondary max-w-3xl mx-auto">
            See what procurement professionals are saying about their experience with Unarchived.
          </p>
        </motion.div>

        {/* Testimonials Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <motion.div
              key={testimonial.id}
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <Card className="h-full hover:shadow-xl transition-all duration-300">
                <CardContent className="p-6 h-full flex flex-col">
                  {/* Rating */}
                  <div className="flex items-center space-x-1 mb-4">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                    ))}
                  </div>

                  {/* Content */}
                  <blockquote className="flex-1 text-text-primary mb-6 italic">
                    "{testimonial.content}"
                  </blockquote>

                  {/* Author */}
                  <div className="flex items-center space-x-3">
                    <Avatar className="w-12 h-12">
                      <AvatarImage src={testimonial.avatar} alt={testimonial.name} />
                      <AvatarFallback>{testimonial.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                    </Avatar>
                    <div>
                      <div className="font-semibold text-text-primary">{testimonial.name}</div>
                      <div className="text-sm text-text-secondary">{testimonial.role}</div>
                      <div className="text-sm text-text-accent">{testimonial.company}</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Stats */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-8 mt-16 pt-16 border-t border-surface-border"
        >
          {[
            { label: 'Happy Customers', value: '1,000+' },
            { label: 'Orders Processed', value: '$50M+' },
            { label: 'Verified Suppliers', value: '50,000+' },
            { label: 'Countries Covered', value: '40+' }
          ].map((stat, index) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="text-center"
            >
              <div className="text-3xl md:text-4xl font-bold gradient-text mb-2">
                {stat.value}
              </div>
              <div className="text-text-secondary text-sm">
                {stat.label}
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
};

export default TestimonialsSection;