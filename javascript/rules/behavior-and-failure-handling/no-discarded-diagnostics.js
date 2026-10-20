import { execSync, spawnSync } from 'node:child_process';

export function spawnSilently(cmd, args) {
  // ruleid: no-discarded-diagnostics
  return spawnSync(cmd, args, { stdio: 'ignore' });
}

export function execRedirectingStderr() {
  // ruleid: no-discarded-diagnostics
  return execSync('git rev-parse --verify HEAD 2>/dev/null');
}

// ok: no-discarded-diagnostics
export function spawnWithDiagnostics(cmd, args) {
  return spawnSync(cmd, args, { encoding: 'utf8' });
}
