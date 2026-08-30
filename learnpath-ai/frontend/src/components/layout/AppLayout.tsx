import React, { type ReactNode } from 'react';
import { Navbar } from './Navbar';
import './AppLayout.css';

interface AppLayoutProps {
  children: ReactNode;
}

export const AppLayout: React.FC<AppLayoutProps> = ({ children }) => {
  return (
    <div className="app-layout">
      <Navbar />
      <main className="app-main">
        {children}
      </main>
      <footer className="app-footer">
        <div className="container text-center text-muted">
          <p>&copy; {new Date().getFullYear()} LearnPath AI. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};
