import { z } from "zod";
import { handleOpenAppCapability } from "./open-app";
import { capabilities } from "./capabilities";
import { handleOpenAppWithIntent } from "./open-app-with-intent";

export const frontendCapabilitySchema = z.object({
  archetype: z.literal("frontend-capability"),
  kind: z.union(capabilities),
  data: z.record(z.any()),
});

export const openAppDataSchema = z.object({ url: z.string() });

export const handleFrontendCapabilities = async ({
  kind,
  data,
}: z.infer<typeof frontendCapabilitySchema>) => {
  if (kind === "open-app") await handleOpenAppCapability(data);
  if (kind === "open-app-with-intent") await handleOpenAppWithIntent(data);
};
