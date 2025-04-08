import { CapacitorHttp } from "@capacitor/core";
import { SECRET } from "@/constants";
import { BASE_URL } from ".";
import { z } from "zod";

export const endpoint = "/api/conversation";

export const conversationResponseSchema = z.array(z.object({
  role: z.literal('user').or(z.literal('assistant')).or(z.literal('system')).or(z.literal('tool')),
  content: z.string().nullish(),
}))

export const getConversation = async (prompt: string, metadata: object) => {
  try {
    const response = await CapacitorHttp.post({
      url: `${BASE_URL}${endpoint}`,
      data: JSON.stringify({ prompt, metadata }),
      headers: {
        "Content-Type": "application/json",
        "x-secret": SECRET,
      },
    });
    const { data, error } = await conversationResponseSchema.safeParseAsync(JSON.parse(response.data));
    if (error) {
      console.error(error);
      return null;
    }
    return data;
  } catch (err) {
    console.error(err);
    return null;
  }
};
