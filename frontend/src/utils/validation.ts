import { ValidationErrors, FormData } from '../types';

export function validateLinkedInUrl(url: string): string | undefined {
  if (!url.trim()) {
    return 'LinkedIn URL is required';
  }
  
  const linkedInPattern = /^(https?:\/\/)?(www\.)?linkedin\.com\/in\/[\w-]+\/?$/i;
  if (!linkedInPattern.test(url)) {
    return 'Please enter a valid LinkedIn profile URL (e.g., https://linkedin.com/in/username)';
  }
  
  return undefined;
}

export function validateGithubUsername(username: string): string | undefined {
  if (!username.trim()) {
    return 'GitHub username is required';
  }

  const githubUsernamePattern = /^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$/i;
  if (!githubUsernamePattern.test(username)) {
    return 'Please enter a valid GitHub username';
  }
  
  return undefined;
}

export function validateCvFile(file: File | null): string | undefined {
  if (!file) {
    return 'CV file is required';
  }
  
  if (file.type !== 'application/pdf') {
    return 'Only PDF files are accepted';
  }
  
  // 10MB limit
  if (file.size > 10 * 1024 * 1024) {
    return 'File size should be less than 10MB';
  }
  
  return undefined;
}

export function validateJobDescription(description: string): string | undefined {
  // Job description is optional, so no validation if empty
  if (!description.trim()) {
    return undefined;
  }
  
  // Check if it's too short to be useful
  if (description.trim().length < 10) {
    return 'Job description should be at least 10 characters';
  }
  
  // Check if it's too long
  if (description.trim().length > 10000) {
    return 'Job description should be less than 10,000 characters';
  }
  
  return undefined;
}

export function validateForm(data: FormData): ValidationErrors {
  const errors: ValidationErrors = {};
  
  const linkedInError = validateLinkedInUrl(data.linkedInUrl);
  if (linkedInError) errors.linkedInUrl = linkedInError;
  
  const githubError = validateGithubUsername(data.githubUsername);
  if (githubError) errors.githubUsername = githubError;
  
  const cvFileError = validateCvFile(data.cvFile);
  if (cvFileError) errors.cvFile = cvFileError;
  
  const jobDescriptionError = validateJobDescription(data.jobDescription);
  if (jobDescriptionError) errors.jobDescription = jobDescriptionError;
  
  return errors;
}