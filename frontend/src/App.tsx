import React, { useState } from 'react';
import { FormData, FormStatus } from './types';
import PDFPreview from './components/Preview/PDFPreview';

// Styles
const appContainerStyle: React.CSSProperties = {
  backgroundColor: '#f5f5f5',
  minHeight: '100vh',
  padding: '20px',
  fontFamily: 'Arial, sans-serif'
};

const appContentStyle: React.CSSProperties = {
  maxWidth: '1200px',
  margin: '0 auto',
  display: 'flex',
  flexDirection: 'column',
  gap: '20px'
};

const headerStyle: React.CSSProperties = {
  textAlign: 'center',
  marginBottom: '20px'
};

const mainContentStyle: React.CSSProperties = {
  display: 'flex',
  gap: '20px',
  flexDirection: 'row',
  flexWrap: 'wrap'
};

const leftColumnStyle: React.CSSProperties = {
  flex: '1',
  minWidth: '300px',
  display: 'flex',
  flexDirection: 'column',
  gap: '20px'
};

const rightColumnStyle: React.CSSProperties = {
  flex: '1',
  minWidth: '300px',
  display: 'flex',
  flexDirection: 'column'
};

const sectionStyle: React.CSSProperties = {
  backgroundColor: 'white',
  borderRadius: '8px',
  padding: '20px',
  boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
};

const sectionHeaderStyle: React.CSSProperties = {
  display: 'flex',
  alignItems: 'center',
  gap: '10px',
  marginBottom: '15px'
};

const inputStyle: React.CSSProperties = {
  width: '100%',
  padding: '10px',
  border: '1px solid #ddd',
  borderRadius: '4px',
  fontSize: '14px'
};

const textAreaStyle: React.CSSProperties = {
  ...inputStyle,
  minHeight: '150px',
  resize: 'vertical'
};

const buttonStyle: React.CSSProperties = {
  backgroundColor: '#1976d2',
  color: 'white',
  border: 'none',
  borderRadius: '4px',
  padding: '10px 20px',
  cursor: 'pointer',
  fontWeight: 'bold',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  gap: '5px'
};

const uploadAreaStyle: React.CSSProperties = {
  border: '2px dashed #ddd',
  borderRadius: '4px',
  padding: '40px',
  textAlign: 'center',
  cursor: 'pointer',
  marginTop: '10px'
};

