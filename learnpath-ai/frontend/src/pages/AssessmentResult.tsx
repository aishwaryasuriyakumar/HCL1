import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { AppLayout } from '../components/layout/AppLayout';
import { Button } from '../components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card';
import { Loader } from '../components/ui/Loader';
import { assessmentService, skillGapService } from '../services/api';
import { auth } from '../utils/auth';
import type { AssessmentResult } from '../types/schemas';

export const AssessmentResultPage: React.FC = () => {
  const { attemptId } = useParams<{ attemptId: string }>();
  const navigate = useNavigate();
  
  const [result, setResult] = useState<AssessmentResult | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchResult = async () => {
      if (!attemptId) return;
      try {
        const data = await assessmentService.getResult(attemptId);
        setResult(data);
      } catch (err: any) {
        console.error(err);
        setError("Failed to load assessment result.");
      } finally {
        setIsLoading(false);
      }
    };
    fetchResult();
  }, [attemptId]);

  const handleAnalyzeGaps = async () => {
    const userId = auth.getCurrentUserId();
    if (!userId) return;
    
    setIsAnalyzing(true);
    try {
      await skillGapService.analyzeSkillGaps(userId);
      navigate('/skill-gap');
    } catch (err: any) {
      console.error(err);
      setError("Failed to analyze skill gaps.");
      setIsAnalyzing(false);
    }
  };

  if (isLoading) return <AppLayout><Loader fullScreen message="Loading results..." /></AppLayout>;
  
  if (error || !result) {
    return (
      <AppLayout>
        <div className="container py-12 max-w-2xl text-center">
          <div className="alert-error mb-6">{error || "Result not found"}</div>
          <Button onClick={() => navigate('/dashboard')}>Return to Dashboard</Button>
        </div>
      </AppLayout>
    );
  }

  return (
    <AppLayout>
      <div className="container py-12 max-w-4xl">
        {isAnalyzing && <Loader fullScreen message="Analyzing your skill gaps..." />}
        
        <div className="text-center mb-10">
          <h1 className="text-3xl font-bold mb-4">Diagnostic Assessment Complete</h1>
          <p className="text-muted max-w-2xl mx-auto">
            Great job! We've analyzed your responses. Here is a high-level overview of your current proficiency.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <Card className="text-center bg-primary text-white border-none">
            <CardContent className="p-6">
              <div className="text-sm uppercase tracking-wider mb-2 opacity-80">Overall Score</div>
              <div className="text-5xl font-bold">{Math.round(result.overall.score)}%</div>
            </CardContent>
          </Card>
          
          <Card className="text-center border-primary/20">
            <CardContent className="p-6">
              <div className="text-sm uppercase tracking-wider mb-2 text-muted">Proficiency Level</div>
              <div className="text-3xl font-bold text-primary capitalize">{result.overall.proficiency}</div>
            </CardContent>
          </Card>
          
          <Card className="text-center border-primary/20">
            <CardContent className="p-6">
              <div className="text-sm uppercase tracking-wider mb-2 text-muted">Accuracy</div>
              <div className="text-3xl font-bold">
                {result.overall.correct_answers} / {result.overall.total_questions}
              </div>
            </CardContent>
          </Card>
        </div>

        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Skill Breakdown</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            {result.skill_results.map((skill, idx) => (
              <div key={idx} className="border-b pb-4 last:border-0 last:pb-0">
                <div className="flex justify-between items-end mb-2">
                  <div>
                    <h3 className="font-medium text-lg">{skill.skill}</h3>
                    <p className="text-sm text-muted capitalize">{skill.proficiency} proficiency</p>
                  </div>
                  <div className="text-right">
                    <span className="font-bold text-lg">{Math.round(skill.score)}%</span>
                  </div>
                </div>
                <div className="h-2 w-full bg-border rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-primary" 
                    style={{ width: `${Math.round(skill.score)}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        <div className="text-center bg-muted/20 p-8 rounded-xl">
          <h2 className="text-2xl font-bold mb-4">Ready for your personalized path?</h2>
          <p className="text-muted mb-6 max-w-2xl mx-auto">
            Now that we know your current skill level, we can map out exactly what you need to learn to reach your goals.
          </p>
          <Button size="lg" onClick={handleAnalyzeGaps} disabled={isAnalyzing}>
            Analyze My Skill Gaps
          </Button>
        </div>
      </div>
    </AppLayout>
  );
};
