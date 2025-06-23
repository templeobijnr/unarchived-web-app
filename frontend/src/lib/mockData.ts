export interface Message {
  id: string;
  author: 'user' | 'ai';
  content: string;
  timestamp: Date;
  typing?: boolean;
}

export interface Quote {
  id: string;
  rfqId: string;
  supplierId: string;
  supplierName: string;
  supplierLogo: string;
  product: string;
  price: number;
  currency: string;
  leadTime: number;
  moq: number;
  status: 'pending' | 'accepted' | 'rejected' | 'expired';
  specs: Record<string, any>;
  createdAt: Date;
}

export interface Supplier {
  id: string;
  name: string;
  logo: string;
  category: string;
  reliability: number;
  region: string;
  capabilities: string[];
  certifications: string[];
  contact: {
    email: string;
    phone: string;
    address: string;
  };
}

export interface RFQ {
  id: string;
  title: string;
  description: string;
  category: string;
  quantity: number;
  targetPrice: number;
  currency: string;
  deadline: Date;
  status: 'draft' | 'published' | 'closed';
  responses: number;
  createdAt: Date;
}

export const mockMessages: Message[] = [
  {
    id: '1',
    author: 'ai',
    content: "Hello! I'm your AI sourcing assistant. I can help you find suppliers, get quotes, and manage your global sourcing needs. What would you like to source today?",
    timestamp: new Date(Date.now() - 300000)
  },
  {
    id: '2',
    author: 'user',
    content: "I need to source 10,000 custom phone cases with our logo printed on them.",
    timestamp: new Date(Date.now() - 240000)
  },
  {
    id: '3',
    author: 'ai',
    content: "Perfect! I can help you source custom phone cases. Let me gather some details:\n\n📱 **Phone Models**: Which phone models do you need cases for?\n🎨 **Design**: Do you have logo files ready? What printing method do you prefer?\n📦 **Timeline**: When do you need them delivered?\n💰 **Budget**: What's your target price per unit?",
    timestamp: new Date(Date.now() - 180000)
  }
];

export const mockQuotes: Quote[] = [
  {
    id: 'q1',
    rfqId: 'rfq1',
    supplierId: 's1',
    supplierName: 'Shenzhen Tech Cases Ltd',
    supplierLogo: 'https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg?auto=compress&cs=tinysrgb&w=100&h=100&fit=crop',
    product: 'Custom Phone Cases',
    price: 2.50,
    currency: 'USD',
    leadTime: 15,
    moq: 1000,
    status: 'pending',
    specs: {
      material: 'TPU + PC',
      printing: 'UV Printing',
      packaging: 'Individual poly bags'
    },
    createdAt: new Date(Date.now() - 86400000)
  },
  {
    id: 'q2',
    rfqId: 'rfq1',
    supplierId: 's2',
    supplierName: 'Guangzhou Mobile Accessories',
    supplierLogo: 'https://images.pexels.com/photos/3184338/pexels-photo-3184338.jpeg?auto=compress&cs=tinysrgb&w=100&h=100&fit=crop',
    product: 'Custom Phone Cases',
    price: 2.20,
    currency: 'USD',
    leadTime: 20,
    moq: 500,
    status: 'pending',
    specs: {
      material: 'Silicone',
      printing: 'Screen Printing',
      packaging: 'Bulk packaging'
    },
    createdAt: new Date(Date.now() - 82800000)
  },
  {
    id: 'q3',
    rfqId: 'rfq2',
    supplierId: 's3',
    supplierName: 'Premium Cases Co',
    supplierLogo: 'https://images.pexels.com/photos/3184465/pexels-photo-3184465.jpeg?auto=compress&cs=tinysrgb&w=100&h=100&fit=crop',
    product: 'Custom Phone Cases',
    price: 3.80,
    currency: 'USD',
    leadTime: 12,
    moq: 2000,
    status: 'accepted',
    specs: {
      material: 'Premium Leather',
      printing: 'Embossing',
      packaging: 'Gift boxes'
    },
    createdAt: new Date(Date.now() - 172800000)
  }
];

export const mockSuppliers: Supplier[] = [
  {
    id: 's1',
    name: 'Shenzhen Tech Cases Ltd',
    logo: 'https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg?auto=compress&cs=tinysrgb&w=200&h=200&fit=crop',
    category: 'Electronics Accessories',
    reliability: 94,
    region: 'Shenzhen, China',
    capabilities: ['Injection Molding', 'UV Printing', 'Assembly'],
    certifications: ['ISO 9001', 'BSCI', 'RoHS'],
    contact: {
      email: 'sales@sztechcases.com',
      phone: '+86 755 8888 9999',
      address: 'Building A, Tech Park, Shenzhen, China'
    }
  },
  {
    id: 's2',
    name: 'Guangzhou Mobile Accessories',
    logo: 'https://images.pexels.com/photos/3184338/pexels-photo-3184338.jpeg?auto=compress&cs=tinysrgb&w=200&h=200&fit=crop',
    category: 'Mobile Accessories',
    reliability: 89,
    region: 'Guangzhou, China',
    capabilities: ['Screen Printing', 'Silicone Molding', 'Packaging'],
    certifications: ['ISO 14001', 'SEDEX', 'CE'],
    contact: {
      email: 'info@gzmobile.com',
      phone: '+86 20 8888 7777',
      address: 'Industrial Zone, Guangzhou, China'
    }
  },
  {
    id: 's3',
    name: 'Premium Cases Co',
    logo: 'https://images.pexels.com/photos/3184465/pexels-photo-3184465.jpeg?auto=compress&cs=tinysrgb&w=200&h=200&fit=crop',
    category: 'Luxury Accessories',
    reliability: 97,
    region: 'Hong Kong',
    capabilities: ['Leather Crafting', 'Embossing', 'Premium Packaging'],
    certifications: ['ISO 9001', 'WRAP', 'FSC'],
    contact: {
      email: 'premium@casesco.hk',
      phone: '+852 3888 6666',
      address: 'Central District, Hong Kong'
    }
  }
];

export const mockRFQs: RFQ[] = [
  {
    id: 'rfq1',
    title: 'Custom Phone Cases - 10K Units',
    description: 'Looking for custom phone cases with logo printing for iPhone 14/15 series',
    category: 'Electronics',
    quantity: 10000,
    targetPrice: 2.00,
    currency: 'USD',
    deadline: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
    status: 'published',
    responses: 12,
    createdAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000)
  },
  {
    id: 'rfq2',
    title: 'Bluetooth Headphones - 5K Units',
    description: 'Wireless earbuds with custom branding and packaging',
    category: 'Electronics',
    quantity: 5000,
    targetPrice: 15.00,
    currency: 'USD',
    deadline: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000),
    status: 'published',
    responses: 8,
    createdAt: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000)
  }
];

export const mockKPIs = {
  savedCost: 285000,
  quotesInFlight: 24,
  onTimeRate: 94.2,
  totalOrders: 156,
  activeSuppliers: 43,
  avgLeadTime: 18
};