import { useState } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Check, Star } from 'lucide-react';
import { Link } from 'react-router-dom';

const PricingSection = () => {
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'yearly'>('monthly');

  const plans = [
    {
      name: 'Starter',
      description: 'Perfect for small businesses getting started',
      price: { monthly: 29, yearly: 24 },
      features: [
        '5 RFQs per month',
        'Up to 20 supplier connections',
        'Basic quote comparison',
        'Email support',
        'Standard escrow protection',
        'Basic analytics'
      ],
      cta: 'Start Free Trial',
      popular: false
    },
    {
      name: 'Professional',
      description: 'For growing companies with regular sourcing needs',
      price: { monthly: 99, yearly: 82 },
      features: [
        '50 RFQs per month',
        'Up to 200 supplier connections',
        'Advanced quote matrix',
        'Priority support & chat',
        'Enhanced escrow with milestones',
        'Advanced analytics & reports',
        'Custom integration support',
        'Dedicated account manager'
      ],
      cta: 'Start Free Trial',
      popular: true
    },
    {
      name: 'Enterprise',
      description: 'For large organizations with complex requirements',
      price: { monthly: 299, yearly: 249 },
      features: [
        'Unlimited RFQs',
        'Unlimited supplier connections',
        'Custom quote workflows',
        '24/7 phone & chat support',
        'Advanced escrow & financing',
        'Custom analytics & dashboards',
        'Full API access',
        'Dedicated sourcing team',
        'Custom contract terms',
        'White-label options'
      ],
      cta: 'Contact Sales',
      popular: false
    }
  ];

  const faqs = [
    {
      question: 'How does the free trial work?',
      answer: 'Start with a 14-day free trial on any plan. No credit card required. You can cancel anytime during the trial period.'
    },
    {
      question: 'What happens if I exceed my RFQ limit?',
      answer: 'You can purchase additional RFQs or upgrade to a higher plan. We\'ll notify you when you\'re approaching your limit.'
    },
    {
      question: 'How secure are the escrow payments?',
      answer: 'Our escrow service is fully licensed and insured. Payments are held in segregated accounts and released only when milestones are met.'
    },
    {
      question: 'Can I change plans at any time?',
      answer: 'Yes, you can upgrade or downgrade your plan at any time. Changes take effect at the next billing cycle.'
    },
    {
      question: 'Do you offer custom enterprise solutions?',
      answer: 'Yes, we offer custom solutions for large enterprises including private supplier networks, custom integrations, and dedicated support teams.'
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
            Simple, <span className="gradient-text">Transparent Pricing</span>
          </h2>
          <p className="text-lg text-text-secondary max-w-3xl mx-auto mb-8">
            Choose the plan that fits your sourcing volume. All plans include our core features 
            with no setup fees or hidden costs.
          </p>

          {/* Billing Toggle */}
          <div className="inline-flex items-center p-1 glass-effect rounded-lg border border-surface-border">
            <button
              onClick={() => setBillingCycle('monthly')}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${
                billingCycle === 'monthly'
                  ? 'bg-gradient-accent text-white shadow-lg'
                  : 'text-text-secondary hover:text-text-primary'
              }`}
            >
              Monthly
            </button>
            <button
              onClick={() => setBillingCycle('yearly')}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-all relative ${
                billingCycle === 'yearly'
                  ? 'bg-gradient-accent text-white shadow-lg'
                  : 'text-text-secondary hover:text-text-primary'
              }`}
            >
              Yearly
              <Badge className="absolute -top-2 -right-2 bg-success text-white text-xs">
                Save 20%
              </Badge>
            </button>
          </div>
        </motion.div>

        {/* Pricing Cards */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          {plans.map((plan, index) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="relative"
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 z-10">
                  <Badge className="bg-gradient-accent text-white px-4 py-1">
                    <Star className="w-3 h-3 mr-1" />
                    Most Popular
                  </Badge>
                </div>
              )}
              
              <Card className={`h-full relative ${plan.popular ? 'ring-2 ring-accent-gradient-from shadow-2xl scale-105' : ''}`}>
                <CardHeader className="text-center pb-8">
                  <CardTitle className="text-2xl font-bold text-text-primary">{plan.name}</CardTitle>
                  <p className="text-text-secondary">{plan.description}</p>
                  <div className="mt-4">
                    <span className="text-4xl font-bold text-text-primary">
                      ${plan.price[billingCycle]}
                    </span>
                    <span className="text-text-secondary">
                      /{billingCycle === 'monthly' ? 'month' : 'month billed yearly'}
                    </span>
                  </div>
                </CardHeader>

                <CardContent className="space-y-4">
                  <ul className="space-y-3">
                    {plan.features.map((feature, featureIndex) => (
                      <li key={featureIndex} className="flex items-start space-x-3">
                        <Check className="w-5 h-5 text-success shrink-0 mt-0.5" />
                        <span className="text-text-primary text-sm">{feature}</span>
                      </li>
                    ))}
                  </ul>

                  <div className="pt-6">
                    <Link to="/signup" className="block">
                      <Button 
                        className={`w-full ${plan.popular ? 'bg-gradient-accent' : ''}`}
                        variant={plan.popular ? 'default' : 'outline'}
                      >
                        {plan.cta}
                      </Button>
                    </Link>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* FAQ Section */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="max-w-3xl mx-auto"
        >
          <h3 className="text-2xl font-bold text-text-primary text-center mb-8">
            Frequently Asked Questions
          </h3>
          <div className="space-y-4">
            {faqs.map((faq, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <Card>
                  <CardContent className="p-6">
                    <h4 className="font-semibold text-text-primary mb-2">{faq.question}</h4>
                    <p className="text-text-secondary">{faq.answer}</p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* CTA Section */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="text-center mt-16 p-8 glass-effect rounded-2xl border border-surface-border"
        >
          <h3 className="text-2xl font-bold text-text-primary mb-4">
            Still have questions?
          </h3>
          <p className="text-text-secondary mb-6">
            Our team is here to help you choose the right plan for your business.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/contact">
              <Button variant="outline">Contact Sales</Button>
            </Link>
            <Button>Start Free Trial</Button>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default PricingSection;