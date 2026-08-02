import type { OptimizationOpportunity, ValueSummary } from "@/lib/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, { cache: "no-store" });

  if (!response.ok) {
    throw new Error(`Value Hub API request failed with status ${response.status}`);
  }

  return (await response.json()) as T;
}

export function getValueSummary(): Promise<ValueSummary> {
  return request<ValueSummary>("/api/v1/value/summary");
}

export function getOptimizationOpportunities(): Promise<OptimizationOpportunity[]> {
  return request<OptimizationOpportunity[]>("/api/v1/value/opportunities");
}
