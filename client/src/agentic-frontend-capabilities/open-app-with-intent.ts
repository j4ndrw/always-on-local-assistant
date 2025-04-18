import { AppLauncher } from "@/plugins/app-launcher";
import { z } from "zod";

const schema = z.object({ package: z.string(), url: z.string() });

export const handleOpenAppWithIntent = async (data: unknown) => {
  const { url, package: pkg } = schema.parse(data);

  const { value: canOpenUrl } = await AppLauncher.canOpenUrl({ url: pkg });
  if (canOpenUrl)
    await AppLauncher.performActionOnExternalApp({ url, package: pkg });
};
