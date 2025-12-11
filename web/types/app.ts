export enum AppType {
  "chat" = "chat",
  "completion" = "completion",
}

export type VariableInput = {
  key: string;
  name: string;
  value: string;
};

export const AppModes = ["completion", "chat"] as const;
export type AppMode = (typeof AppModes)[number];

export const VariableTypes = ["string", "number", "select"] as const;
export type VariableType = (typeof VariableTypes)[number];