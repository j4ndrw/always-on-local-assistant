import { registerPlugin } from '@capacitor/core';

import type { STTPlugin } from './definitions';

const STT = registerPlugin<STTPlugin>('STT');

export * from './definitions';
export { STT };
