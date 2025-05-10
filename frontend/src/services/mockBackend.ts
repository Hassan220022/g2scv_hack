/**
 * Mock Backend Service
 * 
 * This file provides mock implementations of the backend services for the hackathon demo.
 * It allows the frontend to function without requiring actual backend API endpoints.
 */

// Mock delay to simulate network latency
const MOCK_DELAY = 1500;

/**
 * Mock function to simulate LinkedIn profile scraping
 */
export async function mockScrapeLinkedIn(linkedInUrl: string): Promise<any> {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, MOCK_DELAY));
  
  return {
    id: '123456789',
    firstName: 'Hassan',
    lastName: 'Mikawi',
    occupation: 'Software Engineer',
    headline: 'Software Engineer | Python | Django | Flask',
    summary: 'Experienced software engineer with expertise in Python and web development frameworks.',
    positions: [
      {
        title: 'Software Engineer',
        companyName: 'Al-Ahram Establishment',
        dateRange: 'Sep 2024 - Dec 2024',
        description: 'Developed Python scripts to automate data retrieval and built a fully functional agricultural website.',
        location: 'Cairo, Egypt'
      }
    ],
    educations: [
      {
        schoolName: 'Arab Academy for Science, Technology and Maritime Transport',
        degree: "Bachelor's degree in Computer Engineering",
        dateRange: 'Sep 2020 - Aug 2025',
        description: 'Relevant coursework: Software Development, Databases, Cloud Computing'
      }
    ],
    skills: [
      'Python', 'Django', 'Flask', 'SQL', 'React', 'Git', 'Angular'
    ],
    inputUrl: linkedInUrl
  };
}

/**
 * Mock function to simulate GitHub repository scraping
 */
export async function mockScrapeGithub(githubUsername: string): Promise<any> {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, MOCK_DELAY));
  
  return {
    username: githubUsername,
    repositories: [
      {
        name: 'AirBnB_clone_v2',
        description: 'A clone of the Airbnb website using Python, focusing on backend services and RESTful APIs.',
        url: `https://github.com/${githubUsername}/AirBnB_clone_v2`,
        primaryLanguage: 'Python',
        stars: 12,
        forks: 5
      },
      {
        name: 'Portfolio-Website',
        description: 'My personal portfolio website built with React and Tailwind CSS.',
        url: `https://github.com/${githubUsername}/Portfolio-Website`,
        primaryLanguage: 'JavaScript',
        stars: 8,
        forks: 2
      }
    ]
  };
}

/**
 * Mock function to simulate CV parsing
 */
export async function mockParseCV(cvFile: File): Promise<any> {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, MOCK_DELAY));
  
  // Store the original file for potential fallback
  return {
    originalFile: cvFile,
    content: {
      name: 'Hassan Mikawi',
      email: 'hassan@example.com',
      phone: '+201234567890',
      location: 'Cairo, Egypt',
      summary: 'Dynamic software engineer with proven expertise in backend development and a strong proficiency in Python and its frameworks, such as Django and Flask.',
      experience: [
        {
          title: 'Software Engineer',
          company: 'Al-Ahram Establishment',
          location: 'Cairo, Egypt',
          dates: 'Sep 2024 - Dec 2024',
          highlights: [
            'Developed Python scripts to automate data retrieval from Microsoft SQL Server, enhancing efficiency by 30%.',
            'Built a fully functional agricultural website, including both front-end and back-end development, using Python and Angular.',
            'Implemented robust security measures, reducing potential vulnerabilities by 40%.',
            'Optimized website performance to handle high traffic efficiently, improving response times by 20%.'
          ]
        }
      ],
      education: [
        {
          institution: 'Arab Academy for Science, Technology and Maritime Transport',
          degree: "Bachelor's degree in Computer Engineering",
          dates: 'Sep 2020 - Aug 2025',
          coursework: 'Software Development, Databases, Cloud Computing'
        }
      ],
      skills: {
        languages: ['Python', 'C#', 'Java'],
        frameworks: ['Django', 'Flask', '.NET Framework'],
        databases: ['PostgreSQL', 'MySQL', 'SQL Server'],
        webDevelopment: ['Angular', 'React', 'Flask'],
        cloudPlatforms: ['AWS', 'Azure'],
        tools: ['Git', 'Anaconda']
      },
      projects: [
        {
          name: 'AirBnB Clone v2',
          url: 'https://github.com/Hassan220022/AirBnB_clone_v2',
          description: 'Developed a clone of the Airbnb website using Python, focusing on backend services and RESTful APIs.'
        }
      ]
    }
  };
}

/**
 * Mock function to simulate resume generation
 */
export async function mockGenerateResume(
  linkedInData: any,
  githubData: any,
  cvData: any,
  jobDescription: string
): Promise<Blob> {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, MOCK_DELAY * 2));
  
  // For demo purposes, just return the original CV file
  if (cvData && cvData.originalFile) {
    return cvData.originalFile;
  }
  
  // If no original file, create a simple PDF (this won't actually work without a PDF library)
  const dummyText = 'This is a placeholder for the generated resume PDF.';
  const blob = new Blob([dummyText], { type: 'application/pdf' });
  return blob;
} 