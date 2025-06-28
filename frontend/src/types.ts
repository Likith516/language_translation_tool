export type LanguagePair = {
  source: string;
  target: string;
  label: string;
};

export type TranslationState = {
  selectedPair: LanguagePair | null;
  isRecording: boolean;
  currentSpeaker: 'source' | 'target' | null;
};