/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable react-hooks/exhaustive-deps */
import { useEffect } from "react";
import { getConversation } from "./api/conversation";
import { hasWakeWord } from "./wake-word";
import { sleep } from "./utils";
import { STT } from "./plugins/speech-to-text";
import { Speech } from "./types";
import { tts } from "./speech-to-text";
import { BackgroundMode } from "@anuradev/capacitor-background-mode";
import { executeSideEffectsDrivenByLLM } from "./llm";
import { FrontendCapabilities } from "./plugins/frontend-capabilities";
import { Toast } from "@capacitor/toast";
import { Geolocation } from '@capacitor/geolocation';

STT.available();

function App() {
  const playSpeech = async (speech: Speech, onEnded: () => void) => {
    const audioContext = new AudioContext();
    const audioBufferSource = audioContext.createBufferSource();
    audioBufferSource.connect(audioContext.destination);
    audioBufferSource.addEventListener("ended", onEnded);

    const response = await fetch(speech.file);
    const arrayBuffer = await response.arrayBuffer();

    await audioContext.decodeAudioData(
      arrayBuffer,
      (buffer) => {
        audioBufferSource.buffer = buffer;
        audioBufferSource.start(0);
      },
      (error) => {
        console.error("Error decoding audio data:", error);
      },
    );
  };

  const handleTranscript = async (transcript: string) => {
    if (!hasWakeWord(transcript)) return listenForSpeech();

    await Toast.show({ text: `You asked Lola: "${transcript}"`, duration: "long" })
    const { installedApps } = await FrontendCapabilities.getInstalledApps();
    const gpsPosition = await Geolocation.getCurrentPosition({ timeout: 10000 }).catch(err => {
      console.error(err);
      return null;
    });
    const { latitude, longitude } = gpsPosition?.coords ?? {};
    const metadata = { installedApps, gpsPosition: { latitude, longitude } };
    const history = await getConversation(transcript, metadata);
    if (!history) {
      const speech = await tts("I didn't get that, could you try again?");
      return playSpeech(speech, listenForSpeech);
    }

    const { llmMessages, llmTools } = history.reduce<{
      llmMessages: Array<{
        role: "assistant";
        content?: string | null | undefined;
      }>;
      llmTools: Array<{ role: "tool"; content: string }>;
    }>(
      (acc, message) => {
        if (message.role === "assistant")
          acc.llmMessages.push(
            message as typeof message & { role: "assistant" },
          );
        else if (message.role === "tool" && !!message.content)
          acc.llmTools.push(
            message as typeof message & { role: "tool"; content: string },
          );
        return acc;
      },
      { llmMessages: [], llmTools: [] },
    );

    const { content: llmResponse } = llmMessages[llmMessages.length - 1];
    if (!llmResponse) return listenForSpeech();

    await Promise.all([
      await tts(llmResponse).then((speech) =>
        playSpeech(speech, listenForSpeech),
      ),
      executeSideEffectsDrivenByLLM(llmTools),
    ]);
  };

  const listenForSpeech = async () => {
    // Using while(true) to not exceed the call stack size
    while (true) {
      try {
        const { isListening } = await STT.isListening();
        if (!isListening) await STT.startListening();
        break;
      } catch (err) {
        await Toast.show({ text: `${(err as any).message} - Trying again...`})
        console.error(err);
        await sleep(1000);
        continue;
      }
    }
  };

  useEffect(() => {
    (async () => {
      await BackgroundMode.enable();
      await BackgroundMode.requestNotificationsPermission();
      await BackgroundMode.requestMicrophonePermission();
      await BackgroundMode.requestDisableBatteryOptimizations();
      await BackgroundMode.moveToBackground();

      await Geolocation.requestPermissions({ permissions: ['location', 'coarseLocation']}).catch(err => {
        console.error(err);
      });

      await Toast.show({ text: "Lola is initializing her speech-to-speech capabilities. Please wait..." })

      // Using while(true) to not exceed the call stack size
      while (true) {
        try {
          await STT.initializeModel();
          await Toast.show({ text: "Lola's speech-to-text model is initialized." })
          break;
        } catch (err) {
          console.error(err);
          await sleep(1000);
          continue;
        }
      }

      await STT.addListener("result", async ({ result: transcript }) => {
        if (transcript) {
          await STT.stopListening();
          await handleTranscript(transcript.trim());
        }
      });
      await listenForSpeech();
      await Toast.show({ text: "Lola is ready to listen for commands." })
      await playSpeech(
        await tts("Ready to listen for commands."),
        listenForSpeech,
      );
    })();
  }, []);

  return <div />;
}

export default App;
