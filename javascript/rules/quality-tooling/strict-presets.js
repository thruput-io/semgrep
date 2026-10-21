// ruleid: strict-presets
import nonStrictAssert from 'node:assert';

// ok: strict-presets
import strictAssert from 'node:assert/strict';

// ruleid: strict-presets
export const relaxedCompilerOptions = {
  strict: false,
};

// ok: strict-presets
export const strictCompilerOptions = {
  strict: true,
};

export { nonStrictAssert, strictAssert };
