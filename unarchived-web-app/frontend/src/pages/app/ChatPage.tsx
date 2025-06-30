import { useState } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import DemoChat from '@/components/DemoChat';
import { 
  FileText, 
  Quote, 
  Languages, 
  Zap, 
  Clock, 
  DollarSign,
  Package,
  MapPin
} from 'lucide-react';

const ChatPage = () => {
  const [activeProject, setActiveProject] = useState({
    id: 'proj_001',
    name: 'Custom Phone Cases Q4',
    status: 'active',
    specs: {
      product: 'Custom Phone Cases',
      quantity: 10000,
      targetPrice: '$2.50',
      deadline: '2024-12-15',
      materials: ['TPU', 'PC', 'Silicone'],
      regions: ['China', 'Vietnam']
    }
  });

  const quickActions = [
    {
      icon: FileText,
      label: 'Send RFQ',
      description: 'Create a new request for quote',
      color: 'text-blue-400'
    },
    {
      icon: Quote,
      label: 'Show Quotes',
      description: 'View received supplier quotes',
      color: 'text-green-400'
    },
    {
      icon: Languages,
      label: 'Translate',
      description: 'Translate conversations',
      color: 'text-purple-400'
    },
    {
      icon: Zap,
      label: 'Quick Match',
      description: 'Find suppliers instantly',
      color: 'text-yellow-400'
    }
  ];

  const recentActivity = [
    {
      type: 'quote_received',
      supplier: 'Shenzhen Tech Cases',
      message: 'New quote received for phone cases',
      time: '2 minutes ago',
      amount: '$2.20'
    },
    {
      type: 'message_sent',
      supplier: 'AI Assistant',
      message: 'RFQ sent to 5 verified suppliers',
      time: '1 hour ago'
    },
    {
      type: 'supplier_matched',
      supplier: 'Guangzhou Mobile',
      message: 'New supplier match found',
      time: '3 hours ago'
    }
  ];

  return (
    <div className="h-full flex gap-6">
      {/* Main Chat Area - 70% */}
      <div className="flex-1 flex flex-col">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-text-primary">AI Sourcing Chat</h1>
              <p className="text-text-secondary">
                Communicate with your AI assistant for all sourcing needs
              </p>
            </div>
            <Badge 
              variant="success" 
              className="flex items-center space-x-1"
            >
              <div className="w-2 h-2 bg-white rounded-full" />
              <span>Assistant Online</span>
            </Badge>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="flex-1"
        >
          <DemoChat mode="app" className="h-full" />
        </motion.div>
      </div>

      {/* Context Panel - 30% */}
      <motion.div
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="w-80 space-y-6"
      >
        {/* Current Project */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Package className="w-5 h-5 text-text-accent" />
              <span>Active Project</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <h4 className="font-semibold text-text-primary">{activeProject.name}</h4>
              <Badge variant="success" className="mt-1">
                {activeProject.status}
              </Badge>
            </div>

            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-text-secondary">Product:</span>
                <span className="text-text-primary">{activeProject.specs.product}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-text-secondary">Quantity:</span>
                <span className="text-text-primary">{activeProject.specs.quantity.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-text-secondary">Target Price:</span>
                <span className="text-text-primary">{activeProject.specs.targetPrice}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-text-secondary">Deadline:</span>
                <span className="text-text-primary">{activeProject.specs.deadline}</span>
              </div>
            </div>

            <Separator />

            <div>
              <p className="text-xs text-text-secondary mb-2">MATERIALS</p>
              <div className="flex flex-wrap gap-1">
                {activeProject.specs.materials.map((material) => (
                  <Badge key={material} variant="outline" className="text-xs">
                    {material}
                  </Badge>
                ))}
              </div>
            </div>

            <div>
              <p className="text-xs text-text-secondary mb-2">REGIONS</p>
              <div className="flex flex-wrap gap-1">
                {activeProject.specs.regions.map((region) => (
                  <Badge key={region} variant="outline" className="text-xs">
                    <MapPin className="w-3 h-3 mr-1" />
                    {region}
                  </Badge>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {quickActions.map((action) => (
              <Button
                key={action.label}
                variant="ghost"
                className="w-full justify-start h-auto p-3"
              >
                <action.icon className={`w-4 h-4 mr-3 ${action.color}`} />
                <div className="text-left">
                  <div className="font-medium text-text-primary">{action.label}</div>
                  <div className="text-xs text-text-secondary">{action.description}</div>
                </div>
              </Button>
            ))}
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Clock className="w-5 h-5 text-text-accent" />
              <span>Recent Activity</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {recentActivity.map((activity, index) => (
              <div key={index} className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-accent-gradient-from rounded-full mt-2 shrink-0" />
                <div className="flex-1 text-sm">
                  <p className="text-text-primary font-medium">{activity.message}</p>
                  <div className="flex items-center justify-between mt-1">
                    <span className="text-text-secondary text-xs">{activity.supplier}</span>
                    <span className="text-text-secondary text-xs">{activity.time}</span>
                  </div>
                  {activity.amount && (
                    <div className="flex items-center space-x-1 mt-1">
                      <DollarSign className="w-3 h-3 text-success" />
                      <span className="text-success text-xs font-medium">{activity.amount}</span>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Chat Stats */}
        <Card>
          <CardContent className="p-4">
            <div className="grid grid-cols-2 gap-4 text-center">
              <div>
                <div className="text-2xl font-bold text-text-accent">24</div>
                <div className="text-xs text-text-secondary">Messages Today</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-success">12</div>
                <div className="text-xs text-text-secondary">Active RFQs</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
};

export default ChatPage;