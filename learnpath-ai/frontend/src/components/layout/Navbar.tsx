import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Sparkles, PlusCircle, LayoutDashboard, LogOut } from 'lucide-react';
import { auth } from '../../utils/auth';
import './Navbar.css';

export const Navbar: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const isAuthenticated = auth.isAuthenticated();

  const handleLogout = () => {
    auth.clearUser();
    navigate('/');
  };

  return (
    <header className="navbar">
      <div className="container navbar-container">
        <Link to="/" className="navbar-brand">
          <div className="navbar-logo-badge">
            <Sparkles className="navbar-logo-icon" />
          </div>
          <div className="flex flex-col">
            <span className="navbar-title">
              LearnPath <span className="navbar-title-ai">AI</span>
            </span>
            <span className="navbar-tagline">by Team techQ</span>
          </div>
        </Link>

        <nav className="navbar-nav">
          <Link to="/" className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}>
            Home
          </Link>
          {isAuthenticated && (
            <Link 
              to="/dashboard" 
              className={`nav-link ${location.pathname === '/dashboard' ? 'active' : ''}`}
            >
              <LayoutDashboard className="w-4 h-4 mr-1 inline" />
              Dashboard
            </Link>
          )}

          {isAuthenticated ? (
            <div className="flex items-center gap-3">
              <Link 
                to="/generate" 
                className="nav-link nav-link-cta"
              >
                <PlusCircle className="w-4 h-4 mr-1.5 inline" />
                New Path
              </Link>
              <button
                onClick={handleLogout}
                className="nav-link nav-link-logout"
                title="Logout"
              >
                <LogOut className="w-4 h-4 mr-1 inline" />
                Logout
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-3">
              <Link
                to="/sign-in"
                className="nav-auth-signin-btn"
              >
                Sign In
              </Link>
              <Link
                to="/sign-up"
                className="nav-auth-signup-btn"
              >
                Sign Up
              </Link>
            </div>
          )}
        </nav>
      </div>
    </header>
  );
};
