import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AppLayout } from '../components/layout/AppLayout';
import { Button } from '../components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '../components/ui/Card';
import { assessmentService } from '../services/api';
import { auth } from '../utils/auth';

export const AssessmentIntro: React.FC = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleStart = async () => {
    const userId = auth.getCurrentUserId();
    if (!userId) {
      setError("User session not found. Please return to onboarding.");
      return;
    }
    
    setIsLoading(true);
    setError(null);
    try {
      const response = await assessmentService.start(userId);
      navigate(`/assessment/${response.attempt_id}`);
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || "Failed to start assessment. Please try again.");
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
            <CardTitle className="text-2xl">Diagnostic Skill Assessment</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6 text-center">
            <p className="text-lg text-muted">
              Let's understand your current skill level before creating your personalized learning path.
            </p>
            
            <div className="grid md:grid-cols-3 gap-6 my-8 text-left">
              <div className="p-4 border rounded-md">
                <h4 className="font-semibold mb-2 text-primary">15 Questions</h4>
                <p className="text-sm text-muted">A quick test covering your selected domain.</p>
              </div>
              <div className="p-4 border rounded-md">
                <h4 className="font-semibold mb-2 text-primary">No Penalty</h4>
                <p className="text-sm text-muted">It's okay to guess or select 'I don't know' if available.</p>
              </div>
              <div className="p-4 border rounded-md">
                <h4 className="font-semibold mb-2 text-primary">Personalized</h4>
                <p className="text-sm text-muted">Results are used to craft a roadmap just for you.</p>
              </div>
            </div>
            
            <p className="font-medium">
              Find a quiet place and focus. This should take about 10-15 minutes.
            </p>
          </CardContent>
          <CardFooter className="flex justify-center mt-4">
            <Button size="lg" onClick={handleStart} disabled={isLoading}>
              {isLoading ? 'Preparing Assessment...' : 'Start Assessment'}
            </Button>
          </CardFooter>
        </Card>
      </div>
    </AppLayout>
  );
};
