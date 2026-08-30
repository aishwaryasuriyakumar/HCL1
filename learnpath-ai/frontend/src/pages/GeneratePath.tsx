import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AppLayout } from '../components/layout/AppLayout';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Select } from '../components/ui/Select';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card';
import { Loader } from '../components/ui/Loader';
import { profileService, skillGapService, learningPathService } from '../services/api';
import type { LearnerProfileCreate } from '../types/schemas';
import './GeneratePath.css';

export const GeneratePath: React.FC = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState<LearnerProfileCreate>({
    full_name: '',
    email: '',
    selected_domain: 'web_development',
    experience_level: 'beginner',
    learning_goal: '',
    career_goal: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const [loaderMessage, setLoaderMessage] = useState('Creating your profile...');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    try {
      setLoaderMessage('Creating your profile...');
      const profile = await profileService.createProfile(formData);
      
      setLoaderMessage('Analyzing your skill gaps...');
      await skillGapService.analyzeSkillGaps(profile.user_id);
      
      setLoaderMessage('Crafting your personalized roadmap...');
      const pathResult = await learningPathService.generatePath(profile.user_id);
      
      navigate(`/path/${pathResult.path_id}`);
    } catch (err: any) {
      console.error(err);
      let errorMessage = 'Failed to generate path. Please try again.';
      if (err.response?.data?.detail) {
        if (Array.isArray(err.response.data.detail)) {
          errorMessage = err.response.data.detail.map((d: any) => d.msg || JSON.stringify(d)).join(', ');
        } else if (typeof err.response.data.detail === 'string') {
          errorMessage = err.response.data.detail;
        } else {
          errorMessage = JSON.stringify(err.response.data.detail);
        }
      } else if (err.message) {
        errorMessage = err.message;
      }
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AppLayout>
      <div className="container py-8 max-w-3xl mx-auto">
        <Card>
          <CardHeader>
            <CardTitle>Create Your Learning Path</CardTitle>
            <p className="text-muted">Tell us about your background and goals to get a personalized roadmap.</p>
          </CardHeader>
          <CardContent>
            {error && (
              <div className="alert-error mb-6">
                {error}
              </div>
            )}
            
            <form onSubmit={handleSubmit} className="form-grid">
              <Input
                label="Full Name"
                name="full_name"
                value={formData.full_name}
                onChange={handleChange}
                required
                placeholder="John Doe"
              />
              
              <Input
                label="Email"
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                placeholder="john@example.com"
              />

              <Select
                label="Domain"
                name="selected_domain"
                value={formData.selected_domain}
                onChange={handleChange}
                required
                options={[
                  { value: 'machine_learning', label: 'Machine Learning' },
                  { value: 'data_science', label: 'Data Science' },
                  { value: 'generative_ai', label: 'Generative AI' },
                  { value: 'web_development', label: 'Web Development' },
                  { value: 'cloud_devops', label: 'Cloud & DevOps' }
                ]}
              />

              <Select
                label="Experience Level"
                name="experience_level"
                value={formData.experience_level}
                onChange={handleChange}
                required
                options={[
                  { value: 'beginner', label: 'Beginner (No experience)' },
                  { value: 'intermediate', label: 'Intermediate (Some experience)' },
                  { value: 'advanced', label: 'Advanced (Solid understanding)' },
                  { value: 'professional', label: 'Professional (Working in field)' }
                ]}
              />

              <Input
                label="Learning Goal"
                name="learning_goal"
                value={formData.learning_goal}
                onChange={handleChange}
                required
                placeholder="e.g. Master React and modern CSS"
                className="col-span-full"
              />

              <Input
                label="Career Goal"
                name="career_goal"
                value={formData.career_goal}
                onChange={handleChange}
                required
                placeholder="e.g. Get a job as a Junior Frontend Developer"
                className="col-span-full"
              />

              <div className="col-span-full mt-4">
                <Button type="submit" size="lg" className="w-full" isLoading={isLoading}>
                  Generate Learning Path
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>

      {isLoading && <Loader fullScreen message={loaderMessage} />}
    </AppLayout>
  );
};
