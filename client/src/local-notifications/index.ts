import {
  ActionPerformed,
  LocalNotifications,
} from "@capacitor/local-notifications";

const interruptLolaNotificationAction = (title: string) => {
  const typeId = "interrupt-lola-action-type";
  const id = "interrupt-lola-action";
  return {
    interruptLola: {
      typeId,
      id,
      registerActionType: () =>
        LocalNotifications.registerActionTypes({
          types: [{ id: typeId, actions: [{ id, title }] }],
        }),
      action: (action: ActionPerformed) => ({
        call: async (audioCtxPool: AudioContext[], onDone: () => void) => {
          if (action.actionId === localNotificationActions.interruptLola.id)
            await Promise.all(audioCtxPool.map((ctx) => ctx.close()))
              .then(LocalNotifications.removeAllListeners)
              .then(onDone);
        },
      }),
    },
  } as const;
};

export const localNotificationActions = {
  channel: {
    id: "lola-always-on-llm-agent-notification-channel",
    name: "Lola - Always On LLM Agent",
  },
  ...interruptLolaNotificationAction("Interrupt Lola"),
};
