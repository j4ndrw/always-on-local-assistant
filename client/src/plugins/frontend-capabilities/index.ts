import { registerPlugin } from '@capacitor/core';

import type { FrontendCapabilitiesPlugin } from './definitions';

const FrontendCapabilities = registerPlugin<FrontendCapabilitiesPlugin>('FrontendCapabilities');

export * from './definitions';
export { FrontendCapabilities };
