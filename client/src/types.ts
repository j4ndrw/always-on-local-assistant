import { piperGenerate } from "piper-wasm";

export type Speech = Awaited<ReturnType<typeof piperGenerate>>;
