import React, { type HTMLAttributes, type ReactNode } from 'react';
import './Card.css';

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  children?: ReactNode;
  className?: string;
}

export const Card: React.FC<CardProps> = ({ children, className = '', ...props }) => {
  return <div className={`card ${className}`} {...props}>{children}</div>;
};

export const CardHeader: React.FC<CardProps> = ({ children, className = '', ...props }) => {
  return <div className={`card-header ${className}`} {...props}>{children}</div>;
};

export const CardTitle: React.FC<CardProps> = ({ children, className = '', ...props }) => {
  return <h3 className={`card-title ${className}`} {...props}>{children}</h3>;
};

export const CardContent: React.FC<CardProps> = ({ children, className = '', ...props }) => {
  return <div className={`card-content ${className}`} {...props}>{children}</div>;
};

export const CardFooter: React.FC<CardProps> = ({ children, className = '', ...props }) => {
  return <div className={`card-footer ${className}`} {...props}>{children}</div>;
};
