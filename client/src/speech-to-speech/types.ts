import { tts } from ".";

export type Speech = Awaited<ReturnType<typeof tts>>;
