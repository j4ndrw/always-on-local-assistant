import { STATIC_ASSETS_BASE_URL } from "@/constants";
import { Speech } from "@/types";
import { Toast } from "@capacitor/toast";
import { piperGenerate } from "piper-wasm";

export const tts = async (text: string) => {
  const speech = await piperGenerate(
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

  await Toast.show({
    text: `Lola says: ${text.trim().replace(/\n+/g, " ")}`,
    duration: "long",
  });

  return speech;
};

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
  };

export const speak = (s: string, options: { whenDone: () => void }) =>
  tts(s).then(stt({ onEnded: options.whenDone }));
