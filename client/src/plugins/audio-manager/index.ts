import { registerPlugin } from '@capacitor/core';

import type { AudioManagerPlugin } from './definitions';

const AudioManager = registerPlugin<AudioManagerPlugin>('AudioManager');

export * from './definitions';
export { AudioManager };
