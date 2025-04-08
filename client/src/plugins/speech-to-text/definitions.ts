import { PluginListenerHandle } from "@capacitor/core";

type STTEvent = 'partialResult' | 'result' | 'finalResult';

type STTListenerData<T extends STTEvent> =
  T extends 'partialResult'
  ? { matches: string }
  : T extends 'result'
  ? { result: string }
  : T extends 'finalResult'
  ? { result: string }
  : never;

export interface STTPlugin {
  initializeModel(): Promise<void>;
  available(): Promise<{ available: boolean }>;
  startListening(): Promise <void>;
  stopListening(): Promise <void>;
  pauseListening(): Promise <void>;
  resumeListening(): Promise <void>;
  isListening(): Promise<{ isListening: boolean }>;

  addListener<T extends STTEvent>(
    eventName: T,
    listener: (data: STTListenerData<T>) => void
  ): Promise<PluginListenerHandle>;
}
