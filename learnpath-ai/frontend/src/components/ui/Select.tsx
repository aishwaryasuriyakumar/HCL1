import React, { type SelectHTMLAttributes } from 'react';
import './Input.css';

interface SelectProps extends SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
  helperText?: string;
  options: { value: string; label: string }[];
}

export const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ className = '', label, error, helperText, options, ...props }, ref) => {
    return (
      <div className={`input-wrapper ${className}`}>
        {label && <label className="input-label">{label}</label>}
        <select
          ref={ref}
          className={`input-field ${error ? 'input-error' : ''}`}
          {...props}
        >
          <option value="" disabled>Select an option</option>
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
        {error && <p className="input-error-text">{error}</p>}
        {helperText && !error && <p className="input-helper-text">{helperText}</p>}
      </div>
    );
  }
);
Select.displayName = 'Select';
