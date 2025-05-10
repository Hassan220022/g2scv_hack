import React from 'react';

interface SplitScreenProps {
  left: React.ReactNode;
  right: React.ReactNode;
}

const SplitScreen: React.FC<SplitScreenProps> = ({ left, right }) => {
  return (
    <div className="flex flex-col lg:flex-row h-full rounded-lg overflow-hidden shadow-lg">
      <div className="w-full lg:w-2/5 bg-white overflow-y-auto border-r">
        {left}
      </div>
      <div className="w-full lg:w-3/5 bg-white overflow-hidden flex flex-col">
        {right}
      </div>
    </div>
  );
};

export default SplitScreen;