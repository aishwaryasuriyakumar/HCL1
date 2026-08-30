import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { AppLayout } from '../components/layout/AppLayout';
import { Button } from '../components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card';
import { Loader } from '../components/ui/Loader';
import { CheckCircle, AlertTriangle } from 'lucide-react';
import { masteryService } from '../services/api';
import type { MasteryResult } from '../types/schemas';

export const MasteryResultPage: React.FC = () => {
  const { attemptId } = useParams<{ attemptId: string }>();
  const navigate = useNavigate();
  
  const [result, setResult] = useState<MasteryResult | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchResult = async () => {
      if (!attemptId) return;
      try {
        const data = await masteryService.getResult(attemptId);
        setResult(data);
      } catch (err: any) {
        console.error(err);
        setError("Failed to load result.");
      } finally {
        setIsLoading(false);
      }
    };
    fetchResult();
  }, [attemptId]);

  const handleRemediationComplete = async () => {
    if (!attemptId) return;
    try {
      await masteryService.completeRemediation(attemptId);
      navigate(`/mastery/intro/${result?.phase_id}`);
    } catch (err: any) {
      console.error(err);
      setError("Failed to mark remediation as complete.");
    }
  };

  if (isLoading) return <AppLayout><Loader fullScreen message="Grading your assessment..." /></AppLayout>;
  
  if (error || !result) {
    return (
      <AppLayout>
        <div className="container py-12 text-center">
          <div className="alert-error mb-6">{error || "Result not found"}</div>
          <Button onClick={() => navigate('/dashboard')}>Return to Dashboard</Button>
        </div>
      </AppLayout>
    );
  }

  return (
    <AppLayout>
      <div className="container py-12 max-w-4xl">
        
        <div className="text-center mb-10">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-full mb-6 mx-auto bg-muted/10">
            {result.passed ? (
              <CheckCircle className="w-10 h-10 text-success" />
            ) : (
              <AlertTriangle className="w-10 h-10 text-warning" />
            )}
          </div>
          <h1 className="text-3xl font-bold mb-4">
            {result.passed ? "Phase Mastered!" : "Needs Improvement"}
          </h1>
          <p className="text-muted max-w-2xl mx-auto">
            {result.passed 
              ? "Congratulations! You have successfully mastered this phase and unlocked the next steps in your learning path." 
              : "You didn't quite hit the pass threshold. Let's review the weak topics to strengthen your understanding before trying again."}
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <Card className={`text-center border-none text-white ${result.passed ? 'bg-success' : 'bg-warning'}`}>
            <CardContent className="p-6">
              <div className="text-sm uppercase tracking-wider mb-2 opacity-80">Your Score</div>
              <div className="text-5xl font-bold">{Math.round(result.score)}%</div>
            </CardContent>
          </Card>
          
          <Card className="text-center border-border">
            <CardContent className="p-6">
              <div className="text-sm uppercase tracking-wider mb-2 text-muted">Pass Threshold</div>
              <div className="text-5xl font-bold text-muted">{Math.round(result.pass_threshold)}%</div>
            </CardContent>
          </Card>
        </div>

        {!result.passed && result.weak_topics.length > 0 && (
          <Card className="mb-8 border-warning/50">
            <CardHeader className="bg-warning/5">
              <CardTitle className="text-warning text-lg flex items-center gap-2">
                <AlertTriangle className="w-5 h-5" /> Topics to Review
              </CardTitle>
            </CardHeader>
            <CardContent className="pt-6 space-y-4">
              {result.weak_topics.map((topic, idx) => (
                <div key={idx} className="bg-surface-hover p-4 rounded-md border border-border">
                  <div className="flex justify-between font-medium mb-1">
                    <span>{topic.topic}</span>
                    <span className="text-warning">{Math.round(topic.score)}%</span>
                  </div>
                  {topic.reason && <p className="text-sm text-muted mt-2">{topic.reason}</p>}
                </div>
              ))}
            </CardContent>
          </Card>
        )}

        <div className="text-center bg-muted/10 p-8 rounded-xl border border-border">
          <h2 className="text-xl font-bold mb-4">Next Action</h2>
          <p className="text-muted mb-6">
            {result.next_action || (result.passed ? "Continue to the next phase in your learning path." : "Review recommended resources and complete remediation.")}
          </p>
          
          {result.passed ? (
            <Button size="lg" onClick={() => navigate('/dashboard')}>
              Continue to Dashboard
            </Button>
          ) : (
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" variant="outline" onClick={() => navigate(`/path/${result.learning_path_id}`)}>
                Review Resources
              </Button>
              <Button size="lg" onClick={handleRemediationComplete}>
                Mark Remediation Complete & Retake
              </Button>
            </div>
          )}
        </div>
      </div>
    </AppLayout>
  );
};
