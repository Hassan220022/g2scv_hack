# G2SCV Resume Builder

A powerful resume builder that leverages LinkedIn profiles, GitHub repositories, and your existing CV to generate ATS-optimized resumes tailored to specific job descriptions.

## Features

- **LinkedIn Integration**: Automatically extract professional experience, education, and skills from your LinkedIn profile.
- **GitHub Integration**: Analyze your public repositories to showcase coding projects and technical skills.
- **CV Parsing**: Upload your existing CV to extract and reuse your professional information.
- **Job Description Analysis**: Tailor your resume to specific job descriptions for higher ATS scores.
- **ATS-Optimized Output**: Generate LaTeX-formatted resumes that pass through Applicant Tracking Systems.

## Setup Instructions

### Prerequisites

- Node.js 18+ and npm

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/g2scv.git
   cd g2scv/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file:
   ```bash
   cp .env.example .env
   ```
   
4. Edit the `.env` file with your API keys:
   - Get an Apify API token at [https://console.apify.com/account/integrations](https://console.apify.com/account/integrations)

### Running the Application

Development mode:
```bash
npm run dev
```

The application will be available at http://localhost:5173/

## Usage

1. Enter your LinkedIn profile URL (e.g., https://www.linkedin.com/in/username)
2. Enter your GitHub username
3. Upload your existing CV (PDF format)
4. Paste the job description you're applying for
5. Click "Generate Resume" and wait for the optimized resume to be generated
6. Preview the result and download the PDF

## Technologies Used

- React + TypeScript
- Vite
- Tailwind CSS
- Apify (LinkedIn scraping)
- PDF.js (PDF rendering)

## Backend Services

For the full experience, the frontend integrates with several backend services:

- LinkedIn Scraper: Extracts profile data from LinkedIn
- GitHub Scraper: Analyzes public repositories
- CV Parser: Extracts information from uploaded CVs
- Resume Generator: Combines all data to generate an optimized resume

## Hackathon Mode

For the hackathon demo, the application runs with mock backend services that simulate the actual API calls. 