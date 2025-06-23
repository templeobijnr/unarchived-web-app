import { motion } from 'framer-motion';
import DemoChat from '@/components/DemoChat';
import DashboardCarousel from '@/components/DashboardCarousel';

const DemoSection = () => {
  return (
    <section id="demo" className="py-20 px-4">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-5xl font-bold mb-6">
            See Unarchived in <span className="gradient-text">Action</span>
          </h2>
          <p className="text-lg text-text-secondary max-w-3xl mx-auto">
            Experience the power of AI-driven sourcing. Chat with our AI assistant 
            and explore the comprehensive dashboard that manages your entire supply chain.
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-8 items-start">
          <motion.div
            initial={{ opacity: 0, x: -40 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <div className="mb-6">
              <h3 className="text-2xl font-semibold text-text-primary mb-2">
                AI Sourcing Assistant
              </h3>
              <p className="text-text-secondary">
                Ask questions, get quotes, and manage your sourcing pipeline through natural conversation.
              </p>
            </div>
            <DemoChat mode="marketing" />
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 40 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            <div className="mb-6">
              <h3 className="text-2xl font-semibold text-text-primary mb-2">
                Complete Dashboard
              </h3>
              <p className="text-text-secondary">
                Track quotes, manage suppliers, monitor shipments, and analyze your sourcing performance.
              </p>
            </div>
            <DashboardCarousel />
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default DemoSection;