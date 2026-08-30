import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { AppLayout } from '../components/layout/AppLayout';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Select } from '../components/ui/Select';
import { Loader } from '../components/ui/Loader';
import { auth } from '../utils/auth';
import { profileService, learningPathService, domainService } from '../services/api';
import type { GeneratePathPayload } from '../services/api';
import type { LearnerProfileResponse, DomainInfo } from '../types/schemas';
import './GeneratePath.css';

export const GeneratePath: React.FC = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingInitial, setIsLoadingInitial] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [domains, setDomains] = useState<DomainInfo[]>([]);
  const [loaderMessage, setLoaderMessage] = useState('Generating your learning path...');

  const [formData, setFormData] = useState({
    selected_domain: '',
    experience_level: 'beginner',
    learning_goal: '',
    career_goal: ''
  });

  // Load user profile and domain list on mount
  useEffect(() => {
    const fetchData = async () => {
      const userId = auth.getCurrentUserId();
      if (!userId) {
        setError('User not authenticated. Please complete onboarding first.');
        setIsLoadingInitial(false);
        return;
      }
      try {
        const [domainList, profile] = await Promise.all([
          domainService.getDomains(),
          profileService.getProfile(userId)
        ]);
        setDomains(domainList);
        // Set defaults based on profile (if available)
        setFormData({
          selected_domain: profile.selected_domain?.id || (domainList[0]?.id ?? ''),
          experience_level: profile.experience_level || 'beginner',
          learning_goal: profile.learning_goal || '',
          career_goal: profile.career_goal || ''
        });
      } catch (err: any) {
        console.error(err);
        setError('Failed to load initial data. Please try again later.');
      } finally {
        setIsLoadingInitial(false);
      }
    };
    fetchData();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    const userId = auth.getCurrentUserId();
    if (!userId) {
      setError('User not authenticated.');
      setIsLoading(false);
      return;
    }
    try {
      // Persist any changes the user made to their profile
      await profileService.updateProfile(userId, {
        selected_domain: formData.selected_domain,
        experience_level: formData.experience_level,
        learning_goal: formData.learning_goal,
        career_goal: formData.career_goal
      });
      setLoaderMessage('Crafting your personalized roadmap...');
      const payload: GeneratePathPayload = {
  user_id: userId,
  selected_domain: formData.selected_domain,
  experience_level: formData.experience_level,
  learning_goal: formData.learning_goal,
  career_goal: formData.career_goal,
};
const pathResult = await learningPathService.generatePath(payload);
      navigate(`/path/${pathResult.path_id}`);
    } catch (err: any) {
      console.error(err);
      let message = 'Failed to generate learning path.';
      if (err.response?.data?.detail) {
        if (Array.isArray(err.response.data.detail)) {
          message = err.response.data.detail.map((d: any) => d.msg || JSON.stringify(d)).join(', ');
        } else if (typeof err.response.data.detail === 'string') {
          message = err.response.data.detail;
        } else {
          message = JSON.stringify(err.response.data.detail);
        }
      } else if (err.message) {
        message = err.message;
      }
      setError(message);
      // Redirect to assessment if skill gap needed
      if (message.toLowerCase().includes('skill gap analysis required')) {
        const pendingPath = {
          selected_domain: formData.selected_domain,
          experience_level: formData.experience_level,
          learning_goal: formData.learning_goal,
          career_goal: formData.career_goal,
        };
        localStorage.setItem('pendingLearningPath', JSON.stringify(pendingPath));
        navigate('/assessment/intro');
      }
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoadingInitial) {
    return (
      <AppLayout>
        <Loader fullScreen message="Loading..." />
      </AppLayout>
    );
  }

  return (
    <AppLayout>
      <div className="container py-8 max-w-3xl mx-auto">
        <Card>
          <CardHeader>
            <CardTitle>Create Your Learning Path</CardTitle>
            <p className="text-muted">Tell us about your goals to get a personalized roadmap.</p>
          </CardHeader>
          <CardContent>
            {error && (
              <div className="alert-error mb-6">{error}</div>
            )}
            <form onSubmit={handleSubmit} className="form-grid">
              <Select
                label="Domain"
                name="selected_domain"
                value={formData.selected_domain}
                onChange={handleChange}
                options={domains.map(d => ({ value: d.id, label: d.name }))}
                required
              />
              <Select
                label="Experience Level"
                name="experience_level"
                value={formData.experience_level}
                onChange={handleChange}
                options={[
                  { value: 'beginner', label: 'Beginner (No experience)' },
                  { value: 'intermediate', label: 'Intermediate (Some experience)' },
                  { value: 'advanced', label: 'Advanced' },
                  { value: 'professional', label: 'Professional' }
                ]}
                required
              />
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
              <div className="col-span-full mt-4">
                <Button type="submit" size="lg" className="w-full" isLoading={isLoading}>
                  Generate Learning Path
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
        {isLoading && <Loader fullScreen message={loaderMessage} />}
      </div>
    </AppLayout>
  );
};
