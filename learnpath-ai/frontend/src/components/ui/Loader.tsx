import React from 'react';
import './Loader.css';

interface LoaderProps {
  size?: 'sm' | 'md' | 'lg';
  fullScreen?: boolean;
  message?: string;
}

export const Loader: React.FC<LoaderProps> = ({ size = 'md', fullScreen = false, message }) => {
  const content = (
    <div className="loader-container">
      <div className={`loader-spinner loader-${size}`}></div>
      {message && <p className="loader-message">{message}</p>}
    </div>
  );

  if (fullScreen) {
    return <div className="loader-fullscreen">{content}</div>;
  }

  return content;
};
