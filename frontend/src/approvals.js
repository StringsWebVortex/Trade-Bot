/** Fold one approval event into the pending list (dedupe on request_id, drop on resolved). */
export function applyApproval(prev, ev) {
  const list = prev ?? [];
  if (ev.action === 'resolved') {
    return list.filter((a) => a.request_id !== ev.request_id);
  }
  if (list.some((a) => a.request_id === ev.request_id)) return list;
  return [...list, ev];
}
