import Hero from '@/components/Hero';
import DemoSection from '@/components/sections/DemoSection';
import FeaturesSection from '@/components/sections/FeaturesSection';
import PricingSection from '@/components/sections/PricingSection';
import TestimonialsSection from '@/components/sections/TestimonialsSection';
import Footer from '@/components/Footer';

const HomePage = () => {
  return (
    <main className="overflow-x-hidden">
      <Hero />
      <DemoSection />
      <FeaturesSection />
      <TestimonialsSection />
      <PricingSection />
      <Footer />
    </main>
  );
};

export default HomePage;