import { AppLauncher } from "@/plugins/app-launcher";
import { z } from "zod";

const schema = z.object({ url: z.string() });

export const handleOpenAppCapability = async (data: unknown) => {
  const { url } = schema.parse(data);
  const { value: canOpenUrl } = await AppLauncher.canOpenUrl({ url });
  if (canOpenUrl) await AppLauncher.openUrl({ url });
};
