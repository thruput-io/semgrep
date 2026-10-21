// ruleid: accept-unknown-properties
export const forbidUnknownSchema = {
  type: 'object',
  properties: { id: { type: 'string' } },
  additionalProperties: false,
};

export function rejectUnknownInZod(z) {
  // ruleid: accept-unknown-properties
  return z.object({ id: z.string() }).strict();
}

// ok: accept-unknown-properties
export const tolerantSchema = {
  type: 'object',
  properties: { id: { type: 'string' } },
};
