export type HealthResponse = {
  status: string;
  version: string;
  ingestion_status: string;
  last_success_ingestion_time: string | null;
  total_docs: number;
  environment: string;
};

export type QueryResponse = {
  status?: string;
  message?: string;
  answer?: string;
  [key: string]: unknown;
};
