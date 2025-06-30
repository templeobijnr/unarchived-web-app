import { useState } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { 
  User, 
  Building, 
  CreditCard, 
  Key, 
  Bell, 
  Shield,
  Globe,
  Copy,
  Plus,
  Trash2,
  ExternalLink
} from 'lucide-react';

const SettingsPage = () => {
  const [activeTab, setActiveTab] = useState('profile');
  const [apiKeys, setApiKeys] = useState([
    { id: '1', name: 'Production API', key: 'una_live_*********************xyz', created: '2024-11-15', lastUsed: '2024-11-20' },
    { id: '2', name: 'Development API', key: 'una_test_*********************abc', created: '2024-11-10', lastUsed: '2024-11-19' }
  ]);

  const tabs = [
    { id: 'profile', label: 'Profile', icon: User },
    { id: 'organization', label: 'Organization', icon: Building },
    { id: 'billing', label: 'Billing', icon: CreditCard },
    { id: 'api', label: 'API Keys', icon: Key },
    { id: 'notifications', label: 'Notifications', icon: Bell },
    { id: 'security', label: 'Security', icon: Shield }
  ];

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    // Could add toast notification here
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case 'profile':
        return (
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Personal Information</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-text-primary mb-2">First Name</label>
                    <Input defaultValue="John" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-text-primary mb-2">Last Name</label>
                    <Input defaultValue="Doe" />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-primary mb-2">Email</label>
                  <Input type="email" defaultValue="john@company.com" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-primary mb-2">Phone</label>
                  <Input type="tel" defaultValue="+1 (555) 123-4567" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-primary mb-2">Job Title</label>
                  <Input defaultValue="Procurement Manager" />
                </div>
                <Button>Update Profile</Button>
              </CardContent>
            </Card>
          </div>
        );

      case 'organization':
        return (
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Company Details</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-text-primary mb-2">Company Name</label>
                  <Input defaultValue="Tech Corp" />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-text-primary mb-2">Industry</label>
                    <select className="w-full bg-surface-glass border border-surface-border rounded-md px-3 py-2 text-text-primary">
                      <option>Technology</option>
                      <option>Manufacturing</option>
                      <option>Retail</option>
                      <option>Healthcare</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-text-primary mb-2">Company Size</label>
                    <select className="w-full bg-surface-glass border border-surface-border rounded-md px-3 py-2 text-text-primary">
                      <option>1-10 employees</option>
                      <option>11-50 employees</option>
                      <option>51-200 employees</option>
                      <option>200+ employees</option>
                    </select>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-primary mb-2">Address</label>
                  <Input defaultValue="123 Business Ave, San Francisco, CA 94102" />
                </div>
                <Button>Update Organization</Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Default Settings</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-text-primary mb-2">Default Currency</label>
                    <select className="w-full bg-surface-glass border border-surface-border rounded-md px-3 py-2 text-text-primary">
                      <option>USD</option>
                      <option>EUR</option>
                      <option>GBP</option>
                      <option>CNY</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-text-primary mb-2">Default Incoterm</label>
                    <select className="w-full bg-surface-glass border border-surface-border rounded-md px-3 py-2 text-text-primary">
                      <option>FOB</option>
                      <option>CIF</option>
                      <option>EXW</option>
                      <option>DDP</option>
                    </select>
                  </div>
                </div>
                <Button>Save Defaults</Button>
              </CardContent>
            </Card>
          </div>
        );

      case 'billing':
        return (
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Current Plan</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-semibold text-text-primary">Professional Plan</h3>
                    <p className="text-text-secondary">$99/month • Billed monthly</p>
                  </div>
                  <Badge variant="success">Active</Badge>
                </div>
                <Separator className="my-4" />
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-text-secondary">RFQs per month</span>
                    <span className="text-text-primary">50 / Unlimited</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-text-secondary">Supplier connections</span>
                    <span className="text-text-primary">150 / Unlimited</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-text-secondary">Next billing date</span>
                    <span className="text-text-primary">December 15, 2024</span>
                  </div>
                </div>
                <div className="mt-4 flex space-x-3">
                  <Button variant="outline">Change Plan</Button>
                  <Button variant="outline">
                    <ExternalLink className="w-4 h-4 mr-2" />
                    Billing Portal
                  </Button>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Payment Method</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-8 bg-gradient-accent rounded flex items-center justify-center">
                    <CreditCard className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <p className="font-medium text-text-primary">•••• •••• •••• 4242</p>
                    <p className="text-sm text-text-secondary">Expires 12/2027</p>
                  </div>
                </div>
                <Button variant="outline" className="mt-4">Update Payment Method</Button>
              </CardContent>
            </Card>
          </div>
        );

      case 'api':
        return (
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  API Keys
                  <Button size="sm">
                    <Plus className="w-4 h-4 mr-2" />
                    New Key
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {apiKeys.map((key) => (
                    <div key={key.id} className="p-4 glass-effect rounded-lg">
                      <div className="flex items-center justify-between">
                        <div>
                          <h4 className="font-medium text-text-primary">{key.name}</h4>
                          <p className="text-sm text-text-secondary">Created {key.created}</p>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => copyToClipboard(key.key)}
                          >
                            <Copy className="w-4 h-4" />
                          </Button>
                          <Button variant="ghost" size="icon">
                            <Trash2 className="w-4 h-4 text-danger" />
                          </Button>
                        </div>
                      </div>
                      <div className="mt-2">
                        <code className="text-xs bg-surface-glass px-2 py-1 rounded text-text-primary">
                          {key.key}
                        </code>
                      </div>
                      <p className="text-xs text-text-secondary mt-1">Last used: {key.lastUsed}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>API Documentation</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-text-secondary mb-4">
                  Integrate Unarchived into your existing workflow with our comprehensive API.
                </p>
                <Button variant="outline">
                  <ExternalLink className="w-4 h-4 mr-2" />
                  View Documentation
                </Button>
              </CardContent>
            </Card>
          </div>
        );

      case 'notifications':
        return (
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Email Notifications</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {[
                  { label: 'New quotes received', description: 'When suppliers respond to your RFQs' },
                  { label: 'Payment milestones', description: 'Escrow payment updates and reminders' },
                  { label: 'Shipment updates', description: 'Tracking and delivery notifications' },
                  { label: 'Weekly summaries', description: 'Summary of your sourcing activity' },
                  { label: 'Security alerts', description: 'Login attempts and security events' }
                ].map((notification) => (
                  <div key={notification.label} className="flex items-center justify-between">
                    <div>
                      <p className="font-medium text-text-primary">{notification.label}</p>
                      <p className="text-sm text-text-secondary">{notification.description}</p>
                    </div>
                    <input type="checkbox" defaultChecked className="rounded border-surface-border" />
                  </div>
                ))}
                <Button>Save Preferences</Button>
              </CardContent>
            </Card>
          </div>
        );

      case 'security':
        return (
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Password</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-text-primary mb-2">Current Password</label>
                  <Input type="password" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-primary mb-2">New Password</label>
                  <Input type="password" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-primary mb-2">Confirm New Password</label>
                  <Input type="password" />
                </div>
                <Button>Update Password</Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Two-Factor Authentication</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium text-text-primary">SMS Authentication</p>
                    <p className="text-sm text-text-secondary">Receive codes via SMS</p>
                  </div>
                  <Badge variant="secondary">Disabled</Badge>
                </div>
                <Button variant="outline" className="mt-4">Enable 2FA</Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Active Sessions</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {[
                    { device: 'Chrome on MacBook Pro', location: 'San Francisco, CA', current: true },
                    { device: 'Safari on iPhone', location: 'San Francisco, CA', current: false },
                    { device: 'Chrome on Windows', location: 'New York, NY', current: false }
                  ].map((session, index) => (
                    <div key={index} className="flex items-center justify-between p-3 glass-effect rounded-lg">
                      <div>
                        <p className="font-medium text-text-primary">{session.device}</p>
                        <p className="text-sm text-text-secondary">{session.location}</p>
                      </div>
                      <div className="flex items-center space-x-2">
                        {session.current && <Badge variant="success">Current</Badge>}
                        {!session.current && <Button variant="outline" size="sm">Revoke</Button>}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold text-text-primary">Settings</h1>
        <p className="text-text-secondary">
          Manage your account preferences and organization settings
        </p>
      </motion.div>

      <div className="flex gap-6">
        {/* Sidebar Navigation */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="w-64 shrink-0"
        >
          <Card>
            <CardContent className="p-0">
              <nav className="space-y-1">
                {tabs.map((tab) => {
                  const Icon = tab.icon;
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`w-full flex items-center space-x-3 px-4 py-3 text-left transition-colors ${
                        activeTab === tab.id
                          ? 'bg-gradient-accent text-white'
                          : 'text-text-secondary hover:text-text-primary hover:bg-surface-glass'
                      }`}
                    >
                      <Icon className="w-5 h-5" />
                      <span>{tab.label}</span>
                    </button>
                  );
                })}
              </nav>
            </CardContent>
          </Card>
        </motion.div>

        {/* Main Content */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="flex-1"
        >
          {renderTabContent()}
        </motion.div>
      </div>
    </div>
  );
};

export default SettingsPage;