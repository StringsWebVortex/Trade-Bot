import { describe, expect, it } from 'vitest';

import { applyApproval } from './approvals.js';

describe('applyApproval (FE-21)', () => {
  it('appends a new request and dedupes on request_id', () => {
    const a = { request_id: 'r1', action: 'created' };
    const once = applyApproval(null, a);
    expect(once).toEqual([a]);
    expect(applyApproval(once, a)).toBe(once);
  });

  it('removes a request on resolved', () => {
    const list = [{ request_id: 'r1' }, { request_id: 'r2' }];
    expect(applyApproval(list, { request_id: 'r1', action: 'resolved' })).toEqual([{ request_id: 'r2' }]);
  });
});
