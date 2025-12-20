import { IWorkspace } from "@/models/common";
import type { Fetcher } from "swr";
import { get } from "./base";

export const fetchWorkspaces: Fetcher<
  { workspaces: IWorkspace[] },
  { url: string; params: Record<string, any> }
> = ({ url, params }) => {
  return get(url, { params }) as Promise<{ workspaces: IWorkspace[] }>;
};
