import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  LayoutDashboard, 
  Quote, 
  Users, 
  MessageSquare, 
  Settings, 
  Menu,
  X,
  Bell,
  ChevronDown,
  Globe,
  LogOut
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { 
  DropdownMenu, 
  DropdownMenuContent, 
  DropdownMenuItem, 
  DropdownMenuSeparator, 
  DropdownMenuTrigger 
} from '@/components/ui/dropdown-menu';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

interface AppLayoutProps {
  children: React.ReactNode;
}

const AppLayout = ({ children }: AppLayoutProps) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const location = useLocation();

  const navigation = [
    { name: 'Dashboard', href: '/app/dashboard', icon: LayoutDashboard },
    { name: 'Quotes', href: '/app/quotes', icon: Quote },
    { name: 'Suppliers', href: '/app/suppliers', icon: Users },
    { name: 'Chat', href: '/app/chat', icon: MessageSquare },
    { name: 'Settings', href: '/app/settings', icon: Settings },
  ];

  const isActive = (path: string) => location.pathname === path;

  const user = {
    name: 'John Doe',
    email: 'john@company.com',
    company: 'Tech Corp',
    avatar: 'https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&w=100&h=100&fit=crop'
  };

  return (
    <div className="h-screen flex bg-gradient-main">
      {/* Sidebar */}
      <motion.div
        className={cn(
          'relative flex flex-col glass-effect border-r border-surface-border',
          sidebarOpen ? 'w-64' : 'w-16'
        )}
        animate={{ width: sidebarOpen ? 256 : 64 }}
        transition={{ duration: 0.3, ease: 'easeInOut' }}
      >
        {/* Sidebar Header */}
        <div className="flex items-center justify-between p-4 border-b border-surface-border">
          <Link to="/app/dashboard" className="flex items-center space-x-2">
            <div className="relative">
              <Globe className="h-8 w-8 text-accent-gradient-from" />
              <div className="absolute -inset-1 bg-gradient-accent rounded-full opacity-20 blur" />
            </div>
            {sidebarOpen && (
              <span className="text-xl font-bold gradient-text">Unarchived</span>
            )}
          </Link>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="shrink-0"
          >
            {sidebarOpen ? <X className="h-4 w-4" /> : <Menu className="h-4 w-4" />}
          </Button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-2">
          {navigation.map((item) => (
            <Link
              key={item.name}
              to={item.href}
              className={cn(
                'flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 group relative',
                isActive(item.href)
                  ? 'bg-gradient-accent text-white shadow-lg'
                  : 'text-text-secondary hover:text-text-primary hover:bg-surface-glass'
              )}
            >
              <item.icon className={cn(
                'h-5 w-5 shrink-0',
                isActive(item.href) ? 'text-white' : 'text-text-accent'
              )} />
              {sidebarOpen && (
                <span className="truncate">{item.name}</span>
              )}
              {isActive(item.href) && (
                <motion.div
                  className="absolute left-0 top-0 bottom-0 w-1 bg-white rounded-r-full"
                  layoutId="sidebar-indicator"
                />
              )}
            </Link>
          ))}
        </nav>

        {/* User Profile */}
        {sidebarOpen && (
          <div className="p-4 border-t border-surface-border">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="w-full justify-start h-auto p-2">
                  <Avatar className="h-8 w-8 mr-3">
                    <AvatarImage src={user.avatar} alt={user.name} />
                    <AvatarFallback>{user.name.charAt(0)}</AvatarFallback>
                  </Avatar>
                  <div className="flex-1 text-left">
                    <p className="text-sm font-medium text-text-primary truncate">{user.name}</p>
                    <p className="text-xs text-text-secondary truncate">{user.company}</p>
                  </div>
                  <ChevronDown className="h-4 w-4 text-text-secondary" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56 glass-effect border-surface-border">
                <DropdownMenuItem>
                  <Settings className="mr-2 h-4 w-4" />
                  <span>Account Settings</span>
                </DropdownMenuItem>
                <DropdownMenuItem>
                  <Users className="mr-2 h-4 w-4" />
                  <span>Team Settings</span>
                </DropdownMenuItem>
                <DropdownMenuSeparator className="bg-surface-border" />
                <DropdownMenuItem className="text-danger">
                  <LogOut className="mr-2 h-4 w-4" />
                  <span>Sign Out</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        )}
      </motion.div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <header className="flex items-center justify-between p-4 glass-effect border-b border-surface-border">
          <div className="flex items-center space-x-4">
            <h1 className="text-xl font-semibold text-text-primary">
              {navigation.find(item => isActive(item.href))?.name || 'Dashboard'}
            </h1>
          </div>

          <div className="flex items-center space-x-4">
            {/* Organization Switcher */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" className="flex items-center space-x-2">
                  <span className="text-sm">{user.company}</span>
                  <ChevronDown className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="glass-effect border-surface-border">
                <DropdownMenuItem>
                  <span>Tech Corp</span>
                  <Badge variant="outline" className="ml-2">Current</Badge>
                </DropdownMenuItem>
                <DropdownMenuItem>
                  <span>Manufacturing LLC</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>

            {/* Notifications */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon" className="relative">
                  <Bell className="h-5 w-5" />
                  <Badge 
                    variant="destructive" 
                    className="absolute -top-2 -right-2 h-5 w-5 p-0 flex items-center justify-center text-xs"
                  >
                    3
                  </Badge>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-80 glass-effect border-surface-border">
                <div className="p-3 border-b border-surface-border">
                  <h4 className="font-semibold text-text-primary">Notifications</h4>
                </div>
                <div className="p-2 space-y-2">
                  <div className="p-2 rounded hover:bg-surface-glass">
                    <p className="text-sm text-text-primary font-medium">New quote received</p>
                    <p className="text-xs text-text-secondary">Shenzhen Tech Cases - $2.20 per unit</p>
                  </div>
                  <div className="p-2 rounded hover:bg-surface-glass">
                    <p className="text-sm text-text-primary font-medium">Shipment update</p>
                    <p className="text-xs text-text-secondary">Order #1847 departed from Shenzhen Port</p>
                  </div>
                </div>
              </DropdownMenuContent>
            </DropdownMenu>

            {/* User Avatar */}
            <Avatar className="h-8 w-8">
              <AvatarImage src={user.avatar} alt={user.name} />
              <AvatarFallback>{user.name.charAt(0)}</AvatarFallback>
            </Avatar>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
};

export default AppLayout;