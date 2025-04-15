/* eslint-disable react-hooks/exhaustive-deps */
import { useEffect } from "react";

import { BackgroundMode } from "@anuradev/capacitor-background-mode";
import { Toast } from "@capacitor/toast";
import { Geolocation } from "@capacitor/geolocation";
import { LocalNotifications } from "@capacitor/local-notifications";

import { FrontendCapabilities } from "./plugins/frontend-capabilities";
import { BackgroundGeolocation } from "./plugins/background-geolocation";
import { STT } from "./plugins/speech-to-text";

import { speak } from "./speech-to-speech";
import { playAudio } from "./audio";
import { executeSideEffectsDrivenByLLM } from "./llm";
import { hasWakeWord } from "./wake-word";
import { getConversation } from "./api/conversation";
import { sleep } from "./utils";

function App() {
  const handleTranscript = async (transcript: string) => {
    if (!hasWakeWord(transcript)) return listen();

    await playAudio("PROMPT_ACCEPTED");
    await Toast.show({
      text: `You asked Lola: "${transcript}"`,
      duration: "long",
    });
    const { installedApps } = await FrontendCapabilities.getInstalledApps();
    const gpsPosition = await Geolocation.getCurrentPosition({
      timeout: 10000,
    }).catch((err) => {
      console.error(err);
      return null;
    });
    const { latitude, longitude } = gpsPosition?.coords ?? {};
    const metadata = { installedApps, gpsPosition: { latitude, longitude } };
    const history = await getConversation(transcript, metadata);
    if (!history) {
      return speak("I didn't get that, could you try again?", {
        whenDone: listen,
      });
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
    if (!llmResponse) return listen();

    await Promise.all([
      await speak(llmResponse, { whenDone: listen }),
      executeSideEffectsDrivenByLLM(llmTools),
    ]);
  };

  const listen = async () => {
    // Using while(true) to not exceed the call stack size
    while (true) {
      try {
        const { isListening } = await STT.isListening();
        if (!isListening) await STT.startListening();
        break;
      } catch (err) {
        console.error(err);
        await sleep(1000);
        continue;
      }
    }
  };

  const moveAppToBackground = async () => {
    await BackgroundMode.enable();
    await BackgroundMode.requestNotificationsPermission();
    await BackgroundMode.requestMicrophonePermission();
    await BackgroundMode.requestDisableBatteryOptimizations();
    await BackgroundMode.moveToBackground();
  };

  const keepAppAwake = async () => {
    // Hack to keep app awake at all times
    await BackgroundGeolocation.addWatcher(
      {
        backgroundTitle:
          "Lola is currently listening for commands / interactions.",
        requestPermissions: true,
      },
      () => { },
    );
  };

  const initializeSTTModel = async () => {
    // Using while(true) to not exceed the call stack size
    while (true) {
      try {
        await STT.initializeModel();
        await Toast.show({
          text: "Lola's speech-to-text model is initialized.",
        });
        break;
      } catch (err) {
        console.error(err);
        await sleep(1000);
        continue;
      }
    }
  };

  const initializeConversation = async () => {
    await STT.addListener("result", async ({ result: transcript }) => {
      if (transcript) {
        await STT.stopListening();
        await handleTranscript(transcript.trim());
      }
    });
    await Toast.show({ text: "Lola is ready to listen for commands." });
    await listen().then(() =>
      speak("Ready to listen for commands.", { whenDone: listen }),
    );
  };

  const requestPermissions = async () => {
    await STT.available();
    await Geolocation.requestPermissions({
      permissions: ["location", "coarseLocation"],
    }).catch((err) => {
      console.error(err);
    });
    await LocalNotifications.requestPermissions();
  };

  useEffect(() => {
    (async () => {
      await moveAppToBackground();
      await keepAppAwake();
      await requestPermissions();

      await Toast.show({
        text: "Lola is initializing her speech-to-speech capabilities. Please wait...",
      });

      await initializeSTTModel();
      await initializeConversation();
    })();
  }, []);

  return <div />;
}

export default App;
