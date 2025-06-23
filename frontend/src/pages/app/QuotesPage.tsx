import { useState } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { 
  Search, 
  Filter, 
  Download, 
  Eye,
  Clock,
  CheckCircle,
  XCircle,
  AlertCircle
} from 'lucide-react';
import QuoteMatrix from '@/components/QuoteMatrix';
import { formatCurrency, formatDate } from '@/lib/utils';
import { quoteApi, Quote } from '@/lib/api';
import { useQuery } from '@tanstack/react-query';

const QuotesPage = () => {
  const [selectedQuote, setSelectedQuote] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');

  // Fetch quotes from Django API
  const { data: quotesData, isLoading } = useQuery({
    queryKey: ['quotes', searchTerm, statusFilter],
    queryFn: () => quoteApi.getAll(searchTerm, statusFilter),
  });

  const quotes = quotesData?.results || [];

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'accepted': return <CheckCircle className="w-4 h-4 text-success" />;
      case 'rejected': return <XCircle className="w-4 h-4 text-danger" />;
      case 'expired': return <AlertCircle className="w-4 h-4 text-warning" />;
      default: return <Clock className="w-4 h-4 text-text-accent" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'accepted': return 'success';
      case 'rejected': return 'destructive';
      case 'expired': return 'warning';
      default: return 'secondary';
    }
  };

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
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold text-text-primary">Quotes</h1>
          <p className="text-text-secondary">
            Manage and compare supplier quotes
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <Button variant="outline">
            <Download className="w-4 h-4 mr-2" />
            Export
          </Button>
          <Button>
            Create RFQ
          </Button>
        </div>
      </motion.div>

      {/* Filters */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="flex items-center space-x-4"
      >
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-text-secondary" />
          <Input
            placeholder="Search quotes..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        <div className="flex items-center space-x-2">
          <Filter className="w-4 h-4 text-text-secondary" />
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="bg-surface-glass border border-surface-border rounded-md px-3 py-2 text-sm text-text-primary"
          >
            <option value="all">All Status</option>
            <option value="pending">Pending</option>
            <option value="accepted">Accepted</option>
            <option value="rejected">Rejected</option>
            <option value="expired">Expired</option>
          </select>
        </div>
      </motion.div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {[
          { label: 'Total Quotes', value: quotes.length, color: 'text-text-accent' },
          { label: 'Pending', value: quotes.filter(q => q.status === 'pending').length, color: 'text-warning' },
          { label: 'Accepted', value: quotes.filter(q => q.status === 'accepted').length, color: 'text-success' },
          { label: 'Best Price', value: quotes.length > 0 ? formatCurrency(Math.min(...quotes.map(q => q.price))) : formatCurrency(0), color: 'text-success' }
        ].map((stat, index) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 + index * 0.1 }}
          >
            <Card>
              <CardContent className="p-4">
                <div className="text-2xl font-bold text-text-primary">{stat.value}</div>
                <div className={`text-sm ${stat.color}`}>{stat.label}</div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Quotes Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        <Card>
          <CardHeader>
            <CardTitle>Quote Responses</CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="border-b border-surface-border">
                  <tr className="text-left">
                    <th className="p-4 text-text-secondary font-medium">Supplier</th>
                    <th className="p-4 text-text-secondary font-medium">Product</th>
                    <th className="p-4 text-text-secondary font-medium">Price</th>
                    <th className="p-4 text-text-secondary font-medium">Lead Time</th>
                    <th className="p-4 text-text-secondary font-medium">Status</th>
                    <th className="p-4 text-text-secondary font-medium">Created</th>
                    <th className="p-4 text-text-secondary font-medium">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {quotes.map((quote) => (
                    <tr 
                      key={quote.id} 
                      className="border-b border-surface-border hover:bg-surface-glass/50 transition-colors"
                    >
                      <td className="p-4">
                        <div className="flex items-center space-x-3">
                          <img 
                            src={quote.supplier_logo} 
                            alt={quote.supplier_name}
                            className="w-8 h-8 rounded-full object-cover"
                          />
                          <span className="font-medium text-text-primary">{quote.supplier_name}</span>
                        </div>
                      </td>
                      <td className="p-4 text-text-primary">{quote.product}</td>
                      <td className="p-4 text-text-primary font-medium">
                        {formatCurrency(quote.price, quote.currency)}
                      </td>
                      <td className="p-4 text-text-primary">{quote.lead_time} days</td>
                      <td className="p-4">
                        <Badge variant={getStatusColor(quote.status) as any} className="flex items-center space-x-1 w-fit">
                          {getStatusIcon(quote.status)}
                          <span>{quote.status}</span>
                        </Badge>
                      </td>
                      <td className="p-4 text-text-secondary">{formatDate(new Date(quote.created_at))}</td>
                      <td className="p-4">
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => setSelectedQuote(quote.id.toString())}
                        >
                          <Eye className="w-4 h-4" />
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Quote Details Drawer */}
      {selectedQuote && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4"
          onClick={() => setSelectedQuote(null)}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className="bg-surface-glass backdrop-blur-lg border border-surface-border rounded-xl p-6 max-w-4xl w-full max-h-[80vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-text-primary">Quote Comparison</h2>
              <Button variant="ghost" onClick={() => setSelectedQuote(null)}>
                <XCircle className="w-5 h-5" />
              </Button>
            </div>
            
            <QuoteMatrix 
              quotes={quotes.filter(q => q.rfq_id_read === quotes.find(mq => mq.id.toString() === selectedQuote)?.rfq_id_read)} 
              onSelectQuote={(quoteId) => {
                // Handle quote selection
                console.log('Selected quote:', quoteId);
              }}
            />
          </motion.div>
        </motion.div>
      )}
    </div>
  );
};

export default QuotesPage;