import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { AppLayout } from '../components/layout/AppLayout';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Select } from '../components/ui/Select';
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '../components/ui/Card';
import { Loader } from '../components/ui/Loader';
import { profileService, domainService } from '../services/api';
import { auth } from '../utils/auth';
import type { LearnerProfileCreate, DomainInfo } from '../types/schemas';
import './Onboarding.css';

export const Onboarding: React.FC = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const [domains, setDomains] = useState<DomainInfo[]>([]);
  const [isLoadingDomains, setIsLoadingDomains] = useState(true);

  const [formData, setFormData] = useState<LearnerProfileCreate>({
    full_name: '',
    email: '',
    selected_domain: '',
    experience_level: 'beginner',
    years_of_experience: 'none',
    learning_goal: '',
    career_goal: '',
    motivation: '',
    current_skills: [],
    interests: [],
    preferred_learning_formats: []
  });

  useEffect(() => {
    const fetchDomains = async () => {
      try {
        const data = await domainService.getDomains();
        setDomains(data);
        if (data.length > 0) {
          setFormData(prev => ({ ...prev, selected_domain: data[0].id }));
        }
      } catch (err) {
        console.error('Failed to load domains', err);
        setError('Failed to load domains. Please refresh the page.');
      } finally {
        setIsLoadingDomains(false);
      }
    };
    fetchDomains();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleNext = () => setStep(prev => prev + 1);
  const handleBack = () => setStep(prev => prev - 1);

  const handleSubmit = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const profile = await profileService.createProfile(formData);
      auth.setCurrentUserId(profile.user_id);
      navigate('/assessment/intro');
    } catch (err: any) {
      console.error(err);
      let errorMessage = 'Failed to create profile. Please try again.';
      if (err.response?.data?.detail) {
        if (Array.isArray(err.response.data.detail)) {
          errorMessage = err.response.data.detail.map((d: any) => d.msg || JSON.stringify(d)).join(', ');
        } else if (typeof err.response.data.detail === 'string') {
          errorMessage = err.response.data.detail;
        }
      }
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoadingDomains) {
    return (
      <AppLayout>
        <Loader fullScreen message="Loading domains..." />
      </AppLayout>
    );
  }

  return (
    <AppLayout>
      <div className="onboarding-container container">
        <div className="onboarding-header text-center mb-8">
          <h1 className="text-3xl font-bold">Your Learning Profile</h1>
          <p className="text-muted mt-2">Step {step} of 4</p>
          <div className="progress-bar mt-4">
            <div className="progress-fill" style={{ width: `${(step / 4) * 100}%` }}></div>
          </div>
        </div>

        {error && <div className="alert-error mb-6">{error}</div>}

        <Card className="max-w-2xl mx-auto">
          <CardHeader>
            <CardTitle>
              {step === 1 && "Basic Information"}
              {step === 2 && "Choose Your Domain"}
              {step === 3 && "Experience Level"}
              {step === 4 && "Goals & Motivation"}
            </CardTitle>
          </CardHeader>
          <CardContent>
            {step === 1 && (
              <div className="space-y-4">
                <Input
                  label="Full Name"
                  name="full_name"
                  value={formData.full_name}
                  onChange={handleChange}
                  placeholder="e.g. Jane Doe"
                  required
                />
                <Input
                  label="Email"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="jane@example.com"
                  required
                />
              </div>
            )}

            {step === 2 && (
              <div className="domain-grid">
                {domains.map(domain => (
                  <div 
                    key={domain.id}
                    className={`domain-card ${formData.selected_domain === domain.id ? 'selected' : ''}`}
                    onClick={() => setFormData(prev => ({ ...prev, selected_domain: domain.id }))}
                  >
                    <h3 className="font-semibold text-lg">{domain.name}</h3>
                    <p className="text-sm text-muted mt-2">{domain.description}</p>
                  </div>
                ))}
              </div>
            )}

            {step === 3 && (
              <div className="space-y-4">
                <Select
                  label="Experience Level"
                  name="experience_level"
                  value={formData.experience_level}
                  onChange={handleChange}
                  options={[
                    { value: 'beginner', label: 'Beginner' },
                    { value: 'intermediate', label: 'Intermediate' },
                    { value: 'advanced', label: 'Advanced' },
                    { value: 'professional', label: 'Professional' }
                  ]}
                />
                <Select
                  label="Years of Experience"
                  name="years_of_experience"
                  value={formData.years_of_experience || 'none'}
                  onChange={handleChange}
                  options={[
                    { value: 'none', label: 'None' },
                    { value: 'less_than_1', label: '< 1 Year' },
                    { value: '1_2', label: '1 - 2 Years' },
                    { value: '3_5', label: '3 - 5 Years' },
                    { value: '5_plus', label: '5+ Years' }
                  ]}
                />
              </div>
            )}

            {step === 4 && (
              <div className="space-y-4">
                <Input
                  label="Learning Goal"
                  name="learning_goal"
                  value={formData.learning_goal}
                  onChange={handleChange}
                  placeholder="What do you want to learn?"
                  required
                />
                <Input
                  label="Career Goal"
                  name="career_goal"
                  value={formData.career_goal}
                  onChange={handleChange}
                  placeholder="Where do you want to be?"
                  required
                />
                <div className="input-wrapper">
                  <label className="input-label">Motivation (Optional)</label>
                  <textarea
                    className="input-field"
                    name="motivation"
                    value={formData.motivation}
                    onChange={handleChange}
                    placeholder="Why are you pursuing this path?"
                    rows={3}
                  />
                </div>
              </div>
            )}
          </CardContent>
          
          <CardFooter className="flex justify-between mt-6">
            <Button variant="outline" onClick={handleBack} disabled={step === 1 || isLoading}>
              Back
            </Button>
            {step < 4 ? (
              <Button 
                onClick={handleNext}
                disabled={(step === 1 && (!formData.full_name || !formData.email)) || (step === 2 && !formData.selected_domain)}
              >
                Next
              </Button>
            ) : (
              <Button 
                onClick={handleSubmit} 
                disabled={isLoading || !formData.learning_goal || !formData.career_goal}
              >
                {isLoading ? 'Creating Profile...' : 'Complete Profile'}
              </Button>
            )}
          </CardFooter>
        </Card>
      </div>
      {isLoading && <Loader fullScreen message="Setting up your learner profile..." />}
    </AppLayout>
  );
};
