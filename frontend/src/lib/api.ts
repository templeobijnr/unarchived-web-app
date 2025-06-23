// API service for communicating with Django backend
const API_BASE_URL = 'http://127.0.0.1:8000/api';

// Types matching the Django backend models
export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

export interface Supplier {
  id: number;
  name: string;
  logo: string;
  category: string;
  reliability: number;
  region: string;
  capabilities: string[];
  certifications: string[];
  contact_email: string;
  contact_phone: string;
  contact_address: string;
  created_at: string;
  updated_at: string;
}

export interface RFQ {
  id: number;
  title: string;
  description: string;
  category: string;
  quantity: number;
  target_price: string;
  currency: string;
  deadline: string;
  status: 'draft' | 'published' | 'closed';
  responses: number;
  created_by: User;
  created_at: string;
  updated_at: string;
}

export interface Quote {
  id: number;
  rfq: number;
  supplier: Supplier;
  product: string;
  price: string;
  currency: string;
  lead_time: number;
  moq: number;
  status: 'pending' | 'accepted' | 'rejected' | 'expired';
  specs: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface Message {
  id: number;
  author: 'user' | 'ai';
  content: string;
  timestamp: string;
  typing: boolean;
  user: User;
}

export interface KPI {
  id: number;
  saved_cost: string;
  quotes_in_flight: number;
  on_time_rate: string;
  total_orders: number;
  active_suppliers: number;
  avg_lead_time: number;
  user: User;
  created_at: string;
  updated_at: string;
}

export interface DashboardKPI {
  saved_cost: number;
  quotes_in_flight: number;
  on_time_rate: number;
  avg_lead_time: number;
}

export interface RecentActivity {
  id: number;
  type: string;
  title: string;
  description: string;
  time: string;
  icon: string;
  color: string;
}

export interface UpcomingDeadline {
  id: number;
  title: string;
  deadline: string;
  type: string;
  status: string;
}

// API response types
interface ApiResponse<T> {
  count?: number;
  next?: string;
  previous?: string;
  results?: T[];
}

// Helper function for API calls
async function apiCall<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    credentials: 'include', // Include cookies for session authentication
  };

  const response = await fetch(url, { ...defaultOptions, ...options });
  
  if (!response.ok) {
    throw new Error(`API call failed: ${response.status} ${response.statusText}`);
  }
  
  return response.json();
}

