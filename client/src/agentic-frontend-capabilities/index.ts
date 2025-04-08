import { AppLauncher } from "@/plugins/app-launcher";
import { z } from "zod";

export const frontendCapabilitySchema = z.object({
  archetype: z.literal("frontend-capability"),
  kind: z.literal("open-app"),
  data: z.record(z.any()),
});

export const openAppDataSchema = z.object({ url: z.string() });

export const handleFrontendCapabilities = async ({
  kind,
  data
}: z.infer<typeof frontendCapabilitySchema>) => {
  if (kind === "open-app") await handleOpenAppCapability(openAppDataSchema.parse(data));
};

const handleOpenAppCapability = async ({ url }: z.infer<typeof openAppDataSchema>) => {
  const { value: canOpenUrl } = await AppLauncher.canOpenUrl({ url });
  if (canOpenUrl) await AppLauncher.openUrl({ url });
}
