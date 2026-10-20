import test from 'node:test';
import assert from 'node:assert/strict';

export function configureFlakySuite(jest) {
  // ruleid: no-retry-on-failure
  jest.retryTimes(3);
}

// ruleid: no-retry-on-failure
export const playwrightConfig = { retries: 2 };

// ok: no-retry-on-failure
test('deterministic single-run test', () => {
  assert.equal(2 * 3, 6);
});
