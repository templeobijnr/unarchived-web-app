import { motion } from 'framer-motion';
import { MapPin, Truck, Plane, Ship, Package } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

const ShipmentTracker = () => {
  const shipmentSteps = [
    {
      id: 1,
      location: 'Shenzhen, China',
      status: 'Picked up from supplier',
      timestamp: '2024-11-20 14:30',
      icon: Package,
      completed: true
    },
    {
      id: 2,
      location: 'Shenzhen Port, China',
      status: 'Departed port',
      timestamp: '2024-11-22 09:15',
      icon: Ship,
      completed: true
    },
    {
      id: 3,
      location: 'In Transit - Pacific Ocean',
      status: 'En route to Los Angeles',
      timestamp: '2024-11-25 Current',
      icon: Ship,
      completed: false,
      active: true
    },
    {
      id: 4,
      location: 'Los Angeles Port, USA',
      status: 'Expected arrival',
      timestamp: '2024-12-05 Estimated',
      icon: Truck,
      completed: false
    },
    {
      id: 5,
      location: 'Your Warehouse',
      status: 'Final delivery',
      timestamp: '2024-12-08 Estimated',
      icon: MapPin,
      completed: false
    }
  ];

  const shipmentInfo = {
    trackingNumber: 'UNA-2024-001847',
    vessel: 'COSCO SHIPPING AQUARIUS',
    container: 'CSNU7384920',
    estimatedArrival: 'Dec 8, 2024',
    currentLocation: 'Pacific Ocean (35.2°N, 150.8°W)'
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <h3 className="text-xl font-semibold text-text-primary mb-2">Shipment Tracking</h3>
        <p className="text-text-secondary">Real-time visibility of your order journey</p>
      </div>

      {/* Tracking Info */}
      <Card className="p-4 glass-effect">
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-text-secondary">Tracking #</span>
            <p className="font-mono text-text-primary">{shipmentInfo.trackingNumber}</p>
          </div>
          <div>
            <span className="text-text-secondary">Estimated Arrival</span>
            <p className="text-text-primary font-medium">{shipmentInfo.estimatedArrival}</p>
          </div>
          <div>
            <span className="text-text-secondary">Vessel</span>
            <p className="text-text-primary">{shipmentInfo.vessel}</p>
          </div>
          <div>
            <span className="text-text-secondary">Container</span>
            <p className="font-mono text-text-primary">{shipmentInfo.container}</p>
          </div>
        </div>
      </Card>

      {/* Current Status */}
      <Card className="p-4 bg-gradient-accent/10 border-accent-gradient-from/20">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-full bg-gradient-accent flex items-center justify-center">
            <Ship className="w-5 h-5 text-white" />
          </div>
          <div>
            <h4 className="font-semibold text-text-primary">Currently in Transit</h4>
            <p className="text-sm text-text-secondary">{shipmentInfo.currentLocation}</p>
          </div>
          <div className="ml-auto">
            <Badge className="bg-gradient-accent text-white">On Schedule</Badge>
          </div>
        </div>
      </Card>

      {/* Timeline */}
      <div className="relative">
        <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-surface-border" />
        <motion.div 
          className="absolute left-6 top-0 w-0.5 bg-gradient-accent"
          initial={{ height: 0 }}
          animate={{ height: '40%' }}
          transition={{ duration: 2, ease: "easeOut" }}
        />

        <div className="space-y-6">
          {shipmentSteps.map((step, index) => {
            const Icon = step.icon;
            
            return (
              <motion.div
                key={step.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="relative flex items-start space-x-4"
              >
                {/* Timeline Dot */}
                <div className={`relative z-10 w-3 h-3 rounded-full ${
                  step.completed 
                    ? 'bg-success' 
                    : step.active 
                      ? 'bg-accent-gradient-from' 
                      : 'bg-surface-glass'
                }`}>
                  {step.active && (
                    <motion.div 
                      className="absolute inset-0 rounded-full bg-accent-gradient-from"
                      animate={{ scale: [1, 1.5, 1], opacity: [1, 0, 1] }}
                      transition={{ duration: 2, repeat: Infinity }}
                    />
                  )}
                </div>

                {/* Content */}
                <div className="flex-1 pb-6">
                  <div className="flex items-center space-x-2 mb-1">
                    <Icon className={`w-4 h-4 ${
                      step.completed ? 'text-success' : step.active ? 'text-accent-gradient-from' : 'text-text-secondary'
                    }`} />
                    <h4 className="font-medium text-text-primary">{step.location}</h4>
                  </div>
                  <p className="text-sm text-text-secondary mb-1">{step.status}</p>
                  <p className="text-xs text-text-secondary">{step.timestamp}</p>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>

      {/* Delivery Progress */}
      <Card className="p-4">
        <CardHeader className="p-0 pb-4">
          <CardTitle className="text-lg">Delivery Progress</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <div className="flex justify-between text-sm text-text-secondary mb-2">
            <span>Progress</span>
            <span>40% Complete</span>
          </div>
          <div className="w-full bg-surface-glass rounded-full h-2">
            <motion.div 
              className="bg-gradient-accent h-2 rounded-full"
              initial={{ width: 0 }}
              animate={{ width: '40%' }}
              transition={{ duration: 2, ease: "easeOut" }}
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ShipmentTracker;