import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Home } from './pages/Home';
import { Onboarding } from './pages/Onboarding';
import { Dashboard } from './pages/Dashboard';
import { AssessmentIntro } from './pages/AssessmentIntro';
import { Assessment } from './pages/Assessment';
import { AssessmentResultPage } from './pages/AssessmentResult';
import { SkillGapPage } from './pages/SkillGap';
import { PathResult } from './pages/PathResult';
import { MasteryIntro } from './pages/MasteryIntro';
import { Mastery } from './pages/Mastery';
import { MasteryResultPage } from './pages/MasteryResult';
import { auth } from './utils/auth';
import { GeneratePath } from './pages/GeneratePath';


// Simple PrivateRoute wrapper
const PrivateRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  if (!auth.isAuthenticated()) {
    return <Navigate to="/onboarding" replace />;
  }
  return <>{children}</>;
};

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public / Landing Route */}
        <Route path="/" element={<Home />} />
        
        {/* Onboarding Flow (Creates User Session) */}
        <Route path="/onboarding" element={<Onboarding />} />
        
        {/* Diagnostic Assessment Flow */}
        <Route path="/assessment/intro" element={
          <PrivateRoute><AssessmentIntro /></PrivateRoute>
        } />
        <Route path="/assessment/:attemptId" element={
          <PrivateRoute><Assessment /></PrivateRoute>
        } />
        <Route path="/assessment/:attemptId/result" element={
          <PrivateRoute><AssessmentResultPage /></PrivateRoute>
        } />
        
        {/* Skill Gap Analysis Flow */}
        <Route path="/skill-gap" element={
          <PrivateRoute><SkillGapPage /></PrivateRoute>
        } />
        
        {/* Learning Path & Resources Flow */}
        <Route path="/path/:pathId" element={
          <PrivateRoute><PathResult /></PrivateRoute>
        } />
          <Route path="/generate" element={<PrivateRoute><GeneratePath /></PrivateRoute>} />
        
        {/* Mastery Flow */}
        <Route path="/mastery/intro/:phaseId" element={
          <PrivateRoute><MasteryIntro /></PrivateRoute>
        } />
        <Route path="/mastery/:attemptId" element={
          <PrivateRoute><Mastery /></PrivateRoute>
        } />
        <Route path="/mastery/:attemptId/result" element={
          <PrivateRoute><MasteryResultPage /></PrivateRoute>
        } />
        
        {/* Main Dashboard */}
        <Route path="/dashboard" element={
          <PrivateRoute><Dashboard /></PrivateRoute>
        } />
        
        {/* Fallback route */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
};
