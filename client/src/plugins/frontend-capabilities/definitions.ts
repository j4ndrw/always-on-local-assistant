export interface FrontendCapabilitiesPlugin {
  getInstalledApps(): Promise<{ installedApps: string[] }>
}
