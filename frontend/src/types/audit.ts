export type AuditLog = {
  id: number;
  actor_id: number;
  action: string;
  entity: string;
  entity_id?: number;
  created_at: string;
};

export type AuditLogResponse = {
  items: AuditLog[];
  page: number;
  page_size: number;
  total: number;
};
