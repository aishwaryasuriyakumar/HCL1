import React from 'react';
import { Link } from 'react-router-dom';
import { Compass } from 'lucide-react';
import './Navbar.css';

export const Navbar: React.FC = () => {
  return (
    <header className="navbar">
      <div className="container navbar-container">
        <Link to="/" className="navbar-brand">
          <Compass className="navbar-logo-icon" />
          <span className="navbar-title">LearnPath AI</span>
        </Link>
        <nav className="navbar-nav">
          <Link to="/" className="nav-link">Home</Link>
          <Link to="/generate" className="nav-link nav-link-primary">New Path</Link>
        </nav>
      </div>
    </header>
  );
};
