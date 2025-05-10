import React, { useState } from 'react';
import { Linkedin } from 'lucide-react';
import { validateLinkedInUrl } from '../../utils/validation';

interface LinkedInInputProps {
  value: string;
  onChange: (value: string) => void;
  error?: string;
}

const LinkedInInput: React.FC<LinkedInInputProps> = ({ value, onChange, error }) => {
  const [isFocused, setIsFocused] = useState(false);
  const [localError, setLocalError] = useState<string | undefined>(undefined);
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange(e.target.value);
    setLocalError(undefined);
  };
  
  const handleBlur = () => {
    setIsFocused(false);
    setLocalError(validateLinkedInUrl(value));
  };

  const containerStyle = {
    marginBottom: "16px",
  };

  const labelStyle = {
    display: "block",
    fontSize: "14px",
    fontWeight: "500",
    color: "#374151",
    marginBottom: "4px",
  };

  const inputContainerStyle = {
    display: "flex",
    alignItems: "center",
    border: `1px solid ${isFocused ? '#3b82f6' : error || localError ? '#ef4444' : '#d1d5db'}`,
    borderRadius: "6px",
    overflow: "hidden",
  };

  const iconContainerStyle = {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#f9fafb",
    padding: "8px 12px",
    color: "#6b7280",
  };

  const inputStyle = {
    flex: "1",
    padding: "8px 12px",
    border: "none",
    outline: "none",
  };

  const errorStyle = {
    marginTop: "4px",
    fontSize: "14px",
    color: "#ef4444",
  };

  return (
    <div style={containerStyle}>
      <label htmlFor="linkedin" style={labelStyle}>
        LinkedIn URL
      </label>
      <div style={inputContainerStyle}>
        <div style={iconContainerStyle}>
          <Linkedin size={20} />
        </div>
        <input
          id="linkedin"
          type="text"
          value={value}
          onChange={handleChange}
          onFocus={() => setIsFocused(true)}
          onBlur={handleBlur}
          placeholder="https://linkedin.com/in/username"
          style={inputStyle}
        />
      </div>
      {(error || localError) && (
        <p style={errorStyle}>{error || localError}</p>
      )}
    </div>
  );
};

export default LinkedInInput;