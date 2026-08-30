import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { BookOpen, Clock, Award, ArrowLeft } from 'lucide-react';
import { AppLayout } from '../components/layout/AppLayout';
import { Button } from '../components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '../components/ui/Card';
import { Loader } from '../components/ui/Loader';
import { learningPathService } from '../services/api';
import type { LearningPathResult, PhaseSpec } from '../types/schemas';
import './PathResult.css';

export const PathResult: React.FC = () => {
  const { pathId } = useParams<{ pathId: string }>();
  const [path, setPath] = useState<LearningPathResult | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPath = async () => {
      if (!pathId) return;
      try {
        const data = await learningPathService.getPath(pathId);
        setPath(data);
      } catch (err: any) {
        console.error(err);
        setError('Failed to load learning path.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchPath();
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
          <Link to="/">
            <Button>Go Home</Button>
          </Link>
        </div>
      </AppLayout>
    );
  }

  return (
    <AppLayout>
      <div className="result-header">
        <div className="container">
          <Link to="/" className="back-link mb-6 inline-flex items-center text-muted hover:text-primary transition-colors">
            <ArrowLeft className="w-4 h-4 mr-2" /> Back to Home
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
          {path.phases.map((phase: PhaseSpec, index: number) => (
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
                      <div className="badge badge-outline text-xs">
                        {phase.estimated_hours}h
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-muted mb-4">{phase.description}</p>
                    
                    <div className="mb-4">
                      <h4 className="text-sm font-semibold mb-2">Key Skills</h4>
                      <div className="flex flex-wrap gap-2">
                        {phase.skills.map(skill => (
                          <span key={skill} className="skill-tag">{skill}</span>
                        ))}
                      </div>
                    </div>

                    <div className="project-box bg-surface-hover p-4 rounded-lg mt-4 border border-border">
                      <h4 className="flex items-center gap-2 text-sm font-semibold mb-2">
                        <Award className="w-4 h-4 text-warning" /> 
                        Project: {phase.project.title}
                      </h4>
                      <p className="text-xs text-muted">{phase.project.description}</p>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          ))}

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
                <CardFooter>
                  <Button variant="primary" className="w-full sm:w-auto">Start Learning Path</Button>
                </CardFooter>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  );
};
