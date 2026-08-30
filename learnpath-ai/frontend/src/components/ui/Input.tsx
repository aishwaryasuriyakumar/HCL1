import React, { type InputHTMLAttributes } from 'react';
import './Input.css';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className = '', label, error, helperText, ...props }, ref) => {
    return (
      <div className={`input-wrapper ${className}`}>
        {label && <label className="input-label">{label}</label>}
        <input
          ref={ref}
          className={`input-field ${error ? 'input-error' : ''}`}
          {...props}
        />
        {error && <p className="input-error-text">{error}</p>}
        {helperText && !error && <p className="input-helper-text">{helperText}</p>}
      </div>
    );
  }
);
Input.displayName = 'Input';
