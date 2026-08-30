import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Sparkles, Target, Award, Compass, Layers } from 'lucide-react';
import { AppLayout } from '../components/layout/AppLayout';
import { Button } from '../components/ui/Button';
import { auth } from '../utils/auth';
import './Home.css';

export const Home: React.FC = () => {
  const isAuthenticated = auth.isAuthenticated();
  
  return (
    <AppLayout>
      {/* Ambient background glows */}
      <div className="home-ambient-glow glow-1" />
      <div className="home-ambient-glow glow-2" />

      {/* Hero Section */}
      <section className="hero-section text-center">
        <div className="container">
          <div className="hero-badge-wrapper mb-6">
            <span className="badge badge-sparkle">
              <Sparkles className="w-3.5 h-3.5 mr-1 text-primary" />
              AI-Powered Personalized Learning Roadmaps
            </span>
          </div>

          <h1 className="hero-title">
            Master Any Skill with <br />
            <span className="text-gradient">Personalized AI Roadmaps</span>
          </h1>

          <p className="hero-subtitle text-muted mb-8 max-w-2xl mx-auto">
            From diagnostic skill gap analysis to adaptive phases and hands-on projects, LearnPath AI creates your exact roadmap to career readiness.
          </p>

          <div className="hero-cta-group flex items-center justify-center gap-4 flex-wrap">
            {isAuthenticated ? (
              <Link to="/dashboard">
                <Button size="lg" className="hero-cta-btn">
                  Continue Learning <ArrowRight className="ml-2 w-5 h-5" />
                </Button>
              </Link>
            ) : (
              <Link to="/onboarding">
                <Button size="lg" className="hero-cta-btn">
                  Generate Your Learning Path <ArrowRight className="ml-2 w-5 h-5" />
                </Button>
              </Link>
            )}
            <Link to="/generate">
              <Button size="lg" variant="outline" className="hero-secondary-btn">
                <Compass className="mr-2 w-5 h-5" /> Explore Domains
              </Button>
            </Link>
          </div>

          {/* Quick Metrics Bar */}
          <div className="hero-stats-strip grid md:grid-cols-3 gap-6 max-w-4xl mx-auto mt-12">
            <div className="stat-pill">
              <div className="stat-number text-primary">15+</div>
              <div className="stat-label">Diagnostic Questions</div>
            </div>
            <div className="stat-pill">
              <div className="stat-number text-accent">100%</div>
              <div className="stat-label">Tailored to Your Goal</div>
            </div>
            <div className="stat-pill">
              <div className="stat-number text-gold">Phase-by-Phase</div>
              <div className="stat-label">Hands-on Mastery Projects</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="container">
          <div className="text-center mb-12">
            <span className="badge mb-3">HOW IT WORKS</span>
            <h2 className="section-title">Built for Real-World Competence</h2>
            <p className="text-muted max-w-2xl mx-auto">
              A structured, AI-guided journey that moves you from where you are today to where you want to be.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="feature-card">
              <div className="feature-icon-wrapper icon-purple">
                <Target className="w-6 h-6" />
              </div>
              <h3 className="feature-title">Diagnostic Skill Assessment</h3>
              <p className="feature-desc text-muted">
                Quick, adaptive evaluations identify your exact baseline without punishing guesswork.
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon-wrapper icon-pink">
                <Layers className="w-6 h-6" />
              </div>
              <h3 className="feature-title">Granular Skill Gap Analysis</h3>
              <p className="feature-desc text-muted">
                Visual breakdown of current vs. target capabilities with prioritized learning focus.
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon-wrapper icon-gold">
                <Award className="w-6 h-6" />
              </div>
              <h3 className="feature-title">Project & Mastery Milestones</h3>
              <p className="feature-desc text-muted">
                Curated tutorials, docs, and capstone deliverables to turn knowledge into proof of work.
              </p>
            </div>
          </div>
        </div>
      </section>
    </AppLayout>
  );
};
