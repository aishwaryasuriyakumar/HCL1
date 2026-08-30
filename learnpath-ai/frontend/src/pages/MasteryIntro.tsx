import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { AppLayout } from '../components/layout/AppLayout';
import { Button } from '../components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '../components/ui/Card';
import { masteryService } from '../services/api';
import { auth } from '../utils/auth';

export const MasteryIntro: React.FC = () => {
  const { phaseId } = useParams<{ phaseId: string }>();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleStart = async () => {
    const userId = auth.getCurrentUserId();
    if (!userId || !phaseId) return;
    
    setIsLoading(true);
    setError(null);
    try {
      const response = await masteryService.start(userId, phaseId);
      // Store in localStorage since there is no GET endpoint for active mastery attempts
      localStorage.setItem(`mastery_${response.mastery_attempt_id}`, JSON.stringify(response));
      navigate(`/mastery/${response.mastery_attempt_id}`);
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || "Failed to start mastery assessment.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AppLayout>
      <div className="container py-12 max-w-3xl">
        {error && <div className="alert-error mb-6">{error}</div>}
        
        <Card>
          <CardHeader className="text-center">
            <div className="text-xs font-bold text-primary uppercase tracking-wider mb-2">Phase Validation</div>
            <CardTitle className="text-2xl">Mastery Assessment</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6 text-center">
            <p className="text-lg text-muted">
              You've completed this phase. Let's check your understanding before moving on.
            </p>
            
            <div className="bg-muted/10 p-6 rounded-lg text-left">
              <ul className="space-y-3">
                <li className="flex items-center gap-3">
                  <div className="w-2 h-2 rounded-full bg-primary"></div>
                  <span>Tests the specific topics covered in this phase</span>
                </li>
                <li className="flex items-center gap-3">
                  <div className="w-2 h-2 rounded-full bg-primary"></div>
                  <span>You must meet the pass threshold to unlock the next phase</span>
                </li>
                <li className="flex items-center gap-3">
                  <div className="w-2 h-2 rounded-full bg-primary"></div>
                  <span>If you don't pass, we'll provide targeted resources to help you review</span>
                </li>
              </ul>
            </div>
          </CardContent>
          <CardFooter className="flex justify-center mt-4">
            <Button size="lg" onClick={handleStart} disabled={isLoading || !phaseId}>
              {isLoading ? 'Preparing...' : 'Start Mastery Test'}
            </Button>
          </CardFooter>
        </Card>
      </div>
    </AppLayout>
  );
};
