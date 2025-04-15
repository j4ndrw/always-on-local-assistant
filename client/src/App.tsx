/* eslint-disable react-hooks/exhaustive-deps */
import { useEffect, useRef, useState } from "react";

import { Toast } from "@capacitor/toast";
import { Geolocation } from "@capacitor/geolocation";
import { LocalNotifications } from "@capacitor/local-notifications";
import { Location } from "@capacitor-community/background-geolocation";

import { FrontendCapabilities } from "./plugins/frontend-capabilities";
import { BackgroundGeolocation } from "./plugins/background-geolocation";
import { STT } from "./plugins/speech-to-text";

import { speak } from "./speech-to-speech";
import { playAudio, preloadAudioAssets } from "./audio";
import { executeSideEffectsDrivenByLLM } from "./llm";
import { hasWakeWord } from "./wake-word";
import { getConversation } from "./api/conversation";
import { sleep } from "./utils";
import { localNotificationActions } from "./local-notifications";
import { moveAppToBackground } from "./background-mode";

function App() {
  const [speechAudioCtxPool, setSpeechAudioCtxPool] = useState<AudioContext[]>(
    [],
  );
  const gpsPosition = useRef<Location | undefined>(undefined);
  const handleTranscript = async (transcript: string) => {
    if (!hasWakeWord(transcript)) return listen();

    await playAudio("PROMPT_ACCEPTED");
    await Toast.show({
      text: `You asked Lola: "${transcript}"`,
      duration: "long",
    });
    const { installedApps } = await FrontendCapabilities.getInstalledApps();
    const { latitude, longitude } = gpsPosition.current ?? {};
    const metadata = { installedApps, gpsPosition: { latitude, longitude } };
    const history = await getConversation(transcript, metadata);
    if (!history) {
      return speak("I didn't get that, could you try again?", {
        onSpeechAudioCtxCreated: (ctx) =>
          setSpeechAudioCtxPool((prev) => [...prev, ctx]),
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
      await speak(llmResponse, {
        onSpeechAudioCtxCreated: (ctx) =>
          setSpeechAudioCtxPool((prev) => [...prev, ctx]),
        whenDone: listen,
      }),
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

  const setUpGeolocationWatcher = async () => {
    // Also a hack to keep app awake at all times
    await BackgroundGeolocation.addWatcher(
      {
        backgroundTitle:
          "Lola is currently listening for commands / interactions.",
        requestPermissions: true,
      },
      (position, error) => {
        if (error) {
          console.error(error);
          return;
        }
        gpsPosition.current = position;
      },
    );
  };

  const initializeSTTModel = async () => {
    await Toast.show({
      text: "Lola is initializing her speech-to-speech capabilities. Please wait...",
    });
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
      speak("Ready to listen for commands.", {
        onSpeechAudioCtxCreated: (ctx) =>
          setSpeechAudioCtxPool((prev) => [...prev, ctx]),
        whenDone: listen,
      }),
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

  const initializeLocalNotifications = async () => {
    await LocalNotifications.createChannel({
      ...localNotificationActions.channel,
      importance: 5,
      visibility: 1,
    });

    await localNotificationActions.interruptLola.registerActionType();
  };

  const setUpNotificationActions = async () => {
    await LocalNotifications.addListener(
      "localNotificationActionPerformed",
      async (action) => {
        await localNotificationActions.interruptLola
          .action(action)
          .call(speechAudioCtxPool, () => {
            listen();
            setSpeechAudioCtxPool([]);
          });
      },
    );
  };

  useEffect(() => {
    moveAppToBackground()
      .then(requestPermissions)
      .then(setUpGeolocationWatcher)
      .then(preloadAudioAssets)
      .then(setUpNotificationActions)
      .then(initializeLocalNotifications)
      .then(initializeSTTModel)
      .then(initializeConversation);
  }, []);

  return <div />;
}

export default App;
