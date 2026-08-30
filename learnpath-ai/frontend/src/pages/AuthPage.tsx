import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { Brain, Mail, Lock, User, Loader2, ArrowRight } from 'lucide-react';
import { auth } from '../utils/auth';
import { profileService } from '../services/api';
import './AuthPage.css';

interface AuthPageProps {
  initialMode?: 'signin' | 'signup' | 'forgot';
}

export const AuthPage: React.FC<AuthPageProps> = ({ initialMode = 'signin' }) => {
  const navigate = useNavigate();
  const location = useLocation();

  // If path is /sign-up or /sign-in, adapt mode
  const currentPath = location.pathname;
  const derivedMode = currentPath.includes('sign-up') ? 'signup' : (currentPath.includes('sign-in') ? 'signin' : initialMode);

  const [mode, setMode] = useState<'signin' | 'signup' | 'forgot'>(derivedMode);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    if (auth.isAuthenticated()) {
      navigate('/dashboard');
    }
  }, [navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      if (mode === 'forgot') {
        setSuccess('Password reset instructions sent to your email.');
        setLoading(false);
        return;
      }

      const userEmail = email.trim();
      const userName = name.trim() || userEmail.split('@')[0];

      // Create or ensure learner profile exists on backend
      const profile = await profileService.createProfile({
        full_name: userName,
        email: userEmail,
        selected_domain: 'data_science',
        experience_level: 'intermediate',
        years_of_experience: 'none',
        learning_goal: 'Personalized AI Career Roadmap',
        career_goal: 'Skill Mastery',
        motivation: 'Advance technical career skills',
        current_skills: [],
        interests: [],
        preferred_learning_formats: ['mixed']
      });

      if (profile && profile.user_id) {
        auth.setCurrentUserId(profile.user_id);
        navigate('/dashboard');
      } else {
        throw new Error('Failed to create or load profile.');
      }
    } catch (err: any) {
      console.error(err);
      const detail = err.response?.data?.detail || err.message || 'Authentication failed. Please try again.';
      setError(typeof detail === 'string' ? detail : JSON.stringify(detail));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page-container">
      {/* Left Pane - Creative Showcase (2/3) */}
      <div className="auth-hero-pane">
        {/* Background Floating Geometric Rings */}
        <div className="auth-bg-circle circle-1" />
        <div className="auth-bg-circle circle-2" />
        <div className="auth-bg-circle circle-3" />
        <div className="auth-bg-circle circle-4" />

        <div className="auth-hero-content">
          {/* Logo Badge */}
          <Link to="/" className="auth-brand-badge">
            <div className="auth-logo-box">
              <Brain className="w-7 h-7 text-white" />
            </div>
            <div className="auth-brand-text">
              <div className="auth-brand-title">LearnPath AI</div>
              <div className="auth-brand-sub">Adaptive Learning Platform</div>
            </div>
          </Link>

          {/* Main Headline */}
          <h1 className="auth-hero-headline">
            Learn Smarter with <span className="text-gradient">AI</span>
          </h1>

          {/* Subtitle */}
          <p className="auth-hero-tagline">
            Personalized learning paths, diagnostic assessments, and mastery validation that adapt to you.
          </p>
        </div>
      </div>

      {/* Right Pane - Form (1/3) */}
      <div className="auth-form-pane">
        <div className="auth-form-card">
          <div className="auth-form-header">
            <h2 className="auth-form-title">
              {mode === 'signup' && 'Get Started'}
              {mode === 'signin' && 'Welcome Back'}
              {mode === 'forgot' && 'Reset Password'}
            </h2>
            <p className="auth-form-sub">
              {mode === 'signup' && 'Create your account to start learning'}
              {mode === 'signin' && 'Sign in to access your learning paths'}
              {mode === 'forgot' && 'Enter your email to reset your password'}
            </p>
          </div>

          {error && <div className="alert-error mb-4">{error}</div>}
          {success && <div className="alert-success mb-4 text-green-700 bg-green-50 p-3 rounded-lg text-sm border border-green-200">{success}</div>}

          <form onSubmit={handleSubmit}>
            {mode === 'signup' && (
              <div className="auth-input-group">
                <label className="auth-input-label">Full Name</label>
                <div className="auth-input-wrap">
                  <User className="auth-input-icon" />
                  <input
                    type="text"
                    required
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="e.g. Alex Johnson"
                    className="auth-input-field"
                  />
                </div>
              </div>
            )}

            <div className="auth-input-group">
              <label className="auth-input-label">Email</label>
              <div className="auth-input-wrap">
                <Mail className="auth-input-icon" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="alex@example.com"
                  className="auth-input-field"
                />
              </div>
            </div>

            {mode !== 'forgot' && (
              <div className="auth-input-group">
                <div className="flex justify-between items-center mb-1">
                  <label className="auth-input-label mb-0">Password</label>
                  {mode === 'signin' && (
                    <button
                      type="button"
                      onClick={() => setMode('forgot')}
                      className="text-xs text-primary hover:underline font-semibold"
                    >
                      Forgot password?
                    </button>
                  )}
                </div>
                <div className="auth-input-wrap">
                  <Lock className="auth-input-icon" />
                  <input
                    type="password"
                    required
                    minLength={6}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter your password"
                    className="auth-input-field"
                  />
                </div>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="auth-submit-btn"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin mr-2" />
                  Processing...
                </>
              ) : (
                <>
                  {mode === 'signup' && 'Create Account'}
                  {mode === 'signin' && 'Sign In'}
                  {mode === 'forgot' && 'Send Reset Link'}
                  <ArrowRight className="w-4 h-4 ml-1" />
                </>
              )}
            </button>
          </form>

          {/* Mode Switcher */}
          <div className="auth-mode-switch">
            {mode === 'forgot' ? (
              <p>
                Remember your password?
                <button
                  type="button"
                  onClick={() => setMode('signin')}
                  className="auth-mode-btn"
                >
                  Sign In
                </button>
              </p>
            ) : mode === 'signin' ? (
              <p>
                New here?
                <button
                  type="button"
                  onClick={() => setMode('signup')}
                  className="auth-mode-btn"
                >
                  Sign Up
                </button>
              </p>
            ) : (
              <p>
                Already have an account?
                <button
                  type="button"
                  onClick={() => setMode('signin')}
                  className="auth-mode-btn"
                >
                  Sign In
                </button>
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
