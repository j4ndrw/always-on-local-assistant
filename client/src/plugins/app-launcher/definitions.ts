export interface AppLauncherPlugin {
  canOpenUrl(options: { url: string }): Promise<{ value: boolean }>;
  openUrl(options: { url: string }): Promise<{ completed: boolean }>;
}
