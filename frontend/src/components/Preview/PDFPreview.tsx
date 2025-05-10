import React, { useState } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import PDFControls from './PDFControls';
import { FileWarning } from 'lucide-react';

// Set worker path for PDF.js
pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.js`;

interface PDFPreviewProps {
  pdfBlob: Blob | null;
  isLoading: boolean;
}

const PDFPreview: React.FC<PDFPreviewProps> = ({ pdfBlob, isLoading }) => {
  const [numPages, setNumPages] = useState<number>(0);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [scale, setScale] = useState<number>(1.0);
  const [error, setError] = useState<string | null>(null);
  
  const handleDocumentLoadSuccess = ({ numPages }: { numPages: number }) => {
    setNumPages(numPages);
    setCurrentPage(1);
    setError(null);
  };
  
  const handleDocumentLoadError = (err: Error) => {
    console.error('Error loading PDF', err);
    setError('Error loading the PDF document. Please check the file and try again.');
  };
  
  const handleZoomIn = () => {
    setScale(prev => Math.min(prev + 0.1, 2.0));
  };
  
  const handleZoomOut = () => {
    setScale(prev => Math.max(prev - 0.1, 0.5));
  };
  
  const handleDownload = () => {
    if (pdfBlob) {
      const url = URL.createObjectURL(pdfBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'generated-resume.pdf';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  };

  const containerStyle = {
    width: "100%",
    height: "100%",
    display: "flex",
    flexDirection: "column" as const,
  };
  
  const headerStyle = {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    width: "100%",
    padding: "12px 16px",
    borderBottom: "1px solid #e5e7eb",
    marginBottom: "16px",
  };
  
  const loadingStyle = {
    flex: "1",
    display: "flex",
    flexDirection: "column" as const,
    alignItems: "center",
    justifyContent: "center",
    padding: "24px",
  };
  
  const spinnerStyle = {
    width: "64px",
    height: "64px",
    border: "4px solid #3b82f6",
    borderTopColor: "transparent",
    borderRadius: "50%",
    marginBottom: "16px",
    animation: "spin 1s linear infinite",
  };

  return (
    <div style={containerStyle}>
      <div style={headerStyle}>
        <h2 style={{ fontSize: "20px", fontWeight: "600", color: "#1f2937" }}>Preview</h2>
      </div>
      
      {isLoading ? (
        <div style={loadingStyle}>
          <div style={spinnerStyle}></div>
          <p style={{ fontSize: "18px", fontWeight: "500", color: "#4b5563" }}>Generating preview...</p>
        </div>
      ) : pdfBlob ? (
        <>
          <PDFControls
            numPages={numPages}
            currentPage={currentPage}
            scale={scale}
            onPageChange={setCurrentPage}
            onZoomIn={handleZoomIn}
            onZoomOut={handleZoomOut}
            onDownload={handleDownload}
            canDownload={!!pdfBlob && !error}
          />
          
          <div style={{ flex: "1", overflow: "auto", backgroundColor: "#f3f4f6", padding: "16px", display: "flex", justifyContent: "center" }}>
            <div style={{ backgroundColor: "white", boxShadow: "0 1px 3px rgba(0,0,0,0.1)" }}>
              <Document
                file={pdfBlob}
                onLoadSuccess={handleDocumentLoadSuccess}
                onLoadError={handleDocumentLoadError}
                loading={
                  <div style={{ display: "flex", alignItems: "center", justifyContent: "center", padding: "48px" }}>
                    <div style={{ width: "40px", height: "40px", border: "4px solid #3b82f6", borderTopColor: "transparent", borderRadius: "50%" }}></div>
                  </div>
                }
                error={
                  <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: "48px", color: "#ef4444" }}>
                    <div style={{ marginBottom: "8px" }}>
                      <FileWarning size={48} />
                    </div>
                    <p style={{ textAlign: "center" }}>{error || 'Failed to load PDF'}</p>
                  </div>
                }
              >
                <Page 
                  pageNumber={currentPage} 
                  scale={scale}
                  renderTextLayer={false}
                  renderAnnotationLayer={false}
                />
              </Document>
            </div>
          </div>
        </>
      ) : (
        <div style={{ flex: "1", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: "24px", backgroundColor: "#f9fafb" }}>
          <div style={{ padding: "24px", textAlign: "center" }}>
            <div style={{ display: "inline-flex", alignItems: "center", justifyContent: "center", width: "64px", height: "64px", backgroundColor: "#f3f4f6", borderRadius: "50%", marginBottom: "16px" }}>
              <FileWarning size={32} style={{ color: "#9ca3af" }} />
            </div>
            <h3 style={{ fontSize: "18px", fontWeight: "500", color: "#111827", marginBottom: "4px" }}>No PDF to preview</h3>
            <p style={{ color: "#6b7280" }}>
              Fill out the form and submit to generate a preview
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default PDFPreview;