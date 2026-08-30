import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { AppLayout } from '../components/layout/AppLayout';
import { Button } from '../components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '../components/ui/Card';
import { Loader } from '../components/ui/Loader';
import { assessmentService } from '../services/api';
import type { AssessmentStartResponse, AnswerSubmit } from '../types/schemas';
import './Assessment.css';

export const Assessment: React.FC = () => {
  const { attemptId } = useParams<{ attemptId: string }>();
  const navigate = useNavigate();
  
  const [assessment, setAssessment] = useState<AssessmentStartResponse | null>(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({}); // question_id -> option_id
  
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAssessment = async () => {
      if (!attemptId) return;
      try {
        const data = await assessmentService.getAttempt(attemptId);
        setAssessment(data);
      } catch (err: any) {
        console.error(err);
        setError("Failed to load assessment. It may have already been submitted or expired.");
      } finally {
        setIsLoading(false);
      }
    };
    fetchAssessment();
  }, [attemptId]);

  if (isLoading) return <AppLayout><Loader fullScreen message="Loading assessment..." /></AppLayout>;
  
  if (error || !assessment) {
    return (
      <AppLayout>
        <div className="container py-12 max-w-2xl text-center">
          <div className="alert-error mb-6">{error || "Assessment not found"}</div>
          <Button onClick={() => navigate('/dashboard')}>Return to Dashboard</Button>
        </div>
      </AppLayout>
    );
  }

  const currentQuestion = assessment.questions[currentQuestionIndex];
  const isLastQuestion = currentQuestionIndex === assessment.questions.length - 1;
  const isReviewMode = currentQuestionIndex >= assessment.questions.length;
  const progress = ((currentQuestionIndex) / assessment.questions.length) * 100;

  const handleOptionSelect = (optionId: string) => {
    setAnswers(prev => ({
      ...prev,
      [currentQuestion.id]: optionId
    }));
  };

  const handleNext = () => {
    if (currentQuestionIndex <= assessment.questions.length) {
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
      const submissionList: AnswerSubmit[] = Object.entries(answers).map(([question_id, selected_option_id]) => ({
        question_id,
        selected_option_id
      }));
      
      await assessmentService.submit(attemptId, { answers: submissionList });
      navigate(`/assessment/${attemptId}/result`);
    } catch (err: any) {
      console.error(err);
      setError("Failed to submit assessment. Please try again.");
      setIsSubmitting(false);
    }
  };

  if (isReviewMode) {
    return (
      <AppLayout>
        <div className="container py-12 max-w-3xl">
          {error && <div className="alert-error mb-6">{error}</div>}
          <Card>
            <CardHeader className="text-center">
              <CardTitle>Review & Submit</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-center text-muted mb-8">
                You have answered {Object.keys(answers).length} out of {assessment.questions.length} questions.
              </p>
              
              <div className="space-y-4 max-h-[60vh] overflow-y-auto p-4 border rounded">
                {assessment.questions.map((q, idx) => {
                  const answeredOptId = answers[q.id];
                  const answeredOpt = q.options.find(o => o.id === answeredOptId);
                  return (
                    <div key={q.id} className="p-4 bg-muted/30 rounded-md">
                      <div className="flex justify-between items-start mb-2">
                        <span className="font-semibold text-sm">Question {idx + 1}</span>
                        <Button variant="outline" size="sm" onClick={() => setCurrentQuestionIndex(idx)}>Edit</Button>
                      </div>
                      <p className="text-sm mb-2">{q.question}</p>
                      <p className="text-sm font-medium">
                        Answer: <span className={answeredOpt ? 'text-primary' : 'text-red-500'}>
                          {answeredOpt ? answeredOpt.text : 'Not answered'}
                        </span>
                      </p>
                    </div>
                  );
                })}
              </div>
            </CardContent>
            <CardFooter className="flex justify-between mt-6">
              <Button variant="outline" onClick={handlePrevious} disabled={isSubmitting}>Back to Last Question</Button>
              <Button onClick={handleSubmit} disabled={isSubmitting}>
                {isSubmitting ? 'Submitting...' : 'Submit Assessment'}
              </Button>
            </CardFooter>
          </Card>
        </div>
      </AppLayout>
    );
  }

  const selectedOptionId = answers[currentQuestion.id];

  return (
    <AppLayout>
      <div className="container py-8 max-w-3xl">
        <div className="mb-8">
          <div className="flex justify-between text-sm text-muted mb-2">
            <span>Question {currentQuestionIndex + 1} of {assessment.questions.length}</span>
            <span className="capitalize">{currentQuestion.difficulty}</span>
          </div>
          <div className="h-2 w-full bg-border rounded-full overflow-hidden">
            <div className="h-full bg-primary transition-all duration-300" style={{ width: `${progress}%` }}></div>
          </div>
        </div>

        <Card className="assessment-card">
          <CardHeader>
            <div className="text-xs font-semibold uppercase tracking-wider text-primary mb-2">
              {currentQuestion.skill}
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
            <Button 
              onClick={handleNext}
              disabled={!selectedOptionId}
            >
              {isLastQuestion ? 'Review & Submit' : 'Next'}
            </Button>
          </CardFooter>
        </Card>
      </div>
    </AppLayout>
  );
};
