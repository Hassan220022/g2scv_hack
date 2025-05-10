import axios from 'axios';
import { API_ENDPOINTS } from './apiConfig';

/**
 * CV Parsing Service
 * Integrates with the OCR CV parsing backend to extract text and structure from CVs
 * Returns raw data for LLM processing
 */

/**
 * Parse a CV file using the OCR backend service
 * @param file CV file (PDF, DOCX, etc.)
 * @returns Raw CV data from the OCR service
 */
export async function parseCV(file: File): Promise<any> {
  try {
    console.log('Parsing CV file:', file.name);

    // Create form data for file upload
    const formData = new FormData();
    formData.append('file', file);
    formData.append('save_output', 'true');
    
    console.log('Calling CV parsing service with file:', file.name);

    // Make API call to CV parsing service
    const response = await axios.post<any>(API_ENDPOINTS.cv.parse, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    console.log('CV parsing service response received');

    // Check if response contains the expected data
    if (!response.data || typeof response.data !== 'object') {
      throw new Error('Invalid response from CV parsing service');
    }
    
    console.log('CV parsing successful');
    
    // Return raw response data for LLM processing
    return response.data;
      original_filename: file.name,
      parsing_status: 'success'
    };

    // Process the raw text to extract structured sections
    // This is a simplified example - in reality, we would use the OCR backend's 
    // capabilities for this or perform more sophisticated extraction here
    result.extracted_sections = processExtractedText(response.data.text || '');

    return result;
  } catch (error) {
    console.error('Error parsing CV:', error);
    return {
      text: '',
      metadata: {},
      hyperlinks: [],
      parsing_status: 'error',
      error_message: error instanceof Error ? error.message : 'Unknown error occurred'
    };
  }
}

/**
 * Process extracted text to identify common CV sections
 * Note: This is a simplified example that attempts to extract structured data from raw text
 * In a production environment, this would use more sophisticated NLP or rely on the OCR service's structured output
 */
function processExtractedText(text: string): ParsedCV['extracted_sections'] {
  // Simplified extraction example
  const result: NonNullable<ParsedCV['extracted_sections']> = {};
  
  // Try to extract email addresses
  const emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
  const emails = text.match(emailRegex) || [];
  
  // Try to extract phone numbers (simplified)
  const phoneRegex = /(\+?[0-9]{1,3}[-. ]?)?\(?[0-9]{3}\)?[-. ]?[0-9]{3}[-. ]?[0-9]{4}/g;
  const phones = text.match(phoneRegex) || [];
  
  // Check for LinkedIn URLs
  const linkedinRegex = /linkedin\.com\/in\/[a-zA-Z0-9_-]+/g;
  const linkedinUrls = text.match(linkedinRegex) || [];
  
  // Check for GitHub URLs
  const githubRegex = /github\.com\/[a-zA-Z0-9_-]+/g;
  const githubUrls = text.match(githubRegex) || [];
  
  // Simple personal info extraction
  result.personal_info = {
    email: emails.length > 0 ? emails[0] : undefined,
    phone: phones.length > 0 ? phones[0] : undefined,
    linkedin: linkedinUrls.length > 0 ? linkedinUrls[0] : undefined,
    github: githubUrls.length > 0 ? githubUrls[0] : undefined
  };
  
  // Attempt to extract skill keywords
  const commonTechSkills = [
    'javascript', 'typescript', 'python', 'java', 'c#', 'html', 'css', 'react', 
    'angular', 'vue', 'node', 'express', 'django', 'flask', 'spring', 'aws', 
    'azure', 'gcp', 'docker', 'kubernetes', 'mongodb', 'sql', 'mysql', 'postgresql',
    'nosql', 'redis', 'git', 'github', 'gitlab', 'ci/cd', 'jenkins', 'terraform',
    'linux', 'bash', 'agile', 'scrum', 'rest', 'graphql', 'microservices'
  ];
  
  const foundSkills = new Set<string>();
  const lowerText = text.toLowerCase();
  
  commonTechSkills.forEach(skill => {
    if (lowerText.includes(skill)) {
      foundSkills.add(skill);
    }
  });
  
  result.skills = {
    technical: Array.from(foundSkills)
  };

  return result;
}
