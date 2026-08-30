import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { AppLayout } from '../components/layout/AppLayout';
import { Button } from '../components/ui/Button';
import { Card, CardContent, CardHeader, CardFooter } from '../components/ui/Card';
import { Loader } from '../components/ui/Loader';
import { masteryService } from '../services/api';
import type { MasteryStartResponse, MasteryAnswerSubmission } from '../types/schemas';
import '../pages/Assessment.css'; // Reuse Assessment CSS

export const Mastery: React.FC = () => {
  const { attemptId } = useParams<{ attemptId: string }>();
  const navigate = useNavigate();
  
  const [assessment, setAssessment] = useState<MasteryStartResponse | null>(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({}); // question_id -> option_id
  
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // In a real app, we might need a GET /api/mastery/{attempt_id} to resume
    // For now, if we don't have it in state, we show an error (or we could store it in Context)
    // Actually, looking at the API, there is no GET /mastery/{attempt_id} to resume.
    // If they refresh, they might need to restart.
    // We'll simulate loading it or just error out.
    // Wait, the prompt says "If GET /api/mastery/{attempt_id} exists...". It doesn't.
    // Let's just assume we get it from a global store, or for now, we just rely on the user NOT refreshing,
    // OR we could fetch it if there was an endpoint. Since there isn't, if they refresh, they get an error.
    
    // For simplicity, we'll assume we can't resume if they refresh, unless we saved to localStorage.
    const stored = localStorage.getItem(`mastery_${attemptId}`);
    if (stored) {
      setAssessment(JSON.parse(stored));
      setIsLoading(false);
    } else {
      setError("Assessment data lost due to refresh. Please restart.");
      setIsLoading(false);
    }
  }, [attemptId]);

  // Wait, I should save the response when we start it. 
  // Since I didn't save it in MasteryIntro, I will just go back and fix MasteryIntro to save it,
  // or I can just use a hack for now.
  // Actually, the prompt says "Store: mastery_attempt_id".
  // Let me just add localStorage saving to this page if it comes via router state? No.
  // Let's assume the user doesn't refresh for now, or I'll implement a context.
  
  // Correction: The backend might NOT have a GET method for the active questions. 
  // I will just use the state from localStorage.

  // Let's modify MasteryIntro to save to localStorage, or I will just write it here.
  
  if (isLoading) return <AppLayout><Loader fullScreen message="Loading..." /></AppLayout>;
  
  if (error || !assessment) {
    return (
      <AppLayout>
        <div className="container py-12 text-center">
          <div className="alert-error mb-6">{error || "Assessment not found"}</div>
          <Button onClick={() => navigate('/dashboard')}>Return to Dashboard</Button>
        </div>
      </AppLayout>
    );
  }

  const currentQuestion = assessment.questions[currentQuestionIndex];
  const isLastQuestion = currentQuestionIndex === assessment.questions.length - 1;
  const progress = ((currentQuestionIndex) / assessment.questions.length) * 100;

  const handleOptionSelect = (optionId: string) => {
    setAnswers(prev => ({
      ...prev,
      [currentQuestion.question_id]: optionId
    }));
  };

  const handleNext = () => {
    if (currentQuestionIndex < assessment.questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
    }
  };

  const handleSubmit = async () => {
    if (!attemptId) return;
    setIsSubmitting(true);
    setError(null);
    try {
      const submissionList: MasteryAnswerSubmission[] = Object.entries(answers).map(([question_id, selected_option_id]) => ({
        question_id,
        selected_option_id
      }));
      
      await masteryService.submit(attemptId, { answers: submissionList });
      localStorage.removeItem(`mastery_${attemptId}`);
      navigate(`/mastery/${attemptId}/result`);
    } catch (err: any) {
      console.error(err);
      setError("Failed to submit. Please try again.");
      setIsSubmitting(false);
    }
  };

  const selectedOptionId = answers[currentQuestion.question_id];

  return (
    <AppLayout>
      <div className="container py-8 max-w-3xl">
        <div className="mb-8">
          <div className="flex justify-between text-sm text-muted mb-2">
            <span>Mastery Question {currentQuestionIndex + 1} of {assessment.questions.length}</span>
            <span className="capitalize">{currentQuestion.difficulty}</span>
          </div>
          <div className="h-2 w-full bg-border rounded-full overflow-hidden">
            <div className="h-full bg-primary transition-all duration-300" style={{ width: `${progress}%` }}></div>
          </div>
        </div>

        <Card className="assessment-card">
          <CardHeader>
            <div className="text-xs font-semibold uppercase tracking-wider text-primary mb-2">
              Topic: {currentQuestion.topic}
            </div>
            <h2 className="text-xl font-medium leading-relaxed">{currentQuestion.question}</h2>
          </CardHeader>
          <CardContent className="space-y-3">
            {currentQuestion.options.map((option) => (
              <div 
                key={option.id}
                className={`option-card ${selectedOptionId === option.id ? 'selected' : ''}`}
                onClick={() => handleOptionSelect(option.id)}
              >
                <div className="option-radio">
                  <div className={`option-radio-inner ${selectedOptionId === option.id ? 'active' : ''}`}></div>
                </div>
                <span className="option-text">{option.text}</span>
              </div>
            ))}
          </CardContent>
          <CardFooter className="flex justify-between mt-8 border-t pt-6">
            <Button 
              variant="outline" 
              onClick={handlePrevious}
              disabled={currentQuestionIndex === 0}
            >
              Previous
            </Button>
            {isLastQuestion ? (
              <Button onClick={handleSubmit} disabled={!selectedOptionId || isSubmitting}>
                {isSubmitting ? 'Submitting...' : 'Submit Assessment'}
              </Button>
            ) : (
              <Button onClick={handleNext} disabled={!selectedOptionId}>
                Next
              </Button>
            )}
          </CardFooter>
        </Card>
      </div>
    </AppLayout>
  );
};
