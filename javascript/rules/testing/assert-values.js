import test from 'node:test';
import assert from 'node:assert/strict';

function checkLedger(name, probe, ledger) {
  return { name, probe, ledger };
}

// ruleid: assert-values
test('checkLedger accepts rows matching the rules in order without asserting return value', () => {
  checkLedger('g', {}, { headCommit: 'h', rows: [] });
});

test('doesNotThrow only checks absence of error', () => {
  // ruleid: assert-values
  assert.doesNotThrow(() => checkLedger('g', {}, { headCommit: 'h', rows: [] }));
});

// ok: assert-values
test('asserts actual returned value', () => {
  assert.deepEqual(checkLedger('g', {}, { headCommit: 'h', rows: [] }), {
    name: 'g',
    probe: {},
    ledger: { headCommit: 'h', rows: [] },
  });
});
