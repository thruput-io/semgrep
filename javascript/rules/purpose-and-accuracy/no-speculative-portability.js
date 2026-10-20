import os from 'node:os';

// ruleid: no-speculative-portability
const binary = process.platform === 'win32' ? 'semgrep.exe' : 'semgrep';

// ruleid: no-speculative-portability
if (os.platform() !== 'linux') {
  throw new Error('unsupported');
}

// ok: no-speculative-portability
const designatedBinary = 'semgrep';
export { binary, designatedBinary };
