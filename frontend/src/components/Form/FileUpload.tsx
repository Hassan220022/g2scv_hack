import React, { useCallback, useState } from 'react';
import { FileUp, CheckCircle, XCircle, File } from 'lucide-react';

interface FileUploadProps {
  onFileChange: (file: File | null) => void;
  error?: string;
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileChange, error }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [fileError, setFileError] = useState<string | undefined>(undefined);
  
  const validateFile = (file: File): string | undefined => {
    if (file.type !== 'application/pdf') {
      return 'Only PDF files are accepted';
    }
    
    if (file.size > 10 * 1024 * 1024) { // 10MB
      return 'File size should be less than 10MB';
    }
    
    return undefined;
  };

  const handleFile = useCallback((file: File) => {
    const validationError = validateFile(file);
    
    if (validationError) {
      setFileError(validationError);
      setFile(null);
      onFileChange(null);
      return;
    }
    
    setFileError(undefined);
    setFile(file);
    onFileChange(file);
  }, [onFileChange]);

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFile(e.dataTransfer.files[0]);
    }
  }, [handleFile]);

  const handleFileInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFile(e.target.files[0]);
    }
  }, [handleFile]);

  const removeFile = useCallback(() => {
    setFile(null);
    setFileError(undefined);
    onFileChange(null);
  }, [onFileChange]);

  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700 mb-1">
        CV Upload (PDF, DOCX, png, jpeg, tex)
      </label>
      
      {!file ? (
        <div
          className={`border-2 border-dashed rounded-md p-6 transition-all ${
            isDragging ? 'border-blue-500 bg-blue-50' : error || fileError ? 'border-red-300 bg-red-50' : 'border-gray-300 hover:border-blue-400'
          }`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <div className="flex flex-col items-center justify-center text-center">
            <FileUp className={`h-10 w-10 mb-3 ${isDragging ? 'text-blue-500' : error || fileError ? 'text-red-500' : 'text-gray-400'}`} />
            <p className="text-sm font-medium mb-1">
              Drag & drop your CV here, or{' '}
              <label className="text-blue-600 hover:text-blue-700 cursor-pointer">
                browse
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileInputChange}
                  className="hidden"
                />
              </label>
            </p>
            <p className="text-xs text-gray-500">PDF only, max 10MB</p>
          </div>
        </div>
      ) : (
        <div className="border rounded-md p-4 bg-gray-50 flex items-center">
          <div className="mr-3 text-blue-600">
            <File size={24} />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-900 truncate">{file.name}</p>
            <p className="text-xs text-gray-500">{(file.size / 1024).toFixed(0)} KB</p>
          </div>
          <div className="flex items-center">
            <CheckCircle className="h-5 w-5 text-green-500 mr-2" />
            <button 
              type="button" 
              onClick={removeFile}
              className="text-gray-400 hover:text-red-500 transition-colors"
            >
              <XCircle size={20} />
            </button>
          </div>
        </div>
      )}
      
      {(error || fileError) && (
        <p className="mt-1 text-sm text-red-500">{error || fileError}</p>
      )}
    </div>
  );
};

export default FileUpload;