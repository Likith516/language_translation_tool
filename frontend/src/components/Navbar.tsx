import React from 'react';
import { LanguagePair } from '../types';
import { Languages } from 'lucide-react';

interface NavbarProps {
  languagePairs: LanguagePair[];
  selectedPair: LanguagePair | null;
  onSelectPair: (pair: LanguagePair) => void;
}

export function Navbar({ languagePairs, selectedPair, onSelectPair }: NavbarProps) {
  return (
    <nav className="bg-indigo-600 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Languages className="h-8 w-8" />
            <span className="ml-2 text-xl font-semibold">Speech Translator</span>
          </div>
          <div className="flex space-x-4">
            {languagePairs.map((pair) => (
              <button
                key={`${pair.source}-${pair.target}`}
                onClick={() => onSelectPair(pair)}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors
                  ${selectedPair?.source === pair.source && selectedPair?.target === pair.target
                    ? 'bg-indigo-800 text-white'
                    : 'text-indigo-100 hover:bg-indigo-700'
                  }`}
              >
                {pair.label}
              </button>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
}