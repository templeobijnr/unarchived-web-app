import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import DemoChat from '@/components/DemoChat';
import { 
  DollarSign, 
  Quote, 
  TrendingUp, 
  Clock,
  Package,
  Users,
  MapPin,
  Calendar
} from 'lucide-react';
import { formatCurrency } from '@/lib/utils';
import { dashboardApi, DashboardKPI, RecentActivity, UpcomingDeadline } from '@/lib/api';
import { useQuery } from '@tanstack/react-query';

const DashboardPage = () => {
  // Fetch data from Django API
  const { data: kpiData, isLoading: kpiLoading } = useQuery<DashboardKPI>({
    queryKey: ['dashboard-kpis'],
    queryFn: () => dashboardApi.getKPIs(),
  });

  const { data: recentActivity, isLoading: activityLoading } = useQuery<RecentActivity[]>({
    queryKey: ['dashboard-activity'],
    queryFn: () => dashboardApi.getRecentActivity(),
  });

  const { data: upcomingDeadlines, isLoading: deadlinesLoading } = useQuery<UpcomingDeadline[]>({
    queryKey: ['dashboard-deadlines'],
    queryFn: () => dashboardApi.getUpcomingDeadlines(),
  });

  // Use API data or fallback to defaults
  const kpis = [
    {
      title: 'Cost Savings',
      value: kpiData ? formatCurrency(kpiData.saved_cost) : formatCurrency(285000),
      change: '+12.5%',
      changeType: 'positive' as const,
      icon: DollarSign,
      description: 'Total savings this quarter'
    },
    {
      title: 'Active Quotes',
      value: kpiData ? kpiData.quotes_in_flight.toString() : '24',
      change: '+8',
      changeType: 'positive' as const,
      icon: Quote,
      description: 'Quotes awaiting response'
    },
    {
      title: 'On-Time Rate',
      value: kpiData ? `${kpiData.on_time_rate}%` : '94.2%',
      change: '+2.1%',
      changeType: 'positive' as const,
      icon: TrendingUp,
      description: 'Delivery performance'
    },
    {
      title: 'Avg Lead Time',
      value: kpiData ? `${kpiData.avg_lead_time} days` : '18 days',
      change: '-3 days',
      changeType: 'positive' as const,
      icon: Clock,
      description: 'Average production time'
    }
  ];

  // Use API data or fallback to mock data
  const activityData = recentActivity || [
    {
      id: 1,
      type: 'quote_received',
      title: 'New quote received',
      description: 'Shenzhen Tech Cases submitted quote for phone cases',
      time: '2 minutes ago',
      icon: 'Quote',
      color: 'text-blue-400'
    },
    {
      id: 2,
      type: 'rfq_created',
      title: 'RFQ published',
      description: 'Bluetooth headphones RFQ sent to 8 suppliers',
      time: '1 hour ago',
      icon: 'Package',
      color: 'text-green-400'
    },
    {
      id: 3,
      type: 'supplier_verified',
      title: 'Supplier verified',
      description: 'Premium Cases Co completed verification process',
      time: '3 hours ago',
      icon: 'Users',
      color: 'text-purple-400'
    },
    {
      id: 4,
      type: 'shipment_update',
      title: 'Shipment departed',
      description: 'Order #1847 left Shenzhen Port',
      time: '5 hours ago',
      icon: 'MapPin',
      color: 'text-yellow-400'
    }
  ];

  const deadlinesData = upcomingDeadlines || [
    {
      id: 1,
      title: 'Phone Cases RFQ',
      deadline: '2024-12-15',
      status: 'urgent',
      responses: 12
    },
    {
      id: 2,
      title: 'Bluetooth Headphones',
      deadline: '2024-12-20',
      status: 'normal',
      responses: 8
    },
    {
      id: 3,
      title: 'Laptop Stands',
      deadline: '2024-12-25',
      status: 'normal',
      responses: 5
    }
  ];

  const isLoading = kpiLoading || activityLoading || deadlinesLoading;

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-accent-gradient-from"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold text-text-primary">Dashboard</h1>
        <p className="text-text-secondary">
          Welcome back! Here's what's happening with your sourcing operations.
        </p>
      </motion.div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {kpis.map((kpi, index) => (
          <motion.div
            key={kpi.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            <Card className="hover:shadow-xl transition-all duration-300">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-text-secondary">
                  {kpi.title}
                </CardTitle>
                <kpi.icon className="h-4 w-4 text-text-accent" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-text-primary">{kpi.value}</div>
                <div className="flex items-center space-x-2 text-xs">
                  <span className={`font-medium ${
                    kpi.changeType === 'positive' ? 'text-success' : 'text-danger'
                  }`}>
                    {kpi.change}
                  </span>
                  <span className="text-text-secondary">from last month</span>
                </div>
                <p className="text-xs text-text-secondary mt-1">{kpi.description}</p>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Main Content Grid */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Recent Activity */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="lg:col-span-2"
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Clock className="w-5 h-5 text-text-accent" />
                <span>Recent Activity</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {activityData.map((activity) => (
                <div key={activity.id} className="flex items-start space-x-3 p-3 rounded-lg hover:bg-surface-glass transition-colors">
                  <div className={`w-8 h-8 rounded-full bg-surface-glass flex items-center justify-center ${activity.color}`}>
                    <activity.icon className="w-4 h-4" />
                  </div>
                  <div className="flex-1">
                    <h4 className="font-medium text-text-primary">{activity.title}</h4>
                    <p className="text-sm text-text-secondary">{activity.description}</p>
                    <p className="text-xs text-text-secondary mt-1">{activity.time}</p>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </motion.div>

        {/* Quick Chat */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          <Card>
            <CardHeader>
              <CardTitle>Quick Chat</CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <DemoChat mode="app" className="h-80" />
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Upcoming Deadlines */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.4 }}
      >
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Calendar className="w-5 h-5 text-text-accent" />
              <span>Upcoming RFQ Deadlines</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {deadlinesData.map((deadline) => (
                <div key={deadline.id} className="flex items-center justify-between p-3 rounded-lg glass-effect">
                  <div>
                    <h4 className="font-medium text-text-primary">{deadline.title}</h4>
                    <p className="text-sm text-text-secondary">{deadline.responses} responses received</p>
                  </div>
                  <div className="text-right">
                    <Badge 
                      variant={deadline.status === 'urgent' ? 'destructive' : 'secondary'}
                      className="mb-1"
                    >
                      {deadline.status}
                    </Badge>
                    <p className="text-sm text-text-secondary">{deadline.deadline}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
};

export default DashboardPage;