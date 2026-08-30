import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Sparkles, PlusCircle, LayoutDashboard } from 'lucide-react';
import { auth } from '../../utils/auth';
import './Navbar.css';

export const Navbar: React.FC = () => {
  const location = useLocation();
  const isAuthenticated = auth.isAuthenticated();

  return (
    <header className="navbar">
      <div className="container navbar-container">
        <Link to="/" className="navbar-brand">
          <div className="navbar-logo-badge">
            <Sparkles className="navbar-logo-icon" />
          </div>
          <span className="navbar-title">
            LearnPath <span className="navbar-title-ai">AI</span>
          </span>
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
          <Link 
            to="/generate" 
            className="nav-link nav-link-cta"
          >
            <PlusCircle className="w-4 h-4 mr-1.5 inline" />
            New Path
          </Link>
        </nav>
      </div>
    </header>
  );
};
