import { execSync } from 'node:child_process';

export function runIgnoringExitCode() {
  // ruleid: no-suppressed-exit-status
  return execSync('semgrep scan . || true');
}

export function exitZeroOnError(task) {
  // ruleid: no-suppressed-exit-status
  try {
    task();
  } catch (error) {
    process.exit(0);
  }
}

// ok: no-suppressed-exit-status
export function runCheckingExitCode() {
  return execSync('semgrep scan .');
}
