import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import QuoteMatrix from '@/components/QuoteMatrix';
import EscrowTimeline from '@/components/EscrowTimeline';
import ShipmentTracker from '@/components/ShipmentTracker';

const DashboardCarousel = () => {
  const [currentSlide, setCurrentSlide] = useState(0);

  const slides = [
    {
      id: 'quotes',
      title: 'Quote Comparison',
      description: 'Compare multiple supplier quotes side by side',
      component: <QuoteMatrix />
    },
    {
      id: 'escrow',
      title: 'Escrow Protection',
      description: 'Milestone-based payments with escrow security',
      component: <EscrowTimeline />
    },
    {
      id: 'tracking',
      title: 'Shipment Tracking',
      description: 'Real-time logistics and delivery monitoring',
      component: <ShipmentTracker />
    }
  ];

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % slides.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);
  };

  // Auto-advance slides
  useEffect(() => {
    const interval = setInterval(nextSlide, 8000);
    return () => clearInterval(interval);
  }, []);

  return (
    <Card className="relative h-[500px] overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-surface-border">
        <div>
          <h3 className="font-semibold text-text-primary">{slides[currentSlide].title}</h3>
          <p className="text-sm text-text-secondary">{slides[currentSlide].description}</p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="ghost" size="icon" onClick={prevSlide}>
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="icon" onClick={nextSlide}>
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Slides */}
      <div className="relative h-full">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentSlide}
            initial={{ opacity: 0, x: 300 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -300 }}
            transition={{ duration: 0.5, ease: "easeInOut" }}
            className="absolute inset-0 p-4 overflow-y-auto"
          >
            {slides[currentSlide].component}
          </motion.div>
        </AnimatePresence>
      </div>

      {/* Indicators */}
      <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2">
        {slides.map((_, index) => (
          <button
            key={index}
            className={`w-2 h-2 rounded-full transition-colors ${
              index === currentSlide ? 'bg-accent-gradient-from' : 'bg-surface-border'
            }`}
            onClick={() => setCurrentSlide(index)}
          />
        ))}
      </div>
    </Card>
  );
};

export default DashboardCarousel;