export interface AudioManagerPlugin {
  muteNotifications(): Promise<void>;
  unmuteNotifications(): Promise<void>;
}
