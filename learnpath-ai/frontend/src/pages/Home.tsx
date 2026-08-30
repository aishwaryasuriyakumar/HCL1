import React, { useRef, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Sparkles, Target, Award, Compass, Layers, ChevronRight, Zap } from 'lucide-react';
import { AppLayout } from '../components/layout/AppLayout';
import { Button } from '../components/ui/Button';
import { auth } from '../utils/auth';
import './Home.css';

export const Home: React.FC = () => {
  const isAuthenticated = auth.isAuthenticated();
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isVideoLoaded, setIsVideoLoaded] = useState(false);

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.play().catch(err => {
        console.warn('Video auto-play prevented', err);
      });
    }
  }, []);

  return (
    <AppLayout>
      {/* Ambient background glows */}
      <div className="home-ambient-glow glow-1" />
      <div className="home-ambient-glow glow-2" />

      {/* Hero Section Container */}
      <section className="hero-container-wrap">
        <div className="hero-banner-card">
          {/* Background Poster Image (Always visible as base layer) */}
          <img
            src="/images/hero-light-beams.png"
            alt="AI Learning Platform Background"
            className="hero-media-bg hero-poster-bg"
          />

          {/* Background Animated Video (Looping subtle ambient beam particles) */}
          <video
            ref={videoRef}
            autoPlay
            loop
            muted
            playsInline
            poster="/images/hero-light-beams.png"
            onLoadedData={() => setIsVideoLoaded(true)}
            className={`hero-media-bg hero-video-bg ${isVideoLoaded ? 'loaded' : ''}`}
          >
            <source src="/videos/hero-light-beams.mp4" type="video/mp4" />
          </video>

          {/* Dark overlay for contrast */}
          <div className="hero-dark-overlay" />
          {/* Brand gradient overlay for vibrant colors */}
          <div className="hero-brand-overlay" />

          {/* Floating animated orbs for dynamic visual depth */}
          <div className="hero-orb hero-orb-1" />
          <div className="hero-orb hero-orb-2" />

          {/* Hero Content */}
          <div className="hero-content">
            <div className="hero-badge-wrapper mb-4">
              <span className="badge badge-sparkle">
                <Sparkles className="w-3.5 h-3.5 mr-1.5 text-primary" />
                AI-Powered Personalized Learning Roadmaps
              </span>
            </div>

            <h1 className="hero-title">
              Master Any Skill with <br />
              <span className="text-gradient">Personalized AI Roadmaps</span>
            </h1>

            <p className="hero-subtitle mb-8 max-w-2xl mx-auto">
              From diagnostic skill gap analysis to adaptive phases and hands-on projects, LearnPath AI creates your exact roadmap to career readiness.
            </p>

            <div className="hero-cta-group flex items-center justify-center gap-4 flex-wrap mb-10">
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

            {/* Quick Metrics Cards */}
            <div className="hero-stats-grid grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-3xl mx-auto">
              <div className="hero-stat-card">
                <div className="hero-stat-value text-white">Guided</div>
                <div className="hero-stat-label">Step-by-step milestones that keep you moving</div>
              </div>
              <div className="hero-stat-card highlight">
                <div className="hero-stat-value text-white">Personalized</div>
                <div className="hero-stat-label">Paths tailored to your exact baseline & goals</div>
              </div>
              <div className="hero-stat-card">
                <div className="hero-stat-value text-white">Hands-on</div>
                <div className="hero-stat-label">Proof-of-work projects and mastery evaluation</div>
              </div>
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
              A structured, AI-guided journey that moves you from where you are today to career readiness.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 mb-16">
            <div className="feature-card">
              <div className="feature-icon-wrapper icon-purple">
                <Target className="w-6 h-6" />
              </div>
              <h3 className="feature-title">Diagnostic Skill Assessment</h3>
              <p className="feature-desc text-muted">
                Adaptive evaluations identify your exact baseline proficiency across key domain competencies without guesswork.
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon-wrapper icon-pink">
                <Layers className="w-6 h-6" />
              </div>
              <h3 className="feature-title">Granular Skill Gap Analysis</h3>
              <p className="feature-desc text-muted">
                Visual breakdown comparing your current skills with industry target requirements, highlighting high-priority gaps.
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon-wrapper icon-gold">
                <Award className="w-6 h-6" />
              </div>
              <h3 className="feature-title">Project & Mastery Milestones</h3>
              <p className="feature-desc text-muted">
                Curated learning resources, practical coding projects, and mastery quizzes to turn knowledge into proof of work.
              </p>
            </div>
          </div>

          {/* Interactive Flow Roadmap Preview */}
          <div className="flow-preview-card">
            <div className="flow-preview-header">
              <div className="flex items-center gap-2">
                <Zap className="w-5 h-5 text-primary" />
                <h3 className="text-lg font-bold">The Continuous Learning Loop</h3>
              </div>
              <span className="text-xs text-muted font-medium">5 Integrated Stages</span>
            </div>

            <div className="flow-steps-grid">
              <div className="flow-step-item">
                <div className="flow-step-number">1</div>
                <div className="flow-step-title">Domain & Goal</div>
                <p className="flow-step-desc">Specify what you want to master and your target career role.</p>
              </div>
              <div className="flow-step-arrow"><ChevronRight className="w-5 h-5" /></div>
              <div className="flow-step-item">
                <div className="flow-step-number">2</div>
                <div className="flow-step-title">Diagnostic Quiz</div>
                <p className="flow-step-desc">Test your real knowledge across fundamental and advanced topics.</p>
              </div>
              <div className="flow-step-arrow"><ChevronRight className="w-5 h-5" /></div>
              <div className="flow-step-item">
                <div className="flow-step-number">3</div>
                <div className="flow-step-title">Skill Gap AI</div>
                <p className="flow-step-desc">Agent calculates exact gaps and prioritizes prerequisite areas.</p>
              </div>
              <div className="flow-step-arrow"><ChevronRight className="w-5 h-5" /></div>
              <div className="flow-step-item">
                <div className="flow-step-number">4</div>
                <div className="flow-step-title">Dynamic Roadmap</div>
                <p className="flow-step-desc">Multi-phase learning path with tailored deliverables and hours.</p>
              </div>
              <div className="flow-step-arrow"><ChevronRight className="w-5 h-5" /></div>
              <div className="flow-step-item">
                <div className="flow-step-number">5</div>
                <div className="flow-step-title">Mastery Unlock</div>
                <p className="flow-step-desc">Pass phase assessments with 70%+ score to unlock next stages.</p>
              </div>
            </div>
          </div>

          {/* Bottom CTA Card */}
          <div className="bottom-cta-banner mt-16">
            <div className="bottom-cta-content text-center max-w-2xl mx-auto">
              <h3 className="bottom-cta-title">
                Ready to accelerate your career?
              </h3>
              <p className="bottom-cta-desc">
                Join thousands of engineers and learners generating personalized AI learning paths today.
              </p>
              <Link to="/onboarding">
                <Button size="lg" className="hero-cta-btn bg-white text-gray-900 hover:bg-white/90">
                  Get Started Free <ArrowRight className="ml-2 w-4 h-4" />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>
    </AppLayout>
  );
};
