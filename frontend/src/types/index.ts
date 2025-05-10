export interface FormData {
  linkedInUrl: string;
  githubUsername: string;
  cvFile: File | null;
  jobDescription: string;
}

export interface ValidationErrors {
  linkedInUrl?: string;
  githubUsername?: string;
  cvFile?: string;
  jobDescription?: string;
}

export type FormStatus = 'idle' | 'submitting' | 'success' | 'error';