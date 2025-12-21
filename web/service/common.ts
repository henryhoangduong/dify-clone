import { CommonResponse, IWorkspace } from "@/models/common";
import type { Fetcher } from "swr";
import { get, post } from "./base";

export const login: Fetcher<
  CommonResponse,
  { url: string; body: Record<string, any> }
> = ({ url, body }) => {
  return post(url, { body }) as Promise<CommonResponse>;
};

export const fetchWorkspaces: Fetcher<
  { workspaces: IWorkspace[] },
  { url: string; params: Record<string, any> }
> = ({ url, params }) => {
  return get(url, { params }) as Promise<{ workspaces: IWorkspace[] }>;
};
