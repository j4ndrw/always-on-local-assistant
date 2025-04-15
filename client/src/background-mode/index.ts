import { BackgroundMode } from "@anuradev/capacitor-background-mode";

export const moveAppToBackground = async () => {
  await BackgroundMode.enable();
  await BackgroundMode.requestNotificationsPermission();
  await BackgroundMode.requestMicrophonePermission();
  await BackgroundMode.requestDisableBatteryOptimizations();
  await BackgroundMode.moveToBackground();
  await BackgroundMode.addListener(
    "appInForeground",
    BackgroundMode.moveToBackground,
  );
};
