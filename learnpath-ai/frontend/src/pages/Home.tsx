import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Brain, Zap, Target } from 'lucide-react';
import { AppLayout } from '../components/layout/AppLayout';
import { Button } from '../components/ui/Button';
import './Home.css';

export const Home: React.FC = () => {
  return (
    <AppLayout>
      <section className="hero-section text-center">
        <div className="container">
          <h1 className="hero-title">
            Unlock Your Potential with <span className="text-gradient">AI-Powered</span> Learning Paths
          </h1>
          <p className="hero-subtitle text-muted mb-8 max-w-2xl mx-auto">
            Tell us your goals, experience, and domain. We'll craft a hyper-personalized roadmap to take your skills to the next level.
          </p>
          <Link to="/generate">
            <Button size="lg" className="hero-cta">
              Get Started <ArrowRight className="ml-2 w-5 h-5" />
            </Button>
          </Link>
        </div>
      </section>

      <section className="features-section">
        <div className="container">
          <div className="grid md:grid-cols-3 gap-8">
            <div className="feature-card">
              <div className="feature-icon-wrapper text-primary mb-4">
                <Brain className="w-8 h-8" />
              </div>
              <h3 className="feature-title">Smart Skill Gap Analysis</h3>
              <p className="feature-desc text-muted">
                Our AI analyzes your current skills to identify exactly what you need to learn.
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon-wrapper text-primary mb-4">
                <Target className="w-8 h-8" />
              </div>
              <h3 className="feature-title">Goal-Oriented Phases</h3>
              <p className="feature-desc text-muted">
                Structured learning phases customized to help you hit your career objectives faster.
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon-wrapper text-primary mb-4">
                <Zap className="w-8 h-8" />
              </div>
              <h3 className="feature-title">Actionable Projects</h3>
              <p className="feature-desc text-muted">
                Every learning phase comes with a hands-on project to validate your understanding.
              </p>
            </div>
          </div>
        </div>
      </section>
    </AppLayout>
  );
};
