import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { Home } from './pages/Home';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Dashboard } from './pages/Dashboard';
import { Documents } from './pages/Documents';
import { Verify } from './pages/Verify';
import { Lab } from './pages/Lab';
import { About } from './pages/About';

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, isLoading } = useAuth();
  if (isLoading) return <div className="text-center p-12 text-slate-400">Verifying session...</div>;
  if (!user) return <Navigate to="/login" replace />;
  return <>{children}</>;
};

export const App: React.FC = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-teal-500 selection:text-slate-950">
          <Navbar />
          <main className="flex-1">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/verify" element={<Verify />} />
              <Route path="/about" element={<About />} />
              
              {/* Authenticated Routes */}
              <Route 
                path="/dashboard" 
                element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/documents" 
                element={
                  <ProtectedRoute>
                    <Documents />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/lab" 
                element={
                  <ProtectedRoute>
                    <Lab />
                  </ProtectedRoute>
                } 
              />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
          
          <footer className="border-t border-slate-900 bg-slate-950 py-8 text-center text-xs text-slate-500">
            <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
              <div>
                <strong>AquaMark</strong> — Secure Digital Watermarking & Document Integrity Platform
              </div>
              <div className="font-mono text-[11px]">
                Ed25519 • SHA-256 • DCT-MidFreq • Argon2id
              </div>
            </div>
          </footer>
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
