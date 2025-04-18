import { z } from "zod";

export const capabilities = [
  z.literal("open-app"),
  z.literal("open-app-with-intent"),
] as const;

