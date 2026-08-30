import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { AppLayout } from '../components/layout/AppLayout';
import { Button } from '../components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card';
import { Loader } from '../components/ui/Loader';
import { skillGapService, learningPathService } from '../services/api';
import { auth } from '../utils/auth';
import type { SkillGapResult } from '../types/schemas';


export const SkillGapPage: React.FC = () => {
  const navigate = useNavigate();
  const [skillGap, setSkillGap] = useState<SkillGapResult | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isGeneratingPath, setIsGeneratingPath] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [generationError, setGenerationError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSkillGaps = async () => {
      const userId = auth.getCurrentUserId();
      if (!userId) {
        navigate('/onboarding');
        return;
      }
      
      try {
        const data = await skillGapService.getLatestAnalysis(userId);
        setSkillGap(data);
      } catch (err: any) {
        console.error(err);
        setError("Could not load your skill gap analysis. Please make sure you've completed the assessment.");
      } finally {
        setIsLoading(false);
      }
    };
    fetchSkillGaps();
  }, [navigate]);

  const handleGeneratePath = async () => {
    const userId = auth.getCurrentUserId();
    if (!userId) return;

    setError(null);
    setGenerationError(null);
    setIsGeneratingPath(true);
    try {
      const pathResult = await learningPathService.generatePath(userId);
      navigate(`/path/${pathResult.path_id}`);
    } catch (err: any) {
      console.error(err);
      // If generation fails (e.g., path already exists or backend error), try fetching the latest path
      try {
        const latest = await learningPathService.getLatestPath(userId);
        navigate(`/path/${latest.path_id}`);
      } catch (fallbackErr) {
        setGenerationError('Failed to generate learning path. Please try again.');
      }
      setIsGeneratingPath(false);
    }
  };

  const getSeverityColor = (severity: string) => {
    switch(severity) {
      case 'critical': return 'bg-red-100 text-red-800 border-red-200';
      case 'high': return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'moderate': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'minor': return 'bg-blue-100 text-blue-800 border-blue-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  if (isLoading) return <AppLayout><Loader fullScreen message="Loading skill gap analysis..." /></AppLayout>;
  
  if (error || !skillGap) {
    return (
      <AppLayout>
        <div className="container py-12 max-w-2xl text-center">
          <div className="alert-error mb-6">{error || "Analysis not found"}</div>
          <Button onClick={() => navigate('/assessment/intro')}>Take Assessment</Button>
        </div>
      </AppLayout>
    );
  }

  return (
    <AppLayout>
      <div className="container py-12 max-w-5xl">
        {isGeneratingPath && <Loader fullScreen message="AI is crafting your personalized roadmap..." />}
        {generationError && (
          <div className="alert-error mb-6 text-center">
            {generationError}
            <Button className="mt-4 block mx-auto" onClick={handleGeneratePath}>Retry</Button>
          </div>
        )}
        
        <div className="mb-10 text-center">
          <h1 className="text-3xl font-bold mb-4">Your Skill Gap Analysis</h1>
          <p className="text-muted max-w-3xl mx-auto text-lg leading-relaxed">
            {skillGap.summary}
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <div className="md:col-span-2 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Detailed Skill Breakdown</CardTitle>
              </CardHeader>
              <CardContent className="space-y-8">
                {skillGap.skills.map((skill, idx) => (
                  <div key={idx} className="skill-gap-item border-b pb-6 last:border-0 last:pb-0">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="font-semibold text-lg">{skill.skill}</h3>
                        <div className={`mt-2 inline-block px-2 py-1 text-xs font-medium rounded-full border ${getSeverityColor(skill.severity)}`}>
                          {skill.severity.toUpperCase()} GAP
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-sm text-muted">Gap</div>
                        <div className="text-xl font-bold">{Math.round(skill.gap_score)} pts</div>
                      </div>
                    </div>
                    
                    <div className="mb-4">
                      <div className="flex justify-between text-sm mb-1">
                        <span>Current: {Math.round(skill.current_score)}%</span>
                        <span className="font-medium">Target: {Math.round(skill.target_score)}%</span>
                      </div>
                      <div className="h-3 w-full bg-border rounded-full overflow-hidden relative">
                        <div 
                          className="h-full bg-primary absolute left-0 top-0" 
                          style={{ width: `${Math.round(skill.current_score)}%` }}
                        ></div>
                        <div 
                          className="h-full bg-yellow-400 absolute top-0" 
                          style={{ 
                            left: `${Math.round(skill.current_score)}%`, 
                            width: `${Math.round(skill.gap_score)}%` 
                          }}
                        ></div>
                        <div 
                          className="h-full border-r-2 border-black absolute top-0"
                          style={{ left: `${Math.round(skill.target_score)}%` }}
                        ></div>
                      </div>
                    </div>
                    
                    <div className="bg-muted/30 p-4 rounded-md">
                      <h4 className="text-sm font-semibold mb-1">Why this matters</h4>
                      <p className="text-sm text-muted">{skill.reason}</p>
                      {skill.prerequisites.length > 0 && (
                        <p className="text-sm mt-2"><span className="font-medium">Prerequisites:</span> {skill.prerequisites.join(', ')}</p>
                      )}
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>
          
          <div className="space-y-6">
            <Card className="bg-primary text-white border-none">
              <CardContent className="p-6">
                <h3 className="font-semibold text-xl mb-4">Ready to close the gap?</h3>
                <p className="opacity-90 mb-6">
                  We have mapped out the precise learning path you need to master these skills.
                </p>
                <Button 
                  className="w-full bg-white text-primary hover:bg-gray-100" 
                  size="lg"
                  onClick={handleGeneratePath}
                >
                  View Learning Path
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Recommended Focus</CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-4">
                  {skillGap.recommended_focus.map((focus) => (
                    <li key={focus.order} className="flex gap-3">
                      <div className="bg-primary/10 text-primary w-6 h-6 rounded-full flex items-center justify-center font-bold text-sm shrink-0">
                        {focus.order}
                      </div>
                      <div>
                        <div className="font-medium">{focus.skill}</div>
                        <div className="text-xs text-muted mt-1">{focus.reason}</div>
                      </div>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </AppLayout>
  );
};
