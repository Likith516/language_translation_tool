import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { TranslationControls } from './components/TranslationControls';
import { LANGUAGE_PAIRS } from './config';
import { TranslationState } from './types';

const API_URL = 'http://localhost:5000/api';

function App() {
  const [state, setState] = useState<TranslationState>({
    selectedPair: null,
    isRecording: false,
    currentSpeaker: null,
  });

  const handleSelectPair = (pair: typeof LANGUAGE_PAIRS[0]) => {
    setState(prev => ({
      ...prev,
      selectedPair: pair,
      isRecording: false,
      currentSpeaker: null,
    }));
  };

  const handleStartRecording = async (speaker: 'source' | 'target') => {
    try {
      const recordWave = document.getElementById('recordWave') as HTMLElement;
      if (recordWave) recordWave.style.display = 'flex';
      const response = await fetch(`${API_URL}/start-recording`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          languagePair: state.selectedPair,
          speaker,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to start recording');
      }

      setState(prev => ({
        ...prev,
        isRecording: true,
        currentSpeaker: speaker,
      }));
    } catch (error) {
      console.error('Failed to start recording:', error);
      alert('Failed to start recording. Please ensure the Flask server is running.');
    }
  };



  const handleStopRecording = async () => {
    try {
      const recordWave = document.getElementById('recordWave') as HTMLElement;
      if (recordWave) recordWave.style.display = 'none';
      const response = await fetch(`${API_URL}/stop-recording`, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error('Failed to stop recording');
      }

      setState(prev => ({
        ...prev,
        isRecording: false,
        currentSpeaker: null,
      }));
    } catch (error) {
      console.error('Failed to stop recording:', error);
      alert('Failed to stop recording. Please ensure the Flask server is running.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar
        languagePairs={LANGUAGE_PAIRS}
        selectedPair={state.selectedPair}
        onSelectPair={handleSelectPair}
      />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <TranslationControls
            state={state}
            onStartRecording={handleStartRecording}
            onStopRecording={handleStopRecording}
          />
        </div>
      </main>
    </div>
  );
}

export default App;