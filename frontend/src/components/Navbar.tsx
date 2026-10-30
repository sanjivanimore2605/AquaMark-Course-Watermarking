import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  ShieldCheck, 
  FileText, 
  SearchCheck, 
  Cpu, 
  LayoutDashboard, 
  LogOut, 
  User as UserIcon,
  Layers
} from 'lucide-react';

export const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const navLinkClass = (path: string) => {
    const active = location.pathname === path;
    return `text-sm font-medium transition-colors ${
      active ? 'text-teal-400 font-semibold' : 'text-slate-300 hover:text-white'
    }`;
  };

  return (
    <nav className="border-b border-slate-800 bg-slate-950/80 backdrop-blur sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <Link to="/" className="flex items-center space-x-3">
            <div className="p-2 bg-gradient-to-tr from-teal-500 to-cyan-400 rounded-lg shadow-md shadow-cyan-500/20">
              <ShieldCheck className="w-6 h-6 text-slate-950" />
            </div>
            <div>
              <span className="text-xl font-bold tracking-tight text-white">AquaMark</span>
              <span className="hidden sm:inline-block ml-2 text-xs font-mono px-2 py-0.5 rounded bg-teal-950 text-teal-400 border border-teal-800">
                v1.0 Ed25519
              </span>
            </div>
          </Link>

          <div className="hidden md:flex items-center space-x-6">
            <Link to="/" className={navLinkClass('/')}>Overview</Link>
            <Link to="/verify" className={navLinkClass('/verify')}>Verify Document</Link>
            <Link to="/about" className={navLinkClass('/about')}>Security & Specs</Link>
            
            {user ? (
              <>
                <Link to="/dashboard" className={navLinkClass('/dashboard')}>
                  <span className="flex items-center gap-1.5">
                    <LayoutDashboard className="w-4 h-4" /> Dashboard
                  </span>
                </Link>
                <Link to="/documents" className={navLinkClass('/documents')}>
                  <span className="flex items-center gap-1.5">
                    <FileText className="w-4 h-4" /> Documents
                  </span>
                </Link>
                <Link to="/lab" className={navLinkClass('/lab')}>
                  <span className="flex items-center gap-1.5">
                    <Cpu className="w-4 h-4" /> Robustness Lab
                  </span>
                </Link>
              </>
            ) : null}
          </div>

          <div className="flex items-center space-x-4">
            {user ? (
              <div className="flex items-center space-x-4">
                <div className="hidden sm:flex flex-col text-right">
                  <span className="text-xs font-medium text-slate-200">{user.full_name || user.email}</span>
                  <span className="text-[10px] text-teal-400 capitalize">{user.role}</span>
                </div>
                <button
                  onClick={handleLogout}
                  className="p-2 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-slate-800 transition"
                  title="Logout"
                >
                  <LogOut className="w-5 h-5" />
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-3">
                <Link
                  to="/login"
                  className="text-sm font-medium text-slate-300 hover:text-white px-3 py-1.5 rounded transition"
                >
                  Sign In
                </Link>
                <Link
                  to="/register"
                  className="text-sm font-medium bg-teal-500 hover:bg-teal-400 text-slate-950 px-4 py-1.5 rounded-lg font-semibold transition shadow-sm shadow-teal-500/20"
                >
                  Get Started
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};