function App() {
  const [status, setStatus] = useState<FormStatus>('idle');
  const [generatedPDF, setGeneratedPDF] = useState<Blob | null>(null);
  const [formData, setFormData] = useState<FormData>({
    linkedInUrl: '',
    githubUsername: '',
    cvFile: null,
    jobDescription: ''
  });

  const handleInputChange = (field: keyof FormData, value: any) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Form data submitted:', formData);
    setStatus('submitting');
    
    // Simulate an API call to generate PDF
    setTimeout(() => {
      // Create an empty PDF blob for demonstration
      const mockPDF = new Blob(['PDF content'], { type: 'application/pdf' });
      setGeneratedPDF(mockPDF);
      setStatus('success');
    }, 2000);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleInputChange('cvFile', e.target.files[0]);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleInputChange('cvFile', e.dataTransfer.files[0]);
    }
  };

  return (
    <div style={appContainerStyle}>
      <div style={appContentStyle}>
        <header style={headerStyle}>
          <h1 style={{ fontSize: '24px', fontWeight: 'bold' }}>ResumeAI</h1>
          <p style={{ color: '#666' }}>Generate ATS-optimized CVs tailored to your job applications</p>
        </header>

        <main style={mainContentStyle}>
          <div style={leftColumnStyle}>
            {/* LinkedIn Profile Section */}
            <section style={sectionStyle}>
              <div style={sectionHeaderStyle}>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="#0077B5">
                  <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.32 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.79M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z" />
                </svg>
                <h2 style={{ fontSize: '18px', fontWeight: 'bold' }}>LinkedIn Profile</h2>
              </div>
              <div>
                <label style={{ fontSize: '14px', marginBottom: '5px', display: 'block' }}>LinkedIn URL</label>
                <input 
                  type="text" 
                  style={inputStyle} 
                  placeholder="https://www.linkedin.com/in/yourprofile/"
                  value={formData.linkedInUrl}
                  onChange={(e) => handleInputChange('linkedInUrl', e.target.value)}
                />
                <p style={{ fontSize: '12px', color: '#666', marginTop: '5px' }}>We'll scrape your profile data to enhance your CV</p>
              </div>
            </section>

            {/* GitHub Profile Section */}
            <section style={sectionStyle}>
              <div style={sectionHeaderStyle}>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="#333">
                  <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12" />
                </svg>
                <h2 style={{ fontSize: '18px', fontWeight: 'bold' }}>GitHub Profile</h2>
              </div>
              <div>
                <label style={{ fontSize: '14px', marginBottom: '5px', display: 'block' }}>GitHub Username</label>
                <input 
                  type="text" 
                  style={inputStyle} 
                  placeholder="your-github-username"
                  value={formData.githubUsername}
                  onChange={(e) => handleInputChange('githubUsername', e.target.value)}
                />
                <p style={{ fontSize: '12px', color: '#666', marginTop: '5px' }}>We'll analyze your repositories to highlight relevant skills</p>
              </div>
            </section>

            {/* Current CV Upload Section */}
            <section style={sectionStyle}>
              <div style={sectionHeaderStyle}>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="#444">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6zm4 18H6V4h7v5h5v11z" />
                </svg>
                <h2 style={{ fontSize: '18px', fontWeight: 'bold' }}>Current CV Upload</h2>
              </div>
              <div>
                <div 
                  style={uploadAreaStyle}
                  onDragOver={handleDragOver}
                  onDrop={handleDrop}
                  onClick={() => document.getElementById('file-upload')?.click()}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="#ccc" style={{ margin: '0 auto 10px' }}>
                    <path d="M19.35 10.04A7.49 7.49 0 0 0 12 4C9.11 4 6.6 5.64 5.35 8.04A5.994 5.994 0 0 0 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96zM14 13v4h-4v-4H7l5-5 5 5h-3z" />
                  </svg>
                  <p>Drag & drop your CV file here or click to browse</p>
                  <p style={{ fontSize: '12px', color: '#666', marginTop: '5px' }}>Supports PDF, DOCX formats (Max 5MB)</p>
                  <input 
                    type="file" 
                    id="file-upload" 
                    style={{ display: 'none' }} 
                    accept=".pdf,.docx"
                    onChange={handleFileChange}
                  />
                </div>
                {formData.cvFile && (
                  <p style={{ marginTop: '10px', fontSize: '14px' }}>
                    Selected file: {formData.cvFile.name}
                  </p>
                )}
              </div>
            </section>

            {/* Job Description Section */}
            <section style={sectionStyle}>
              <div style={sectionHeaderStyle}>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="#666">
                  <path d="M20 6h-4V4c0-1.11-.89-2-2-2h-4c-1.11 0-2 .89-2 2v2H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2zm-6 0h-4V4h4v2z" />
                </svg>
                <h2 style={{ fontSize: '18px', fontWeight: 'bold' }}>Job Description</h2>
              </div>
              <div>
                <label style={{ fontSize: '14px', marginBottom: '5px', display: 'block' }}>Paste the job description</label>
                <textarea 
                  style={textAreaStyle} 
                  placeholder="Paste the full job description here to optimize your CV for this specific position..."
                  value={formData.jobDescription}
                  onChange={(e) => handleInputChange('jobDescription', e.target.value)}
                />
                <p style={{ fontSize: '12px', color: '#666', marginTop: '5px' }}>The AI will tailor your CV specifically to this job description</p>
              </div>
            </section>

            {/* Generate Button */}
            <button 
              style={buttonStyle} 
              onClick={handleSubmit}
              disabled={status === 'submitting'}
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="white">
                <path d="M19 8l-4 4h3c0 3.31-2.69 6-6 6-1.01 0-1.97-.25-2.8-.7l-1.46 1.46C8.97 19.54 10.43 20 12 20c4.42 0 8-3.58 8-8h3l-4-4zM6 12c0-3.31 2.69-6 6-6 1.01 0 1.97.25 2.8.7l1.46-1.46C15.03 4.46 13.57 4 12 4c-4.42 0-8 3.58-8 8H1l4 4 4-4H6z" />
              </svg>
              {status === 'submitting' ? 'Generating...' : 'Generate ATS-Optimized CV'}
            </button>
          </div>

          <div style={rightColumnStyle}>
            {/* CV Preview Section */}
            <section style={{ ...sectionStyle, height: '100%' }}>
              <div style={sectionHeaderStyle}>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="#444">
                  <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z" />
                </svg>
                <h2 style={{ fontSize: '18px', fontWeight: 'bold' }}>CV Preview</h2>
              </div>
              <div style={{ height: 'calc(100% - 50px)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <PDFPreview 
                  pdfBlob={generatedPDF} 
                  isLoading={status === 'submitting'} 
                />
              </div>
            </section>
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;