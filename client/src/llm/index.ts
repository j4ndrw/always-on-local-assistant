import { frontendCapabilitySchema, handleFrontendCapabilities } from "@/agentic-frontend-capabilities";

export const executeSideEffectsDrivenByLLM = async (llmTools: Array<{ role: "tool", content: string }>) => {
  for await (const tool of llmTools) {
    try {
      const json = JSON.parse(tool.content);
      const frontendCapability = frontendCapabilitySchema.parse(json);
      await handleFrontendCapabilities(frontendCapability);
    } catch(err) {
      console.error("Could not execute side effect from LLM's response", err, tool);
    }
  }
}
