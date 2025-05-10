import React, { useState } from 'react';
import { FormData, ValidationErrors, FormStatus } from '../../types';
import { validateForm } from '../../utils/validation';
import LinkedInInput from './LinkedInInput';
import GithubInput from './GithubInput';
import FileUpload from './FileUpload';
import Button from '../ui/Button';
import { RefreshCw } from 'lucide-react';

interface InputFormProps {
  onSubmit: (data: FormData) => void;
  status: FormStatus;
}

const InputForm: React.FC<InputFormProps> = ({ onSubmit, status }) => {
  const [formData, setFormData] = useState<FormData>({
    linkedInUrl: '',
    githubUsername: '',
    cvFile: null,
    jobDescription: '',
  });
  
  const [errors, setErrors] = useState<ValidationErrors>({});
  
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    const validationErrors = validateForm(formData);
    setErrors(validationErrors);
    
    if (Object.keys(validationErrors).length === 0) {
      onSubmit(formData);
    }
  };
  
  const updateFormData = <K extends keyof FormData>(key: K, value: FormData[K]) => {
    setFormData(prev => ({ ...prev, [key]: value }));
    // Clear error when field is updated
    if (errors[key]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[key];
        return newErrors;
      });
    }
  };

  const formStyle = {
    width: "100%",
    maxWidth: "500px",
    margin: "0 auto",
    padding: "20px",
  };
  
  const inputGroupStyle = {
    marginBottom: "20px",
  };
  
  const labelStyle = {
    display: "block",
    marginBottom: "8px",
    fontWeight: "500",
    color: "#374151",
  };
  
  const inputStyle = {
    width: "100%",
    padding: "10px",
    border: "1px solid #d1d5db",
    borderRadius: "6px",
  };
  
  const buttonStyle = {
    backgroundColor: "#2563eb",
    color: "white",
    padding: "10px 16px",
    borderRadius: "6px",
    fontWeight: "500",
    cursor: "pointer",
    width: "100%",
  };
  
  const errorStyle = {
    color: "#ef4444",
    fontSize: "14px",
    marginTop: "4px",
  };

  return (
    <form onSubmit={handleSubmit} style={formStyle}>
      <h2 style={{ fontSize: "24px", fontWeight: "bold", color: "#111827", marginBottom: "24px" }}>
        Professional Information
      </h2>
      
      <LinkedInInput
        value={formData.linkedInUrl}
        onChange={(value) => updateFormData('linkedInUrl', value)}
        error={errors.linkedInUrl}
      />
      
      <GithubInput
        value={formData.githubUsername}
        onChange={(value) => updateFormData('githubUsername', value)}
        error={errors.githubUsername}
      />
      
      <FileUpload
        onFileChange={(file) => updateFormData('cvFile', file)}
        error={errors.cvFile}
      />
      
      <div style={inputGroupStyle}>
        <label style={labelStyle}>
          Job Description
        </label>
        <textarea
          style={{ ...inputStyle, minHeight: "120px" }}
          placeholder="Paste the job description here to tailor your resume"
          value={formData.jobDescription}
          onChange={(e) => updateFormData('jobDescription', e.target.value)}
        />
        {errors.jobDescription && (
          <p style={errorStyle}>{errors.jobDescription}</p>
        )}
      </div>
      
      <div style={{ marginTop: "24px" }}>
        <button
          type="submit"
          style={buttonStyle}
          disabled={status === 'submitting'}
        >
          {status === 'submitting' ? 'Generating...' : 'Generate Resume'}
        </button>
      </div>
      
      {status === 'error' && (
        <div style={{ marginTop: "16px", padding: "12px", backgroundColor: "#fee2e2", borderRadius: "6px" }}>
          <p style={{ color: "#b91c1c", fontSize: "14px" }}>
            An error occurred while generating your resume. Please try again.
          </p>
        </div>
      )}
    </form>
  );
};

export default InputForm;