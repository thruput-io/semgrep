export function parseHeader(line) {
  // ruleid: no-default-on-failure
  return /^diff --git a\/(.+) b\/(.+)$/.exec(line)?.[2] ?? '/dev/null';
}

export function readOrFallback(read, path) {
  // ruleid: no-default-on-failure
  try {
    return JSON.parse(read(path));
  } catch (error) {
    return {};
  }
}

// ok: no-default-on-failure
export function parseStrict(read, path) {
  return JSON.parse(read(path));
}
