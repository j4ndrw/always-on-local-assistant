export interface AppLauncherPlugin {
  canOpenUrl(options: { url: string }): Promise<{ value: boolean }>;
  openUrl(options: { url: string }): Promise<{ completed: boolean }>;
  performActionOnExternalApp(options: {
    url: string;
    package: string;
  }): Promise<{ completed: boolean }>;
}
