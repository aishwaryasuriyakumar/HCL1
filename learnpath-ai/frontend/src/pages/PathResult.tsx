import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { BookOpen, Clock, Award, ArrowLeft, ExternalLink } from 'lucide-react';
import { AppLayout } from '../components/layout/AppLayout';
import { Button } from '../components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '../components/ui/Card';
import { Loader } from '../components/ui/Loader';
import { learningPathService, resourceService } from '../services/api';
import type { LearningPathResult, PhaseSpec, CuratedPathResources, ResourceCardData } from '../types/schemas';
import './PathResult.css';

export const PathResult: React.FC = () => {
  const { pathId } = useParams<{ pathId: string }>();
  const navigate = useNavigate();
  const [path, setPath] = useState<LearningPathResult | null>(null);
  const [resources, setResources] = useState<CuratedPathResources | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!pathId) return;
      try {
        const pathData = await learningPathService.getPath(pathId);
        setPath(pathData);
        
        try {
          // Try to fetch curated resources. We could use curateForPath, but getPathResources is safer 
          // if they're already curated, or we just call getPathResources.
          const resData = await resourceService.getPathResources(pathId);
          setResources(resData);
        } catch (resErr) {
          console.warn("Could not load resources, they might not be curated yet.");
          // We can optionally trigger curation here, but it might take a long time.
        }
      } catch (err: any) {
        console.error(err);
        setError('Failed to load learning path.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [pathId]);

  if (isLoading) {
    return (
      <AppLayout>
        <div className="container py-12 flex justify-center">
          <Loader size="lg" message="Loading your personalized roadmap..." />
        </div>
      </AppLayout>
    );
  }

  if (error || !path) {
    return (
      <AppLayout>
        <div className="container py-12 text-center">
          <h2 className="text-2xl text-error mb-4">Oops!</h2>
          <p className="text-muted mb-6">{error || 'Learning path not found.'}</p>
          <Link to="/dashboard">
            <Button>Go to Dashboard</Button>
          </Link>
        </div>
      </AppLayout>
    );
  }

  const getPhaseResources = (phaseId: string): ResourceCardData[] => {
    if (!resources) return [];
    const phaseRes = resources.phases.find(p => p.phase_id === phaseId);
    return phaseRes ? phaseRes.resources : [];
  };

  return (
    <AppLayout>
      <div className="result-header">
        <div className="container">
          <Link to="/dashboard" className="back-link mb-6 inline-flex items-center text-muted hover:text-primary transition-colors">
            <ArrowLeft className="w-4 h-4 mr-2" /> Back to Dashboard
          </Link>
          <div className="badge mb-4">Level: {path.overall_level}</div>
          <h1 className="path-title mb-4">{path.title}</h1>
          <p className="path-description text-muted max-w-3xl mb-8">
            {path.description}
          </p>
          <div className="path-stats flex flex-wrap gap-6 text-sm">
            <div className="stat-item flex items-center gap-2">
              <BookOpen className="text-primary w-5 h-5" />
              <span>{path.total_phases} Phases</span>
            </div>
            <div className="stat-item flex items-center gap-2">
              <Clock className="text-primary w-5 h-5" />
              <span>~{path.estimated_total_hours} Hours</span>
            </div>
          </div>
        </div>
      </div>

      <div className="container py-12">
        <div className="timeline">
          {path.phases.map((phase: PhaseSpec, index: number) => {
            const phaseResources = getPhaseResources(phase.phase_id);
            return (
              <div key={phase.phase_id} className="timeline-item">
                <div className="timeline-marker">
                  <span className="timeline-number">{index + 1}</span>
                </div>
                <div className="timeline-content">
                  <Card className="phase-card">
                    <CardHeader>
                      <div className="flex justify-between items-start">
                        <div>
                          <div className="text-xs text-primary font-bold uppercase tracking-wider mb-1">
                            Phase {phase.order}
                          </div>
                          <CardTitle>{phase.title}</CardTitle>
                        </div>
                        <div className="badge badge-outline text-xs capitalize">
                          {phase.status.replace('_', ' ')}
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <p className="text-muted mb-4">{phase.description}</p>
                      
                      <div className="mb-6">
                        <h4 className="text-sm font-semibold mb-2">Key Skills</h4>
                        <div className="flex flex-wrap gap-2">
                          {phase.skills.map(skill => (
                            <span key={skill} className="skill-tag">{skill}</span>
                          ))}
                        </div>
                      </div>

                      {phaseResources.length > 0 && (
                        <div className="mb-6">
                          <h4 className="text-sm font-semibold mb-3">Recommended Resources</h4>
                          <div className="space-y-3">
                            {phaseResources.map(res => (
                              <a 
                                key={res.resource_id} 
                                href={res.original_url} 
                                target="_blank" 
                                rel="noopener noreferrer"
                                className="block border rounded-md p-3 hover:border-primary transition-colors bg-surface-hover group"
                              >
                                <div className="flex justify-between items-start">
                                  <div>
                                    <h5 className="font-medium text-sm group-hover:text-primary transition-colors flex items-center gap-1">
                                      {res.title} <ExternalLink className="w-3 h-3 opacity-50" />
                                    </h5>
                                    <p className="text-xs text-muted mt-1">{res.platform} • {res.resource_type} • {res.difficulty}</p>
                                    <p className="text-xs italic text-muted mt-2 border-l-2 border-primary/30 pl-2">
                                      "{res.why_recommended}"
                                    </p>
                                  </div>
                                </div>
                              </a>
                            ))}
                          </div>
                        </div>
                      )}

                      <div className="project-box bg-primary/5 p-4 rounded-lg mt-4 border border-primary/20">
                        <h4 className="flex items-center gap-2 text-sm font-semibold mb-2">
                          <Award className="w-4 h-4 text-primary" /> 
                          Project: {phase.project.title}
                        </h4>
                        <p className="text-xs text-muted">{phase.project.description}</p>
                      </div>
                    </CardContent>
                    
                    {phase.completion_criteria.assessment_required && (
                      <CardFooter className="bg-muted/10 border-t mt-4 pt-4 flex justify-between items-center">
                        <div className="text-sm text-muted">
                          Ready to validate your skills?
                        </div>
                        <Button 
                          onClick={() => navigate(`/mastery/intro/${phase.phase_id}`)}
                        >
                          Take Mastery Assessment
                        </Button>
                      </CardFooter>
                    )}
                  </Card>
                </div>
              </div>
            );
          })}

          {/* Capstone Project */}
          <div className="timeline-item">
            <div className="timeline-marker timeline-marker-final">
              <Award className="w-5 h-5 text-warning" />
            </div>
            <div className="timeline-content">
              <Card className="capstone-card border-warning">
                <CardHeader>
                  <div className="text-xs text-warning font-bold uppercase tracking-wider mb-1">
                    Final Goal
                  </div>
                  <CardTitle>{path.capstone_project.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted mb-4">{path.capstone_project.description}</p>
                  <h4 className="text-sm font-semibold mb-2">Deliverables</h4>
                  <ul className="list-disc pl-5 text-sm text-muted">
                    {path.capstone_project.deliverables.map((d, i) => (
                      <li key={i}>{d}</li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  );
};
