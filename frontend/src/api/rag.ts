import { requestJson } from "./client";
import type { HealthResponse, QueryResponse } from "../types/api";

export function getHealth(): Promise<HealthResponse> {
  return requestJson<HealthResponse>("/health", { method: "GET" });
}

export function postQuery(question: string): Promise<QueryResponse> {
  return requestJson<QueryResponse>("/query", {
    method: "POST",
    body: JSON.stringify({
      question,
    }),
  });
}