// API Functions
class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      credentials: 'include',
      ...options,
    };

    const response = await fetch(url, config);
    
    if (!response.ok) {
      throw new Error(`API request failed: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  // Authentication
  async login(username: string, password: string): Promise<{ user: User }> {
    return this.request('/auth/session/login/', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
  }

  async logout(): Promise<void> {
    return this.request('/auth/session/logout/', {
      method: 'POST',
    });
  }

  async getCurrentUser(): Promise<User> {
    return this.request('/auth/session/user/');
  }

  // Suppliers
  async getSuppliers(params?: {
    search?: string;
    category?: string;
  }): Promise<Supplier[]> {
    const searchParams = new URLSearchParams();
    if (params?.search) searchParams.append('search', params.search);
    if (params?.category) searchParams.append('category', params.category);
    
    const query = searchParams.toString();
    return this.request(`/suppliers/${query ? `?${query}` : ''}`);
  }

  async getSupplier(id: number): Promise<Supplier> {
    return this.request(`/suppliers/${id}/`);
  }

  async getSupplierQuotes(id: number): Promise<Quote[]> {
    return this.request(`/suppliers/${id}/quotes/`);
  }

  // RFQs
  async getRFQs(): Promise<RFQ[]> {
    return this.request('/rfqs/');
  }

  async getRFQ(id: number): Promise<RFQ> {
    return this.request(`/rfqs/${id}/`);
  }

  async createRFQ(data: Partial<RFQ>): Promise<RFQ> {
    return this.request('/rfqs/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getRFQQuotes(id: number): Promise<Quote[]> {
    return this.request(`/rfqs/${id}/quotes/`);
  }

  // Quotes
  async getQuotes(params?: {
    search?: string;
    status?: string;
  }): Promise<Quote[]> {
    const searchParams = new URLSearchParams();
    if (params?.search) searchParams.append('search', params.search);
    if (params?.status) searchParams.append('status', params.status);
    
    const query = searchParams.toString();
    return this.request(`/quotes/${query ? `?${query}` : ''}`);
  }

  async getQuote(id: number): Promise<Quote> {
    return this.request(`/quotes/${id}/`);
  }

  async updateQuote(id: number, data: Partial<Quote>): Promise<Quote> {
    return this.request(`/quotes/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }

  // Messages (AI Chat)
  async getMessages(): Promise<Message[]> {
    return this.request('/messages/');
  }

  async sendMessage(content: string): Promise<{ message: string; conversation: Message[] }> {
    return this.request('/messages/send_message/', {
      method: 'POST',
      body: JSON.stringify({ content }),
    });
  }

  async createRFQFromChat(currentMessage: string): Promise<{ message: string; rfq: RFQ }> {
    return this.request('/messages/create_rfq/', {
      method: 'POST',
      body: JSON.stringify({ current_message: currentMessage }),
    });
  }

  // Dashboard
  async getDashboardKPIs(): Promise<DashboardKPI> {
    return this.request('/dashboard/kpis/');
  }

  async getRecentActivity(): Promise<RecentActivity[]> {
    return this.request('/dashboard/recent_activity/');
  }

  async getUpcomingDeadlines(): Promise<UpcomingDeadline[]> {
    return this.request('/dashboard/upcoming_deadlines/');
  }

  // KPIs
  async getKPIs(): Promise<KPI[]> {
    return this.request('/kpis/');
  }

  async createKPI(data: Partial<KPI>): Promise<KPI> {
    return this.request('/kpis/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
}

export const api = new ApiService(API_BASE_URL);

// Export specific API instances for different modules
export const authApi = {
  login: (username: string, password: string) => api.login(username, password),
  logout: () => api.logout(),
  getCurrentUser: () => api.getCurrentUser(),
  register: async (username: string, email: string, password: string) => {
    const response = await fetch(`${API_BASE_URL}/auth/register/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify({ username, email, password }),
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Registration failed');
    }
    
    return response.json();
  },
  checkAuth: async () => {
    try {
      const user = await api.getCurrentUser();
      return { isAuthenticated: true, user };
    } catch (error) {
      return { isAuthenticated: false, user: null };
    }
  },
};

export const supplierApi = {
  getSuppliers: (params?: { search?: string; category?: string }) => api.getSuppliers(params),
  getSupplier: (id: number) => api.getSupplier(id),
  getSupplierQuotes: (id: number) => api.getSupplierQuotes(id),
};

export const quoteApi = {
  getQuotes: (params?: { search?: string; status?: string }) => api.getQuotes(params),
  getQuote: (id: number) => api.getQuote(id),
  updateQuote: (id: number, data: Partial<Quote>) => api.updateQuote(id, data),
};

export const dashboardApi = {
  getKPIs: () => api.getDashboardKPIs(),
  getRecentActivity: () => api.getRecentActivity(),
  getUpcomingDeadlines: () => api.getUpcomingDeadlines(),
};

export const rfqApi = {
  getRFQs: () => api.getRFQs(),
  getRFQ: (id: number) => api.getRFQ(id),
  createRFQ: (data: Partial<RFQ>) => api.createRFQ(data),
  getRFQQuotes: (id: number) => api.getRFQQuotes(id),
};

export const messageApi = {
  getMessages: () => api.getMessages(),
  sendMessage: (content: string) => api.sendMessage(content),
  createRFQFromChat: (currentMessage: string) => api.createRFQFromChat(currentMessage),
}; 