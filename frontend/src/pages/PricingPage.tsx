import { useState } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Check, Star, ArrowRight, Zap } from 'lucide-react';
import { Link } from 'react-router-dom';

const PricingPage = () => {
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'yearly'>('monthly');

  const plans = [
    {
      name: 'Starter',
      description: 'Perfect for small businesses getting started with global sourcing',
      price: { monthly: 29, yearly: 24 },
      savings: billingCycle === 'yearly' ? 17 : 0,
      features: [
        '5 RFQs per month',
        'Up to 20 supplier connections',
        'Basic quote comparison',
        'Email support (48h response)',
        'Standard escrow protection',
        'Basic analytics dashboard',
        'Mobile app access',
        'Standard supplier verification'
      ],
      limits: [
        '1 user account',
        'Basic integrations only',
        'Standard support priority'
      ],
      cta: 'Start Free Trial',
      popular: false,
      color: 'from-blue-500 to-cyan-500'
    },
    {
      name: 'Professional',
      description: 'For growing companies with regular sourcing needs',
      price: { monthly: 99, yearly: 82 },
      savings: billingCycle === 'yearly' ? 17 : 0,
      features: [
        '50 RFQs per month',
        'Up to 200 supplier connections',
        'Advanced quote matrix & analytics',
        'Priority support & live chat',
        'Enhanced escrow with milestones',
        'Advanced analytics & custom reports',
        'API access & custom integrations',
        'Dedicated account manager',
        'Advanced supplier verification',
        'Custom contract templates',
        'Bulk order management',
        'Team collaboration tools'
      ],
      limits: [
        'Up to 5 user accounts',
        'Premium integrations included',
        'Priority support queue'
      ],
      cta: 'Start Free Trial',
      popular: true,
      color: 'from-purple-500 to-indigo-500'
    },
    {
      name: 'Enterprise',
      description: 'For large organizations with complex sourcing requirements',
      price: { monthly: 299, yearly: 249 },
      savings: billingCycle === 'yearly' ? 17 : 0,
      features: [
        'Unlimited RFQs',
        'Unlimited supplier connections',
        'Custom quote workflows',
        '24/7 phone & chat support',
        'Advanced escrow & financing options',
        'Custom analytics & dashboards',
        'Full API access & white-label options',
        'Dedicated sourcing team',
        'Custom contract terms',
        'Advanced security & compliance',
        'Private supplier network',
        'Custom training & onboarding',
        'SLA guarantees',
        'Advanced reporting suite'
      ],
      limits: [
        'Unlimited user accounts',
        'All integrations included',
        'Dedicated support team'
      ],
      cta: 'Contact Sales',
      popular: false,
      color: 'from-green-500 to-emerald-500'
    }
  ];

  const features = [
    {
      category: 'Core Features',
      items: [
        { name: 'AI-Powered Chat Assistant', starter: true, pro: true, enterprise: true },
        { name: 'Supplier Network Access', starter: '20 suppliers', pro: '200 suppliers', enterprise: 'Unlimited' },
        { name: 'Quote Comparison Tools', starter: 'Basic', pro: 'Advanced', enterprise: 'Custom' },
        { name: 'Escrow Protection', starter: 'Standard', pro: 'Milestone-based', enterprise: 'Advanced + Financing' },
        { name: 'Shipment Tracking', starter: true, pro: true, enterprise: true },
        { name: 'Mobile App', starter: true, pro: true, enterprise: true }
      ]
    },
    {
      category: 'Analytics & Reporting',
      items: [
        { name: 'Basic Analytics', starter: true, pro: true, enterprise: true },
        { name: 'Custom Reports', starter: false, pro: true, enterprise: true },
        { name: 'Advanced Dashboards', starter: false, pro: true, enterprise: 'Custom' },
        { name: 'API Access', starter: false, pro: 'Standard', enterprise: 'Full' },
        { name: 'Data Export', starter: 'CSV', pro: 'CSV, Excel', enterprise: 'All formats' }
      ]
    },
    {
      category: 'Support & Services',
      items: [
        { name: 'Email Support', starter: '48h response', pro: '24h response', enterprise: '2h response' },
        { name: 'Live Chat', starter: false, pro: true, enterprise: true },
        { name: 'Phone Support', starter: false, pro: false, enterprise: true },
        { name: 'Account Manager', starter: false, pro: true, enterprise: 'Dedicated team' },
        { name: 'Training & Onboarding', starter: 'Self-service', pro: 'Guided', enterprise: 'Custom' }
      ]
    }
  ];

  const faqs = [
    {
      question: 'How does the free trial work?',
      answer: 'Start with a 14-day free trial on any plan. No credit card required. You get full access to all features of your chosen plan during the trial period.'
    },
    {
      question: 'What happens if I exceed my RFQ limit?',
      answer: 'You can purchase additional RFQs at $5 each, or upgrade to a higher plan. We\'ll notify you when you\'re approaching 80% of your limit.'
    },
    {
      question: 'How secure are the escrow payments?',
      answer: 'Our escrow service is fully licensed and regulated. Payments are held in segregated accounts and released only when predefined milestones are met.'
    },
    {
      question: 'Can I change plans at any time?',
      answer: 'Yes, you can upgrade or downgrade at any time. Upgrades take effect immediately, while downgrades take effect at the next billing cycle.'
    },
    {
      question: 'Do you offer custom enterprise solutions?',
      answer: 'Yes, we offer fully customized solutions for large enterprises including private supplier networks, custom integrations, and dedicated support teams.'
    },
    {
      question: 'What payment methods do you accept?',
      answer: 'We accept all major credit cards, PayPal, and wire transfers for enterprise customers. All payments are processed securely through Stripe.'
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
              Transparent Pricing, No Hidden Fees
            </Badge>
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Choose Your <span className="gradient-text">Sourcing Plan</span>
            </h1>
            <p className="text-xl text-text-secondary max-w-3xl mx-auto mb-8">
              Scale your global sourcing operations with plans designed for every business size. 
              All plans include our core AI features with no setup fees.
            </p>

            {/* Billing Toggle */}
            <div className="inline-flex items-center p-1 glass-effect rounded-lg border border-surface-border mb-8">
              <button
                onClick={() => setBillingCycle('monthly')}
                className={`px-6 py-3 rounded-md text-sm font-medium transition-all ${
                  billingCycle === 'monthly'
                    ? 'bg-gradient-accent text-white shadow-lg'
                    : 'text-text-secondary hover:text-text-primary'
                }`}
              >
                Monthly
              </button>
              <button
                onClick={() => setBillingCycle('yearly')}
                className={`px-6 py-3 rounded-md text-sm font-medium transition-all relative ${
                  billingCycle === 'yearly'
                    ? 'bg-gradient-accent text-white shadow-lg'
                    : 'text-text-secondary hover:text-text-primary'
                }`}
              >
                Yearly
                <Badge className="absolute -top-2 -right-2 bg-success text-white text-xs">
                  Save 17%
                </Badge>
              </button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Pricing Cards */}
      <section className="pb-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-3 gap-8 mb-16">
            {plans.map((plan, index) => (
              <motion.div
                key={plan.name}
                initial={{ opacity: 0, y: 40 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="relative"
              >
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 z-10">
                    <Badge className="bg-gradient-accent text-white px-4 py-2">
                      <Star className="w-4 h-4 mr-1" />
                      Most Popular
                    </Badge>
                  </div>
                )}
                
                <Card className={`h-full relative overflow-hidden ${plan.popular ? 'ring-2 ring-accent-gradient-from shadow-2xl scale-105' : ''}`}>
                  {/* Gradient Background */}
                  <div className={`absolute inset-0 bg-gradient-to-br ${plan.color} opacity-5`} />
                  
                  <CardHeader className="text-center pb-8 relative">
                    <CardTitle className="text-2xl font-bold text-text-primary mb-2">{plan.name}</CardTitle>
                    <p className="text-text-secondary mb-6">{plan.description}</p>
                    
                    <div className="space-y-2">
                      <div className="flex items-baseline justify-center">
                        <span className="text-5xl font-bold text-text-primary">
                          ${plan.price[billingCycle]}
                        </span>
                        <span className="text-text-secondary ml-2">
                          /month
                        </span>
                      </div>
                      {billingCycle === 'yearly' && plan.savings > 0 && (
                        <div className="text-sm text-success">
                          Save ${plan.savings * 12}/year
                        </div>
                      )}
                      {billingCycle === 'yearly' && (
                        <div className="text-xs text-text-secondary">
                          Billed annually (${plan.price.yearly * 12}/year)
                        </div>
                      )}
                    </div>
                  </CardHeader>

                  <CardContent className="space-y-6 relative">
                    {/* Features */}
                    <div>
                      <h4 className="font-semibold text-text-primary mb-3">Everything included:</h4>
                      <ul className="space-y-3">
                        {plan.features.map((feature, featureIndex) => (
                          <li key={featureIndex} className="flex items-start space-x-3">
                            <Check className="w-5 h-5 text-success shrink-0 mt-0.5" />
                            <span className="text-text-primary text-sm">{feature}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    {/* Limits */}
                    {plan.limits && (
                      <div className="pt-4 border-t border-surface-border">
                        <h4 className="font-semibold text-text-primary mb-3">Plan details:</h4>
                        <ul className="space-y-2">
                          {plan.limits.map((limit, limitIndex) => (
                            <li key={limitIndex} className="text-text-secondary text-sm">
                              • {limit}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    <div className="pt-6">
                      {plan.name === 'Enterprise' ? (
                        <Link to="/contact" className="block">
                          <Button 
                            className="w-full"
                            variant={plan.popular ? 'default' : 'outline'}
                          >
                            {plan.cta}
                            <ArrowRight className="ml-2 h-4 w-4" />
                          </Button>
                        </Link>
                      ) : (
                        <Link to="/signup" className="block">
                          <Button 
                            className={`w-full ${plan.popular ? 'bg-gradient-accent' : ''}`}
                            variant={plan.popular ? 'default' : 'outline'}
                          >
                            {plan.cta}
                            <ArrowRight className="ml-2 h-4 w-4" />
                          </Button>
                        </Link>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Feature Comparison Table */}
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
              Compare <span className="gradient-text">All Features</span>
            </h2>
            <p className="text-lg text-text-secondary max-w-3xl mx-auto">
              Detailed breakdown of what's included in each plan to help you choose the right fit.
            </p>
          </motion.div>

          <Card className="overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-surface-glass/50">
                  <tr>
                    <th className="text-left p-4 font-semibold text-text-primary">Features</th>
                    <th className="text-center p-4 font-semibold text-text-primary">Starter</th>
                    <th className="text-center p-4 font-semibold text-text-primary">Professional</th>
                    <th className="text-center p-4 font-semibold text-text-primary">Enterprise</th>
                  </tr>
                </thead>
                <tbody>
                  {features.map((category, categoryIndex) => (
                    <React.Fragment key={category.category}>
                      <tr className="bg-surface-glass/30">
                        <td colSpan={4} className="p-4 font-semibold text-text-accent">
                          {category.category}
                        </td>
                      </tr>
                      {category.items.map((item, itemIndex) => (
                        <tr key={itemIndex} className="border-b border-surface-border hover:bg-surface-glass/20">
                          <td className="p-4 text-text-primary">{item.name}</td>
                          <td className="p-4 text-center">
                            {typeof item.starter === 'boolean' ? (
                              item.starter ? <Check className="w-5 h-5 text-success mx-auto" /> : '—'
                            ) : (
                              <span className="text-text-primary">{item.starter}</span>
                            )}
                          </td>
                          <td className="p-4 text-center">
                            {typeof item.pro === 'boolean' ? (
                              item.pro ? <Check className="w-5 h-5 text-success mx-auto" /> : '—'
                            ) : (
                              <span className="text-text-primary">{item.pro}</span>
                            )}
                          </td>
                          <td className="p-4 text-center">
                            {typeof item.enterprise === 'boolean' ? (
                              item.enterprise ? <Check className="w-5 h-5 text-success mx-auto" /> : '—'
                            ) : (
                              <span className="text-text-primary">{item.enterprise}</span>
                            )}
                          </td>
                        </tr>
                      ))}
                    </React.Fragment>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-5xl font-bold mb-6">
              Frequently Asked <span className="gradient-text">Questions</span>
            </h2>
            <p className="text-lg text-text-secondary">
              Everything you need to know about our pricing and plans.
            </p>
          </motion.div>

          <div className="space-y-6">
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
                    <h3 className="font-semibold text-text-primary mb-3 text-lg">{faq.question}</h3>
                    <p className="text-text-secondary leading-relaxed">{faq.answer}</p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
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
              Ready to Get Started?
            </h2>
            <p className="text-lg text-text-secondary mb-8">
              Join thousands of companies transforming their sourcing operations with Unarchived.
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
            <p className="text-sm text-text-secondary mt-6">
              No credit card required • 14-day free trial • Cancel anytime
            </p>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default PricingPage;