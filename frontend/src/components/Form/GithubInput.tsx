import React, { useState } from 'react';
import { Github } from 'lucide-react';
import { validateGithubUsername } from '../../utils/validation';

interface GithubInputProps {
  value: string;
  onChange: (value: string) => void;
  error?: string;
}

const GithubInput: React.FC<GithubInputProps> = ({ value, onChange, error }) => {
  const [isFocused, setIsFocused] = useState(false);
  const [localError, setLocalError] = useState<string | undefined>(undefined);
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange(e.target.value);
    setLocalError(undefined);
  };
  
  const handleBlur = () => {
    setIsFocused(false);
    setLocalError(validateGithubUsername(value));
  };

  return (
    <div className="mb-4">
      <label htmlFor="github" className="block text-sm font-medium text-gray-700 mb-1">
        GitHub Username
      </label>
      <div className={`flex items-center border ${isFocused ? 'border-blue-500 ring-1 ring-blue-500' : error || localError ? 'border-red-500' : 'border-gray-300'} rounded-md overflow-hidden transition-all`}>
        <div className="flex items-center justify-center bg-gray-50 px-3 py-2 text-gray-500">
          <Github size={20} />
        </div>
        <input
          id="github"
          type="text"
          value={value}
          onChange={handleChange}
          onFocus={() => setIsFocused(true)}
          onBlur={handleBlur}
          placeholder="username"
          className="flex-1 px-3 py-2 focus:outline-none"
        />
      </div>
      {(error || localError) && (
        <p className="mt-1 text-sm text-red-500">{error || localError}</p>
      )}
    </div>
  );
};

export default GithubInput;