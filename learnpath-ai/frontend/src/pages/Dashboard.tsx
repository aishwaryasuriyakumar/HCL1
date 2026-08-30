import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { AppLayout } from '../components/layout/AppLayout';
import { Button } from '../components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '../components/ui/Card';
import { Loader } from '../components/ui/Loader';
import { learningPathService, profileService } from '../services/api';
import { auth } from '../utils/auth';
import type { LearningPathResult } from '../types/schemas';

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const handleStartNewPath = async () => {
    const userId = auth.getCurrentUserId();
    if (!userId) {
      navigate('/');
      return;
    }
    try {
      const profile = await profileService.getProfile(userId);
      if (profile.full_name && profile.email) {
        // Existing learner – skip basic info
        navigate('/onboarding?skip=basic');
      } else {
        navigate('/onboarding');
      }
    } catch (err) {
      console.error('Failed to load profile', err);
      navigate('/onboarding');
    }
  };
  const [path, setPath] = useState<LearningPathResult | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboard = async () => {
      const userId = auth.getCurrentUserId();
      if (!userId) {
        navigate('/');
        return;
      }
      
      try {
        const pathData = await learningPathService.getLatestPath(userId);
        setPath(pathData);
      } catch (err: any) {
        console.error(err);
        setError("Could not load your learning path. Have you generated one yet?");
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchDashboard();
  }, [navigate]);

  if (isLoading) return <AppLayout><Loader fullScreen message="Loading dashboard..." /></AppLayout>;
  
  if (error || !path) {
    return (
      <AppLayout>
        <div className="container py-12 max-w-2xl text-center">
          <div className="alert-error mb-6">{error || "No learning path found"}</div>
          <Button onClick={handleStartNewPath}>Start New Path</Button>
        </div>
      </AppLayout>
    );
  }

  const completedPhases = path.phases.filter(p => p.status === 'completed').length;
  const progressPercent = Math.round((completedPhases / path.total_phases) * 100);
  
  const currentPhase = path.phases.find(p => p.status === 'in_progress') || path.phases.find(p => p.status === 'not_started');

  return (
    <AppLayout>
      <div className="container py-12 max-w-5xl">
        <div className="flex justify-between items-end mb-8">
          <div>
            <h1 className="text-3xl font-bold mb-2">Welcome Back!</h1>
            <p className="text-muted">Continue your journey in {path.domain}</p>
          </div>
          <div>
            <Button variant="outline" onClick={() => navigate('/skill-gap')}>
              View Skill Gaps
            </Button>
          </div>
        </div>

        <Card className="mb-8">
          <CardContent className="p-6">
            <div className="flex justify-between items-center mb-2">
              <span className="font-semibold text-sm">Overall Progress</span>
              <span className="font-bold">{progressPercent}%</span>
            </div>
            <div className="h-3 w-full bg-border rounded-full overflow-hidden">
              <div 
                className="h-full bg-primary transition-all duration-500" 
                style={{ width: `${progressPercent}%` }}
              ></div>
            </div>
            <p className="text-sm text-muted mt-3">
              You have completed {completedPhases} of {path.total_phases} phases.
            </p>
          </CardContent>
        </Card>

        <div className="grid md:grid-cols-3 gap-6">
          <div className="md:col-span-2 space-y-6">
            <h2 className="text-xl font-bold">Current Focus</h2>
            
            {currentPhase ? (
              <Card className="border-primary/50 shadow-sm">
                <CardHeader className="bg-primary/5 pb-4">
                  <div className="text-xs font-bold text-primary uppercase tracking-wider mb-1">
                    Phase {currentPhase.order}
                  </div>
                  <CardTitle>{currentPhase.title}</CardTitle>
                </CardHeader>
                <CardContent className="pt-4">
                  <p className="text-muted mb-4">{currentPhase.description}</p>
                  
                  <div className="mb-4">
                    <h4 className="text-sm font-semibold mb-2">Skills to Master</h4>
                    <div className="flex flex-wrap gap-2">
                      {currentPhase.skills.map(skill => (
                        <span key={skill} className="skill-tag">{skill}</span>
                      ))}
                    </div>
                  </div>
                </CardContent>
                <CardFooter className="flex gap-4">
                  <Button onClick={() => navigate(`/path/${path.path_id}`)}>
                    View Full Path & Resources
                  </Button>
                  <Button variant="outline" onClick={() => navigate(`/mastery/intro/${currentPhase.phase_id}`)}>
                    Take Assessment
                  </Button>
                </CardFooter>
              </Card>
            ) : (
              <Card>
                <CardContent className="p-8 text-center">
                  <h3 className="text-xl font-bold mb-2">You've completed all phases!</h3>
                  <p className="text-muted mb-4">Great job mastering {path.domain}. Ready for your capstone project?</p>
                  <Button onClick={() => navigate(`/path/${path.path_id}`)}>
                    View Capstone Details
                  </Button>
                </CardContent>
              </Card>
            )}
          </div>
          
          <div>
            <h2 className="text-xl font-bold mb-6">Path Details</h2>
            <Card>
              <CardContent className="p-6 space-y-4">
                <div>
                  <h4 className="text-xs font-semibold text-muted uppercase tracking-wider mb-1">Goal</h4>
                  <p className="text-sm">{path.career_goal}</p>
                </div>
                <div className="border-t border-border pt-4">
                  <h4 className="text-xs font-semibold text-muted uppercase tracking-wider mb-1">Target Level</h4>
                  <p className="text-sm capitalize">{path.overall_level}</p>
                </div>
                <div className="border-t border-border pt-4">
                  <h4 className="text-xs font-semibold text-muted uppercase tracking-wider mb-1">Est. Time</h4>
                  <p className="text-sm">{path.estimated_total_hours} Hours</p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </AppLayout>
  );
};
