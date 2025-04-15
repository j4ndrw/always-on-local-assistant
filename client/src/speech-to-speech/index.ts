import { moveAppToBackground } from "@/background-mode";
import { STATIC_ASSETS_BASE_URL } from "@/constants";
import { localNotificationActions } from "@/local-notifications";
import { Speech } from "@/types";
import { LocalNotifications } from "@capacitor/local-notifications";
import { piperGenerate } from "piper-wasm";

export const tts = async (text: string) =>
  piperGenerate(
    `${STATIC_ASSETS_BASE_URL}/piper/piper_phonemize.js`,
    `${STATIC_ASSETS_BASE_URL}/piper/piper_phonemize.wasm`,
    `${STATIC_ASSETS_BASE_URL}/piper/piper_phonemize.data`,
    `${STATIC_ASSETS_BASE_URL}/piper/piper_worker.js`,
    `${STATIC_ASSETS_BASE_URL}/piper/models/amy/en_US-amy-low.onnx`,
    `${STATIC_ASSETS_BASE_URL}/piper/models/amy/en_US-amy-low.onnx.json`,
    0,
    text,
    () => { },
    null,
  );

export const stt =
  (options: { onEnded: () => void }) => async (speech: Speech) => {
    const audioContext = new AudioContext();
    const audioBufferSource = audioContext.createBufferSource();
    audioBufferSource.connect(audioContext.destination);
    audioBufferSource.addEventListener("ended", options.onEnded);

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
    return audioContext;
  };

export const speak = async (s: string, options: {
  onSpeechAudioCtxCreated: (ctx: AudioContext) => void,
  whenDone: () => void
}) => {
  const audioCtx = await tts(s).then(
    stt({
      onEnded: () => {
        options.whenDone();
        return LocalNotifications.removeAllListeners();
      },
    }),
  );

  options.onSpeechAudioCtxCreated(audioCtx);

  await LocalNotifications.schedule({
    notifications: [
      {
        channelId: localNotificationActions.channel.id,
        id: 0,
        title: "Lola says:",
        body: s,
        actionTypeId: localNotificationActions.interruptLola.typeId,
      },
    ],
  });

  await LocalNotifications.addListener(
    "localNotificationActionPerformed",
    (action) => {
      if (action.actionId === localNotificationActions.interruptLola.id)
        Promise.all([
          moveAppToBackground,
          audioCtx
            .close()
            .then(LocalNotifications.removeAllListeners)
            .then(options.whenDone),
        ]);
    },
  );
};
