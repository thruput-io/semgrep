import test from 'node:test';
import assert from 'node:assert/strict';

// ruleid: no-muted-tests
test.skip('muted via test.skip', () => {
  assert.equal(1, 1);
});

// ruleid: no-muted-tests
test('muted via options object', { skip: 'flaky upstream' }, () => {
  assert.equal(1, 1);
});

// ok: no-muted-tests
test('active test executes normally', () => {
  assert.equal(1, 1);
});
