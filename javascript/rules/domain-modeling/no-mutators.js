function extendRangeInPlace(ranges, line) {
  const last = ranges.at(-1);
  // ruleid: no-mutators
  last.end = line;
}

class MutableOrder {
  // ruleid: no-mutators
  set status(nextStatus) {
    return nextStatus;
  }
}

function mutateViaAssign(target, patch) {
  // ruleid: no-mutators
  return Object.assign(target, patch);
}

// ok: no-mutators
export function extendRangeImmutably(range, line) {
  return { ...range, end: line };
}

export { extendRangeInPlace, MutableOrder, mutateViaAssign };
