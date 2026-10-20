import test from 'node:test';
import assert from 'node:assert/strict';

test('branching inside a test is forbidden', () => {
  const actual = 42;
  // ruleid: linear-deterministic-code
  if (actual > 0) {
    assert.equal(actual, 42);
  }
});

test('looping inside a test is forbidden', () => {
  // ruleid: linear-deterministic-code
  for (const item of [1, 2]) {
    assert.equal(typeof item, 'number');
  }
});

// ok: linear-deterministic-code
test('linear test case', () => {
  assert.equal(20 + 22, 42);
});
