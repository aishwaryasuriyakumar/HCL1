import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { PlusCircle, ExternalLink, Compass, BookOpen, CheckCircle2 } from 'lucide-react';
import { AppLayout } from '../components/layout/AppLayout';
import { Button } from '../components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '../components/ui/Card';
import { Loader } from '../components/ui/Loader';
import { learningPathService } from '../services/api';
import { auth } from '../utils/auth';
import type { UserPathSummary, PhaseSpec } from '../types/schemas';
import './Dashboard.css';

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [paths, setPaths] = useState<UserPathSummary[]>([]);
  const [selectedPathId, setSelectedPathId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const handleStartNewPath = async () => {
    navigate('/generate');
  };

  useEffect(() => {
    const fetchDashboard = async () => {
      const userId = auth.getCurrentUserId();
      if (!userId) {
        navigate('/');
        return;
      }
      
      try {
        const response = await learningPathService.getUserPaths(userId);
        const userPaths = response.paths || [];
        setPaths(userPaths);
        if (userPaths.length > 0) {
          setSelectedPathId(userPaths[0].path_id);
        }
      } catch (err: any) {
        console.error(err);
        setError("Could not load your learning paths. Please try again or create a new path.");
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchDashboard();
  }, [navigate]);

  if (isLoading) return <AppLayout><Loader fullScreen message="Loading dashboard..." /></AppLayout>;
  
  if (error && paths.length === 0) {
    return (
      <AppLayout>
        <div className="container py-12 max-w-2xl text-center">
          <div className="alert-error mb-6">{error}</div>
          <Button onClick={handleStartNewPath}>
            <PlusCircle className="w-4 h-4 mr-2" /> Start New Path
          </Button>
        </div>
      </AppLayout>
    );
  }

  if (paths.length === 0) {
    return (
      <AppLayout>
        <div className="container py-12 max-w-2xl text-center">
          <Card className="p-8">
            <CardContent>
              <div className="w-16 h-16 rounded-full bg-primary/10 text-primary mx-auto flex items-center justify-center mb-4">
                <Compass className="w-8 h-8" />
              </div>
              <h2 className="text-2xl font-bold mb-2">No Learning Paths Yet</h2>
              <p className="text-muted mb-6">
                Tell us about your career goals and skill gaps to generate your first personalized learning roadmap.
              </p>
              <Button size="lg" onClick={handleStartNewPath}>
                <PlusCircle className="w-4 h-4 mr-2" /> Create Your First Path
              </Button>
            </CardContent>
          </Card>
        </div>
      </AppLayout>
    );
  }

  // Selected Path
  const currentPath = paths.find(p => p.path_id === selectedPathId) || paths[0];

  // Exact completion calculations
  const totalPhases = currentPath.total_phases || currentPath.phases?.length || 0;
  const completedPhases = currentPath.phases?.filter(p => p.status === 'completed').length || currentPath.completed_phases || 0;
  const isPathCompleted = totalPhases > 0 && completedPhases === totalPhases;
  const progressPercent = totalPhases > 0 ? Math.round((completedPhases / totalPhases) * 100) : 0;

  // Find active current phase
  let currentPhase: PhaseSpec | undefined = undefined;
  if (!isPathCompleted && currentPath.phases && currentPath.phases.length > 0) {
    currentPhase = currentPath.phases.find(p => p.status === 'in_progress')
      || currentPath.phases.find(p => p.status === 'available')
      || currentPath.phases.find(p => p.status !== 'completed')
      || currentPath.phases[0];
  }

  const getStatusChipClass = (status: string) => {
    switch (status) {
      case 'completed': return 'status-chip-completed';
      case 'in_progress': return 'status-chip-in_progress';
      default: return 'status-chip-not_started';
    }
  };

  return (
    <AppLayout>
      <div className="container py-10 max-w-5xl">
        {/* Header Bar */}
        <div className="flex justify-between items-center mb-8 flex-wrap gap-4">
          <div>
            <h1 className="text-3xl font-extrabold mb-1">Learner Dashboard</h1>
            <p className="text-muted">Manage your personalized AI learning paths and milestones</p>
          </div>
          <div className="flex gap-3">
            <Button variant="outline" onClick={() => navigate('/skill-gap')}>
              Skill Gaps
            </Button>
            <Button onClick={handleStartNewPath}>
              <PlusCircle className="w-4 h-4 mr-1.5" /> New Path
            </Button>
          </div>
        </div>

        {/* Section 1: My Learning Paths List */}
        <section className="mb-10">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold">My Learning Paths ({paths.length})</h2>
            <span className="text-xs font-semibold text-muted">Click a path to focus or open</span>
          </div>

          <div className="dashboard-paths-grid">
            {paths.map((p) => {
              const pTotal = p.total_phases || p.phases?.length || 0;
              const pCompleted = p.phases?.filter(ph => ph.status === 'completed').length ?? p.completed_phases ?? 0;
              const pPct = pTotal > 0 ? Math.round((pCompleted / pTotal) * 100) : p.progress_percentage || 0;
              const isSelected = p.path_id === currentPath.path_id;

              return (
                <div 
                  key={p.path_id} 
                  className={`path-card-item ${isSelected ? 'active-selected' : ''}`}
                  onClick={() => setSelectedPathId(p.path_id)}
                  style={{ cursor: 'pointer' }}
                >
                  <div className="path-card-top">
                    <div className="flex justify-between items-start mb-1">
                      <span className="path-card-domain">{p.domain.replace('_', ' ')}</span>
                      <span className={`status-chip ${getStatusChipClass(p.status)}`}>
                        {p.status.replace('_', ' ')}
                      </span>
                    </div>
                    <h3 className="path-card-title">{p.title || `${p.domain} Learning Path`}</h3>
                    <p className="path-card-goal text-muted truncate">{p.career_goal || p.learning_goal}</p>
                  </div>

                  <div className="path-card-progress">
                    <div className="flex justify-between items-center text-xs font-semibold mb-1.5">
                      <span>Progress: {pPct}%</span>
                      <span className="text-muted">{pCompleted} / {pTotal} phases</span>
                    </div>
                    <div className="h-2 w-full bg-border rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-primary transition-all duration-300"
                        style={{ width: `${pPct}%` }}
                      ></div>
                    </div>
                  </div>

                  <div className="path-card-footer" onClick={(e) => e.stopPropagation()}>
                    <span className="text-xs text-muted capitalize font-medium">
                      Level: {p.experience_level}
                    </span>
                    <Button 
                      size="sm" 
                      onClick={() => navigate(`/path/${p.path_id}`)}
                    >
                      Open Path <ExternalLink className="w-3.5 h-3.5 ml-1" />
                    </Button>
                  </div>
                </div>
              );
            })}
          </div>
        </section>

        {/* Section 2: Selected Path Overview & Current Focus */}
        <section>
          <div className="flex items-center gap-2 mb-4">
            <span className="badge">FOCUSED PATH</span>
            <h2 className="text-xl font-bold">{currentPath.title || currentPath.domain}</h2>
          </div>

          {/* Progress Card */}
          <Card className="mb-8">
            <CardContent className="p-6">
              <div className="flex justify-between items-center mb-2">
                <span className="font-semibold text-sm">Overall Path Progress</span>
                <span className="font-extrabold text-primary text-lg">{progressPercent}%</span>
              </div>
              <div className="h-3 w-full bg-border rounded-full overflow-hidden">
                <div 
                  className="h-full bg-primary transition-all duration-500" 
                  style={{ width: `${progressPercent}%` }}
                ></div>
              </div>
              <p className="text-sm text-muted mt-3">
                You have completed {completedPhases} of {totalPhases} phases.
              </p>
            </CardContent>
          </Card>

          <div className="grid md:grid-cols-3 gap-6">
            {/* Current Focus / Completion Status */}
            <div className="md:col-span-2 space-y-6">
              <h3 className="text-lg font-bold">Current Focus</h3>
              
              {isPathCompleted ? (
                <Card className="border-green-200 bg-green-50/10">
                  <CardContent className="p-8 text-center">
                    <div className="w-12 h-12 rounded-full bg-green-100 text-green-600 mx-auto flex items-center justify-center mb-3">
                      <CheckCircle2 className="w-6 h-6" />
                    </div>
                    <h3 className="text-xl font-bold mb-2">You've completed all phases!</h3>
                    <p className="text-muted mb-6">
                      Outstanding work mastering {currentPath.domain.replace('_', ' ')}. Ready for your capstone project?
                    </p>
                    <Button onClick={() => navigate(`/path/${currentPath.path_id}`)}>
                      View Capstone Details
                    </Button>
                  </CardContent>
                </Card>
              ) : currentPhase ? (
                <Card className="border-primary/40 shadow-sm">
                  <CardHeader className="bg-primary/5 pb-4">
                    <div className="text-xs font-bold text-primary uppercase tracking-wider mb-1">
                      Phase {currentPhase.order}
                    </div>
                    <CardTitle>{currentPhase.title}</CardTitle>
                  </CardHeader>
                  <CardContent className="pt-4">
                    <p className="text-muted mb-4">{currentPhase.description}</p>
                    
                    <div className="mb-4">
                      <h4 className="text-sm font-semibold mb-2">Key Skills</h4>
                      <div className="flex flex-wrap gap-2">
                        {(currentPhase.skills || []).map(skill => (
                          <span key={skill} className="skill-tag">{skill}</span>
                        ))}
                      </div>
                    </div>
                  </CardContent>
                  <CardFooter className="flex gap-4 flex-wrap">
                    <Button onClick={() => navigate(`/path/${currentPath.path_id}`)}>
                      View Full Path & Resources
                    </Button>
                    <Button 
                      variant="outline" 
                      onClick={() => navigate(`/mastery/intro/${currentPhase.phase_id}`)}
                    >
                      Take Mastery Assessment
                    </Button>
                  </CardFooter>
                </Card>
              ) : (
                <Card>
                  <CardContent className="p-6 text-center text-muted">
                    Your learning path is being prepared.
                  </CardContent>
                </Card>
              )}
            </div>
            
            {/* Path Details Sidebar */}
            <div>
              <h3 className="text-lg font-bold mb-4">Path Details</h3>
              <Card>
                <CardContent className="p-6 space-y-4">
                  <div>
                    <h4 className="text-xs font-bold text-muted uppercase tracking-wider mb-1">Goal</h4>
                    <p className="text-sm font-medium text-gray-900">{currentPath.career_goal || currentPath.learning_goal || 'Not specified'}</p>
                  </div>
                  <div className="border-t border-border pt-4">
                    <h4 className="text-xs font-bold text-muted uppercase tracking-wider mb-1">Target Level</h4>
                    <p className="text-sm font-medium capitalize">{currentPath.experience_level}</p>
                  </div>
                  <div className="border-t border-border pt-4">
                    <h4 className="text-xs font-bold text-muted uppercase tracking-wider mb-1">Phases</h4>
                    <p className="text-sm font-medium">{totalPhases} structured phases</p>
                  </div>
                  <div className="pt-2">
                    <Button 
                      variant="outline" 
                      className="w-full"
                      onClick={() => navigate(`/path/${currentPath.path_id}`)}
                    >
                      <BookOpen className="w-4 h-4 mr-2" /> Open Full Roadmap
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>
      </div>
    </AppLayout>
  );
};
