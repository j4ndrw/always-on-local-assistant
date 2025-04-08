import { STATIC_ASSETS_BASE_URL } from "@/constants";
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

  await Toast.show({ text: `Lola says: ${text.trim().replace(/\n+/g, ' ')}`, duration: "long" });

  return speech;
};
