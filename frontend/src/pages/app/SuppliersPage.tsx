import { useState } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { 
  Search, 
  Filter, 
  MapPin, 
  Star, 
  Award,
  Phone,
  Mail,
  Building,
  Eye,
  Plus
} from 'lucide-react';
import { supplierApi, Supplier } from '@/lib/api';
import { useQuery } from '@tanstack/react-query';

const SuppliersPage = () => {
  const [selectedSupplier, setSelectedSupplier] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState<string>('all');

  // Fetch suppliers from Django API
  const { data: suppliersData, isLoading } = useQuery({
    queryKey: ['suppliers', searchTerm, categoryFilter],
    queryFn: () => supplierApi.getAll(searchTerm, categoryFilter),
  });

  const suppliers = suppliersData?.results || [];
  const selectedSupplierData = suppliers.find(s => s.id.toString() === selectedSupplier);

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
          <h1 className="text-3xl font-bold text-text-primary">Suppliers</h1>
          <p className="text-text-secondary">
            Manage your verified supplier network
          </p>
        </div>
        <Button>
          <Plus className="w-4 h-4 mr-2" />
          Add Supplier
        </Button>
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
            placeholder="Search suppliers..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        <div className="flex items-center space-x-2">
          <Filter className="w-4 h-4 text-text-secondary" />
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="bg-surface-glass border border-surface-border rounded-md px-3 py-2 text-sm text-text-primary"
          >
            <option value="all">All Categories</option>
            <option value="Electronics Accessories">Electronics Accessories</option>
            <option value="Mobile Accessories">Mobile Accessories</option>
            <option value="Luxury Accessories">Luxury Accessories</option>
          </select>
        </div>
      </motion.div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {[
          { label: 'Total Suppliers', value: suppliers.length },
          { label: 'Verified', value: suppliers.length },
          { label: 'Avg Reliability', value: suppliers.length > 0 ? `${Math.round(suppliers.reduce((acc, s) => acc + s.reliability, 0) / suppliers.length)}%` : '0%' },
          { label: 'Countries', value: '3' }
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
                <div className="text-sm text-text-secondary">{stat.label}</div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Suppliers Grid */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="grid md:grid-cols-2 lg:grid-cols-3 gap-6"
      >
        {suppliers.map((supplier, index) => (
          <motion.div
            key={supplier.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            <Card className="hover:shadow-xl transition-all duration-300 cursor-pointer" onClick={() => setSelectedSupplier(supplier.id.toString())}>
              <CardHeader className="text-center">
                <div className="w-16 h-16 mx-auto mb-4 rounded-full overflow-hidden">
                  <img 
                    src={supplier.logo} 
                    alt={supplier.name}
                    className="w-full h-full object-cover"
                  />
                </div>
                <CardTitle className="text-lg">{supplier.name}</CardTitle>
                <div className="flex items-center justify-center space-x-1 text-sm text-text-secondary">
                  <MapPin className="w-4 h-4" />
                  <span>{supplier.region}</span>
                </div>
              </CardHeader>

              <CardContent className="space-y-4">
                <Badge variant="outline" className="w-full justify-center">
                  {supplier.category}
                </Badge>

                {/* Reliability Score */}
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-text-secondary">Reliability</span>
                    <span className="text-text-primary font-medium">{supplier.reliability}%</span>
                  </div>
                  <div className="w-full bg-surface-glass rounded-full h-2">
                    <div 
                      className="bg-gradient-accent h-2 rounded-full transition-all duration-1000"
                      style={{ width: `${supplier.reliability}%` }}
                    />
                  </div>
                </div>

                {/* Capabilities */}
                <div>
                  <p className="text-xs text-text-secondary mb-2">CAPABILITIES</p>
                  <div className="flex flex-wrap gap-1">
                    {supplier.capabilities.slice(0, 2).map((capability) => (
                      <Badge key={capability} variant="secondary" className="text-xs">
                        {capability}
                      </Badge>
                    ))}
                    {supplier.capabilities.length > 2 && (
                      <Badge variant="secondary" className="text-xs">
                        +{supplier.capabilities.length - 2} more
                      </Badge>
                    )}
                  </div>
                </div>

                {/* Certifications */}
                <div className="flex items-center space-x-2">
                  <Award className="w-4 h-4 text-text-accent" />
                  <span className="text-xs text-text-secondary">
                    {supplier.certifications.length} certifications
                  </span>
                </div>

                <Button variant="outline" className="w-full">
                  <Eye className="w-4 h-4 mr-2" />
                  View Details
                </Button>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </motion.div>

      {/* Supplier Details Modal */}
      {selectedSupplier && selectedSupplierData && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4"
          onClick={() => setSelectedSupplier(null)}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className="bg-surface-glass backdrop-blur-lg border border-surface-border rounded-xl p-6 max-w-2xl w-full max-h-[80vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-4">
                <img 
                  src={selectedSupplierData.logo} 
                  alt={selectedSupplierData.name}
                  className="w-12 h-12 rounded-full object-cover"
                />
                <div>
                  <h2 className="text-2xl font-bold text-text-primary">{selectedSupplierData.name}</h2>
                  <p className="text-text-secondary">{selectedSupplierData.category}</p>
                </div>
              </div>
              <Button variant="ghost" onClick={() => setSelectedSupplier(null)}>
                ×
              </Button>
            </div>

            <div className="space-y-6">
              {/* Contact Information */}
              <div>
                <h3 className="font-semibold text-text-primary mb-3">Contact Information</h3>
                <div className="space-y-2 text-sm">
                  <div className="flex items-center space-x-2">
                    <Mail className="w-4 h-4 text-text-accent" />
                    <span className="text-text-primary">{selectedSupplierData.contact.email}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Phone className="w-4 h-4 text-text-accent" />
                    <span className="text-text-primary">{selectedSupplierData.contact.phone}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Building className="w-4 h-4 text-text-accent" />
                    <span className="text-text-primary">{selectedSupplierData.contact.address}</span>
                  </div>
                </div>
              </div>

              {/* Capabilities */}
              <div>
                <h3 className="font-semibold text-text-primary mb-3">Capabilities</h3>
                <div className="flex flex-wrap gap-2">
                  {selectedSupplierData.capabilities.map((capability) => (
                    <Badge key={capability} variant="secondary">
                      {capability}
                    </Badge>
                  ))}
                </div>
              </div>

              {/* Certifications */}
              <div>
                <h3 className="font-semibold text-text-primary mb-3">Certifications</h3>
                <div className="flex flex-wrap gap-2">
                  {selectedSupplierData.certifications.map((certification) => (
                    <Badge key={certification} variant="outline">
                      {certification}
                    </Badge>
                  ))}
                </div>
              </div>

              {/* Reliability Score */}
              <div>
                <h3 className="font-semibold text-text-primary mb-3">Reliability Score</h3>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-text-secondary">Overall Rating</span>
                    <span className="text-text-primary font-medium">{selectedSupplierData.reliability}%</span>
                  </div>
                  <div className="w-full bg-surface-glass rounded-full h-2">
                    <div 
                      className="bg-gradient-accent h-2 rounded-full"
                      style={{ width: `${selectedSupplierData.reliability}%` }}
                    />
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </motion.div>
      )}
    </div>
  );
};

export default SuppliersPage;