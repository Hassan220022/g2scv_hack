/**
 * Resume Service
 * 
 * Integrates all backend services (LinkedIn scraping via Apify, GitHub scraping,
 * and CV parsing) to generate optimized ATS-friendly resumes tailored to job descriptions.
 * Uses an LLM backend with RAG to generate highly customized resumes.
 */

import axios from 'axios';
import { API_ENDPOINTS } from './apiConfig';
import { scrapeLinkedInProfile } from './linkedInService';
import { scrapeGitHubProjects } from './githubService';
import { parseCV as parseCVFile } from './cvParserService';
import { 
  mockScrapeLinkedIn, 
  mockScrapeGithub, 
  mockParseCV, 
  mockGenerateResume 
} from './mockBackend';

// For hackathon demo, use mock backend if specified in .env
const USE_MOCK_BACKEND = (import.meta.env.VITE_USE_MOCK_BACKEND === 'true');

/**
 * Scrape LinkedIn profile data
 * @param linkedInUrl LinkedIn profile URL
 * @returns Raw LinkedIn profile data from Apify
 */
export async function scrapeLinkedIn(linkedInUrl: string): Promise<any> {
  try {
    // For hackathon or demo, use mock data if enabled
    if (USE_MOCK_BACKEND) {
      console.log('Using mock LinkedIn data');
      return mockScrapeLinkedIn(linkedInUrl);
    }
    
    console.log('Scraping LinkedIn profile:', linkedInUrl);
    // Use the dedicated LinkedIn service with Apify integration
    // Now returns raw data instead of transformed data
    return await scrapeLinkedInProfile(linkedInUrl);
  } catch (error) {
    console.error('Error scraping LinkedIn:', error);
    throw error;
  }
}

/**
 * Scrape GitHub data including repositories and README content
 * @param githubUsername GitHub username
 * @returns Raw GitHub data with repositories and README content
 */
export async function scrapeGithub(githubUsername: string): Promise<any> {
  try {
    // For hackathon or demo, use mock data if enabled
    if (USE_MOCK_BACKEND) {
      console.log('Using mock GitHub data');
      return mockScrapeGithub(githubUsername);
    }
    
    console.log('Scraping GitHub data for user:', githubUsername);
    // Use the dedicated GitHub service - now returns raw data
    return await scrapeGitHubProjects(githubUsername);
  } catch (error) {
    console.error('Error scraping GitHub:', error);
    throw error;
  }
}

/**
 * Parse CV file to extract structured data
 * @param cvFile CV file (PDF, DOCX, etc.)
 * @returns Raw CV data from the OCR service
 */
export async function parseCV(cvFile: File): Promise<any> {
  try {
    // For hackathon or demo, use mock data if enabled
    if (USE_MOCK_BACKEND) {
      console.log('Using mock CV parsing');
      return mockParseCV(cvFile);
    }
    
    console.log('Parsing CV file:', cvFile.name);
    // Use the dedicated CV parsing service - now returns raw data
    return await parseCVFile(cvFile);
  } catch (error) {
    console.error('Error parsing CV:', error);
    throw error;
  }
}

/**
 * Main function to generate an ATS-optimized resume using LLM with RAG
 * @param linkedInData Raw LinkedIn profile data
 * @param githubData Raw GitHub repositories and README data
 * @param cvData Raw CV parsed data
 * @param jobDescription Job description to tailor the resume for
 * @returns Generated LaTeX code and PDF as a Blob
 */
