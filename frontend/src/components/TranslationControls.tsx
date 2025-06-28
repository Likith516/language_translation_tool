import React from 'react';
import { Mic, StopCircle } from 'lucide-react';
import { LanguagePair, TranslationState } from '../types';

interface TranslationControlsProps {
  state: TranslationState;
  onStartRecording: (speaker: 'source' | 'target') => void;
  onStopRecording: () => void;
}

export function TranslationControls({ state, onStartRecording, onStopRecording }: TranslationControlsProps) {
  if (!state.selectedPair) {
    return (
      <div className="text-center text-gray-600">
        Please select a language pair from the navigation bar to begin
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center space-y-8">
      <div className="flex space-x-4">
        <button
          onClick={() => onStartRecording('source')}
          disabled={state.isRecording && state.currentSpeaker !== 'source'}
          className={`flex items-center px-6 py-3 rounded-lg font-medium text-white transition-colors
            ${state.isRecording && state.currentSpeaker === 'source'
              ? 'bg-red-600 hover:bg-red-700'
              : 'bg-blue-600 hover:bg-blue-700'
            } disabled:opacity-50 disabled:cursor-not-allowed`}
        >
          <Mic className="w-5 h-5 mr-2" />
          {state.selectedPair.source.toUpperCase()}
        </button>

        <button
          onClick={() => onStartRecording('target')}
          disabled={state.isRecording && state.currentSpeaker !== 'target'}
          className={`flex items-center px-6 py-3 rounded-lg font-medium text-white transition-colors
            ${state.isRecording && state.currentSpeaker === 'target'
              ? 'bg-red-600 hover:bg-red-700'
              : 'bg-blue-600 hover:bg-blue-700'
            } disabled:opacity-50 disabled:cursor-not-allowed`}
        >
          <Mic className="w-5 h-5 mr-2" />
          {state.selectedPair.target.toUpperCase()}
        </button>
      </div>

      {state.isRecording && (
        <button
          onClick={onStopRecording}
          className="flex items-center px-6 py-3 rounded-lg font-medium text-white bg-gray-600 hover:bg-gray-700 transition-colors"
        >
          <StopCircle className="w-5 h-5 mr-2" />
          Stop Recording
        </button>
      )}
    </div>
  );
}