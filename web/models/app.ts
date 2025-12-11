import type { App, AppTemplate, SiteConfig } from "@/types/app";

export type AppMode = "chat" | "completion";

export type AppListResponse = {
  data: App[];
};

export type AppDetailResponse = App;

export type AppTemplatesResponse = {
  data: AppTemplate[];
};

export type CreateAppResponse = App;

export type UpdateAppNameResponse = App;

export type UpdateAppSiteCodeResponse = { app_id: string } & SiteConfig;

export type AppDailyConversationsResponse = {
  data: Array<{ date: string; conversation_count: number }>;
};

export type AppDailyEndUsersResponse = {
  data: Array<{ date: string; terminal_count: number }>;
};

export type AppTokenCostsResponse = {
  data: Array<{
    date: string;
    token_count: number;
    total_price: number;
    currency: number;
  }>;
};

export type UpdateAppModelConfigResponse = { result: string };

export type ApikeyItemResponse = {
  id: string;
  token: string;
  last_used_at: string;
  created_at: string;
};

export type ApikeysListResponse = {
  data: ApikeyItemResponse[];
};

export type CreateApiKeyResponse = {
  id: string;
  token: string;
  created_at: string;
};

export type ValidateOpenAIKeyResponse = {
  result: string;
  error?: string;
};

export type UpdateOpenAIKeyResponse = ValidateOpenAIKeyResponse;

export type GenerationIntroductionResponse = {
  introduction: string;
};
