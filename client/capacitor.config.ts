import { CapacitorConfig } from "@capacitor/cli";

const config: CapacitorConfig = {
  appId: "com.j4ndrw.lola",
  appName: "Lola - Always On LLM Agent",
  webDir: "dist",
  plugins: { CapacitorHttp: { enabled: true } },
  android: { useLegacyBridge: true }
};

export default config;
