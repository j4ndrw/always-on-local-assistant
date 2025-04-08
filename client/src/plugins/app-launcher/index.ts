import { registerPlugin } from '@capacitor/core';

import type { AppLauncherPlugin } from './definitions';

const AppLauncher = registerPlugin<AppLauncherPlugin>('AppLauncher');

export * from './definitions';
export { AppLauncher };
