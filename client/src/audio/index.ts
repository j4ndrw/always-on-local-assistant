import { STATIC_ASSETS_BASE_URL } from "@/constants";
import { NativeAudio, PreloadOptions } from "@capacitor-community/native-audio";

export type AudioAsset = { id: string, path: string };

export const AUDIO_ASSETS = {
  PROMPT_ACCEPTED: {
    id: "prompt-accepted",
    path: `${STATIC_ASSETS_BASE_URL}/assets/sounds/prompt-accepted.mp3`,
  },
} satisfies Record<string, AudioAsset>

const asset = (asset: keyof typeof AUDIO_ASSETS): AudioAsset => AUDIO_ASSETS[asset];
const assetToPreload = (assetToPreload: keyof typeof AUDIO_ASSETS): PreloadOptions => ({
  assetId: asset(assetToPreload).id,
  assetPath: asset(assetToPreload).path,
  isUrl: true,
});

export const preloadAudioAssets = async () => {
  await NativeAudio.preload(assetToPreload("PROMPT_ACCEPTED"));
};

export const playAudio = async (assetToPlay: keyof typeof AUDIO_ASSETS) => {
  const { isPlaying } = await NativeAudio.isPlaying({ assetId: asset(assetToPlay).id });
  if (!isPlaying) await NativeAudio.play({ assetId: asset(assetToPlay).id });
}
