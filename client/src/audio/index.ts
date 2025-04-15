import { NativeAudio, PreloadOptions } from "@capacitor-community/native-audio";

export type AudioAsset = { id: string, path: string };

export const AUDIO_ASSETS = {
  PROMPT_ACCEPTED: {
    id: "prompt-accepted",
    path: `public/assets/sounds/prompt-accepted.mp3`,
  },
} satisfies Record<string, AudioAsset>

const asset = (asset: keyof typeof AUDIO_ASSETS): AudioAsset => AUDIO_ASSETS[asset];
const assetToPreload = (assetToPreload: keyof typeof AUDIO_ASSETS): PreloadOptions => ({
  assetId: asset(assetToPreload).id,
  assetPath: asset(assetToPreload).path,
});

export const preloadAudioAssets = async () => {
  try {
    await NativeAudio.preload(assetToPreload("PROMPT_ACCEPTED"));
  } catch (err) {
    console.error(err);
    return;
  }
};

export const playAudio = async (assetToPlay: keyof typeof AUDIO_ASSETS) => {
  const { isPlaying } = await NativeAudio.isPlaying({ assetId: asset(assetToPlay).id });
  if (!isPlaying) await NativeAudio.play({ assetId: asset(assetToPlay).id });
}
