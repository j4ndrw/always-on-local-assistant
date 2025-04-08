declare module "piper-wasm" {
  export const HF_BASE: "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/";
  export const piperPhonemize: (
    piperPhonemizeJsUrl: string,
    piperPhonemizeWasmUrl: string,
    piperPhonemizeDataUrl: string,
    workerUrl: string,
    modelConfigUrl: string,
    input: string,
    onProgress: (arg0: number) => void,
    onnxruntimeUrl?: string,
  ) => Promise<{
    phonemes: string[];
    phonemeIds: int[];
  }>;
  export const piperGenerate: (
    piperPhonemizeJsUrl: string,
    piperPhonemizeWasmUrl: string,
    piperPhonemizeDataUrl: string,
    workerUrl: string,
    modelUrl: string,
    modelConfigUrl: string,
    speakerId: number | null,
    input: string,
    onProgress: (arg0: number) => void,
    phonemeIds: int[] | null,
    inferEmotion?: boolean,
    onnxruntimeUrl?: string,
    expressionWorkerUrl?: string,
  ) => Promise<{
    file: string;
    expressions: Expressions;
    duration: number;
    input: string;
    kind: string;
    phonemes: string[];
    phonemeIds: int[];
  }>;
}
