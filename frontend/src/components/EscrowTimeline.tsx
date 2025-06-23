import { motion } from 'framer-motion';
import { Check, Clock, DollarSign, Shield, Truck } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

const EscrowTimeline = () => {
  const steps = [
    {
      id: 1,
      title: 'Deposit Held',
      description: 'Your payment is secured in escrow',
      icon: Shield,
      status: 'completed',
      amount: '$12,500',
      date: 'Nov 15, 2024'
    },
    {
      id: 2,
      title: 'Sample Approved',
      description: 'Quality sample meets requirements',
      icon: Check,
      status: 'completed',
      amount: '$2,500',
      date: 'Nov 18, 2024'
    },
    {
      id: 3,
      title: 'Production Started',
      description: 'Manufacturing in progress',
      icon: Clock,
      status: 'active',
      amount: '$5,000',
      date: 'Nov 22, 2024'
    },
    {
      id: 4,
      title: 'QC Inspection',
      description: 'Quality control verification',
      icon: Check,
      status: 'pending',
      amount: '$2,500',
      date: 'Dec 5, 2024'
    },
    {
      id: 5,
      title: 'Shipped',
      description: 'Order dispatched to destination',
      icon: Truck,
      status: 'pending',
      amount: '$2,500',
      date: 'Dec 10, 2024'
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-success';
      case 'active': return 'bg-accent-gradient-from';
      case 'pending': return 'bg-surface-glass';
      default: return 'bg-surface-glass';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return Check;
      case 'active': return Clock;
      default: return Clock;
    }
  };

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h3 className="text-xl font-semibold text-text-primary mb-2">Escrow Timeline</h3>
        <p className="text-text-secondary">Milestone-based payments ensure secure transactions</p>
      </div>

      <div className="relative">
        {/* Progress Line */}
        <div className="absolute left-8 top-6 bottom-6 w-0.5 bg-surface-border" />
        <motion.div 
          className="absolute left-8 top-6 w-0.5 bg-gradient-accent"
          initial={{ height: 0 }}
          animate={{ height: '40%' }}
          transition={{ duration: 2, ease: "easeOut" }}
        />

        <div className="space-y-6">
          {steps.map((step, index) => {
            const Icon = step.icon;
            const StatusIcon = getStatusIcon(step.status);
            
            return (
              <motion.div
                key={step.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="relative flex items-start space-x-4"
              >
                {/* Timeline Dot */}
                <div className={`relative z-10 w-4 h-4 rounded-full ${getStatusColor(step.status)} flex items-center justify-center`}>
                  {step.status === 'completed' && (
                    <Check className="w-2.5 h-2.5 text-white" />
                  )}
                  {step.status === 'active' && (
                    <motion.div 
                      className="w-2 h-2 bg-white rounded-full"
                      animate={{ scale: [1, 1.2, 1] }}
                      transition={{ duration: 2, repeat: Infinity }}
                    />
                  )}
                </div>

                {/* Content Card */}
                <Card className="flex-1 p-4">
                  <CardContent className="p-0">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center space-x-2">
                        <Icon className="w-5 h-5 text-text-accent" />
                        <h4 className="font-semibold text-text-primary">{step.title}</h4>
                      </div>
                      <Badge 
                        variant={step.status === 'completed' ? 'success' : step.status === 'active' ? 'default' : 'secondary'}
                        className="text-xs"
                      >
                        {step.status}
                      </Badge>
                    </div>
                    
                    <p className="text-sm text-text-secondary mb-3">{step.description}</p>
                    
                    <div className="flex items-center justify-between text-sm">
                      <div className="flex items-center space-x-1">
                        <DollarSign className="w-4 h-4 text-success" />
                        <span className="font-medium text-text-primary">{step.amount}</span>
                      </div>
                      <span className="text-text-secondary">{step.date}</span>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            );
          })}
        </div>
      </div>

      {/* Summary */}
      <Card className="p-4 glass-effect">
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-success">$15,000</div>
            <div className="text-xs text-text-secondary">Released</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-text-accent">$10,000</div>
            <div className="text-xs text-text-secondary">In Escrow</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-text-primary">60%</div>
            <div className="text-xs text-text-secondary">Complete</div>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default EscrowTimeline;