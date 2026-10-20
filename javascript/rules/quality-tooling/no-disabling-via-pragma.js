// ruleid: no-disabling-via-pragma
// eslint-disable-next-line no-unused-vars
const suppressedVar = 1;

// ruleid: no-disabling-via-pragma
// @ts-ignore
const uncheckedValue = suppressedVar;

// ok: no-disabling-via-pragma
export const cleanValue = uncheckedValue + 1;
