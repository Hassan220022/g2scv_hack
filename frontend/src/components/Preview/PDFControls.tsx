import React from 'react';
import { ZoomIn, ZoomOut, Download, ChevronLeft, ChevronRight } from 'lucide-react';
import Button from '../ui/Button';

interface PDFControlsProps {
  numPages: number;
  currentPage: number;
  scale: number;
  onPageChange: (page: number) => void;
  onZoomIn: () => void;
  onZoomOut: () => void;
  onDownload: () => void;
  canDownload: boolean;
}

const PDFControls: React.FC<PDFControlsProps> = ({
  numPages,
  currentPage,
  scale,
  onPageChange,
  onZoomIn,
  onZoomOut,
  onDownload,
  canDownload
}) => {
  return (
    <div className="flex flex-col sm:flex-row items-center justify-between w-full py-3 px-4 border-b mb-4">
      <div className="flex items-center space-x-2 mb-2 sm:mb-0">
        <Button
          variant="outline"
          size="sm"
          onClick={() => onPageChange(Math.max(1, currentPage - 1))}
          disabled={currentPage <= 1}
          aria-label="Previous page"
        >
          <ChevronLeft size={18} />
        </Button>
        
        <div className="text-sm">
          Page <span className="font-medium">{currentPage}</span> of <span className="font-medium">{numPages || 1}</span>
        </div>
        
        <Button
          variant="outline"
          size="sm"
          onClick={() => onPageChange(Math.min(numPages, currentPage + 1))}
          disabled={currentPage >= numPages}
          aria-label="Next page"
        >
          <ChevronRight size={18} />
        </Button>
      </div>
      
      <div className="flex items-center space-x-2">
        <div className="flex items-center space-x-2 mr-2">
          <Button
            variant="outline"
            size="sm"
            onClick={onZoomOut}
            disabled={scale <= 0.5}
            aria-label="Zoom out"
          >
            <ZoomOut size={18} />
          </Button>
          
          <span className="text-sm font-medium">{Math.round(scale * 100)}%</span>
          
          <Button
            variant="outline"
            size="sm"
            onClick={onZoomIn}
            disabled={scale >= 2}
            aria-label="Zoom in"
          >
            <ZoomIn size={18} />
          </Button>
        </div>
        
        <Button
          variant="primary"
          size="sm"
          onClick={onDownload}
          disabled={!canDownload}
          className="flex items-center"
        >
          <Download size={18} className="mr-1" />
          <span>Download</span>
        </Button>
      </div>
    </div>
  );
};

export default PDFControls;