export async function generateResume(
  linkedInData: any,
  githubData: any,
  cvData: any,
  jobDescription: string
): Promise<{latex: string, pdf: Blob}> {
  // For hackathon or demo, use mock implementation if enabled
  if (USE_MOCK_BACKEND) {
    console.log('Using mock resume generation');
    const pdfBlob = mockGenerateResume(linkedInData, githubData, cvData, jobDescription);
    return { latex: '\\documentclass{article}\n\\begin{document}\nMock LaTeX Content\n\\end{document}', pdf: pdfBlob };
  }
  
  try {
    console.log('Sending data to LLM service for ATS-optimized resume generation');
    
    // Prepare the request payload with all the raw data
    const payload = {
      linkedInData,
      githubData,
      cvData,
      jobDescription,
      // Include the ATS-optimized CV template
      resumeTemplate: {
        format: 'latex',
        // This tells the LLM to use the LaTeX template provided in the user's request
        templateType: 'ats_optimized'
      }
    };
    
    console.log('Calling resume generation API...');
    
    // Send all data to the LLM-powered resume generation service
    const response = await axios.post(
      API_ENDPOINTS.resume.generate,
      payload,
      { 
        responseType: 'json',
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );
    
    console.log('Resume generated successfully');
    
    // The response should contain both the LaTeX source and the compiled PDF
    const latex = response.data.latex;
    
    // Convert the base64 PDF to a Blob
    const pdfBase64 = response.data.pdf;
    const byteCharacters = atob(pdfBase64);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    const pdf = new Blob([byteArray], {type: 'application/pdf'});
    
    return {
      latex,
      pdf
    };
  } catch (error) {
    console.error('Error generating resume:', error);
    throw error;
  }
}

/**
 * Main function to generate an optimized resume using data from all sources
 * @param linkedInData LinkedIn profile data
 * @param githubData GitHub repositories and skills data
 * @param cvData Parsed CV data
 * @param jobDescription Job description to tailor the resume for
 * @returns Generated PDF as a Blob
 */
export async function generateResume(
  linkedInData: any,
  githubData: any,
  cvData: any,
  jobDescription: string
): Promise<Blob> {
  // For hackathon or demo, use mock implementation if enabled
  if (USE_MOCK_BACKEND) {
    console.log('Using mock resume generation');
    return mockGenerateResume(linkedInData, githubData, cvData, jobDescription);
  }
  
  try {
    console.log('Generating optimized resume with integrated data');
    
    // Prepare the combined data from all sources
    const combinedData = {
      // Personal info (prioritize CV data, supplement with LinkedIn)
      personalInfo: {
        name: cvData?.content?.personal_info?.name || 
              `${linkedInData?.firstName || ''} ${linkedInData?.lastName || ''}`.trim(),
        email: cvData?.content?.personal_info?.email || '',
        phone: cvData?.content?.personal_info?.phone || '',
        location: cvData?.content?.personal_info?.location || linkedInData?.location || '',
        linkedin: linkedInData ? linkedInData.inputUrl : cvData?.content?.personal_info?.linkedin || '',
        github: githubData ? `https://github.com/${githubData.username}` : cvData?.content?.personal_info?.github || '',
      },
      
      // Summary (use LinkedIn summary if available, otherwise from CV)
      summary: linkedInData?.summary || cvData?.content?.summary || '',
      
      // Experience (combine and deduplicate from LinkedIn and CV)
      experience: mergeExperience(
        linkedInData?.positions || [], 
        cvData?.content?.experience || []
      ),
      
      // Education (combine and deduplicate from LinkedIn and CV)
      education: mergeEducation(
        linkedInData?.educations || [], 
        cvData?.content?.education || []
      ),
      
      // Skills (combine from all sources)
      skills: mergeSkills(
        linkedInData?.skills || [],
        githubData?.skills || [],
        cvData?.content?.skills?.technical || []
      ),
      
      // Projects (primarily from GitHub, supplement with CV)
      projects: githubData?.repositories || cvData?.content?.projects || [],
      
      // Certifications (from LinkedIn or CV)
      certifications: linkedInData?.certifications || cvData?.content?.certifications || [],
      
      // Job description for tailoring
      jobDescription: jobDescription
    };
    
    // In a real application, send this data to a backend service that generates the resume
    const response = await axios.post(
      API_ENDPOINTS.resume.generate,
      combinedData,
      { responseType: 'blob' }
    );
    
    return response.data;
  } catch (error) {
    console.error('Error generating resume:', error);
    
    // Fallback: Return the original CV if available
    if (cvData && cvData.originalFile) {
      console.log('Using original CV as fallback');
      return cvData.originalFile;
    }
    
    throw error;
  }
}

/**
 * Helper function to merge experience entries from LinkedIn and CV
 * Deduplicates based on company name and position
 */
function mergeExperience(
  linkedInExperience: Array<{title?: string, companyName?: string, dateRange?: string, description?: string, location?: string}>,
  cvExperience: Array<{position?: string, company?: string, date_range?: string, description?: string, location?: string}>
): Array<{title: string, company: string, dateRange: string, description: string, location: string}> {
  const normalizedLinkedIn = linkedInExperience.map(exp => ({
    title: exp.title || '',
    company: exp.companyName || '',
    dateRange: exp.dateRange || '',
    description: exp.description || '',
    location: exp.location || ''
  }));
  
  const normalizedCV = cvExperience.map(exp => ({
    title: exp.position || '',
    company: exp.company || '',
    dateRange: exp.date_range || '',
    description: exp.description || '',
    location: exp.location || ''
  }));
  
  // Combine and deduplicate - prefer LinkedIn data when duplicates exist
  const combined = [...normalizedLinkedIn];
  
  for (const cvExp of normalizedCV) {
    const isDuplicate = normalizedLinkedIn.some(linkedInExp => 
      isSimilarString(cvExp.company, linkedInExp.company) && 
      isSimilarString(cvExp.title, linkedInExp.title)
    );
    
    if (!isDuplicate) {
      combined.push(cvExp);
    }
  }
  
  return combined;
}

/**
 * Helper function to merge education entries from LinkedIn and CV
 * Deduplicates based on institution and degree
 */
function mergeEducation(
  linkedInEducation: Array<{schoolName?: string, degree?: string, dateRange?: string, description?: string}>,
  cvEducation: Array<{institution?: string, degree?: string, field?: string, date_range?: string}>
): Array<{school: string, degree: string, dateRange: string, description: string}> {
  const normalizedLinkedIn = linkedInEducation.map(edu => ({
    school: edu.schoolName || '',
    degree: edu.degree || '',
    dateRange: edu.dateRange || '',
    description: edu.description || ''
  }));
  
  const normalizedCV = cvEducation.map(edu => ({
    school: edu.institution || '',
    degree: `${edu.degree || ''} ${edu.field || ''}`.trim(),
    dateRange: edu.date_range || '',
    description: ''
  }));
  
  // Combine and deduplicate - prefer LinkedIn data when duplicates exist
  const combined = [...normalizedLinkedIn];
  
  for (const cvEdu of normalizedCV) {
    const isDuplicate = normalizedLinkedIn.some(linkedInEdu => 
      isSimilarString(cvEdu.school, linkedInEdu.school) && 
      isSimilarString(cvEdu.degree, linkedInEdu.degree)
    );
    
    if (!isDuplicate) {
      combined.push(cvEdu);
    }
  }
  
  return combined;
}

/**
 * Helper function to merge skills from all sources
 * Deduplicates and returns a unique list
 */
function mergeSkills(
  linkedInSkills: string[],
  githubSkills: string[],
  cvSkills: string[]
): string[] {
  const skillSet = new Set<string>();
  
  // Add all skills to the set, which automatically deduplicates
  [...linkedInSkills, ...githubSkills, ...cvSkills].forEach(skill => {
    if (skill && skill.trim()) {
      skillSet.add(skill.trim());
    }
  });
  
  return Array.from(skillSet);
}

/**
 * Helper function to check if two strings are similar
 * Used for deduplicating entries from different sources
 */
function isSimilarString(str1?: string, str2?: string): boolean {
  if (!str1 || !str2) return false;
  
  const normalize = (s: string) => s.toLowerCase().trim();
  const normalized1 = normalize(str1);
  const normalized2 = normalize(str2);
  
  // Exact match or one is a substring of the other
  return normalized1 === normalized2 || 
         normalized1.includes(normalized2) || 
         normalized2.includes(normalized1);
}