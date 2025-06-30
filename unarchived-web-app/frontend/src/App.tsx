import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'sonner';

// Public Pages
import HomePage from '@/pages/HomePage';
import FeaturesPage from '@/pages/FeaturesPage';
import PricingPage from '@/pages/PricingPage';
import ContactPage from '@/pages/ContactPage';
import LoginPage from '@/pages/auth/LoginPage';
import SignupPage from '@/pages/auth/SignupPage';

// App Pages (Protected)
import AppLayout from '@/layouts/AppLayout';
import DashboardPage from '@/pages/app/DashboardPage';
import QuotesPage from '@/pages/app/QuotesPage';
import SuppliersPage from '@/pages/app/SuppliersPage';
import ChatPage from '@/pages/app/ChatPage';
import SettingsPage from '@/pages/app/SettingsPage';

import NavBar from '@/components/NavBar';
import { AuthProvider, useAuth } from '@/contexts/AuthContext';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      refetchOnWindowFocus: false,
    },
  },
});

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-accent-gradient-from"></div>
      </div>
    );
  }

  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />;
};

function AppContent() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-main text-foreground">
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={
            <>
              <NavBar />
              <HomePage />
            </>
          } />
          <Route path="/features" element={
            <>
              <NavBar />
              <FeaturesPage />
            </>
          } />
          <Route path="/pricing" element={
            <>
              <NavBar />
              <PricingPage />
            </>
          } />
          <Route path="/contact" element={
            <>
              <NavBar />
              <ContactPage />
            </>
          } />
          
          {/* Auth Routes */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          
          {/* Protected App Routes */}
          <Route path="/app/*" element={
            <ProtectedRoute>
              <AppLayout>
                <Routes>
                  <Route index element={<Navigate to="/app/dashboard" replace />} />
                  <Route path="dashboard" element={<DashboardPage />} />
                  <Route path="quotes" element={<QuotesPage />} />
                  <Route path="suppliers" element={<SuppliersPage />} />
                  <Route path="chat" element={<ChatPage />} />
                  <Route path="settings" element={<SettingsPage />} />
                </Routes>
              </AppLayout>
            </ProtectedRoute>
          } />
          
          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
        
        <Toaster 
          theme="dark" 
          position="top-right"
          toastOptions={{
            style: {
              background: 'rgba(255, 255, 255, 0.1)',
              backdropFilter: 'blur(10px)',
              border: '1px solid rgba(255, 255, 255, 0.2)',
              color: '#e5e7eb'
            }
          }}
        />
      </div>
    </Router>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;