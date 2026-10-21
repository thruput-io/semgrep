#!/usr/bin/env node

// ruleid: no-comments-in-code
// Increment counter by one
const incremented = (value) => value + 1;

// ruleid: no-comments-in-code
/* Temporary workaround for upstream issue */
const doubled = (value) => value * 2;

// ok: no-comments-in-code
/**
 * @param {number} value
 * @returns {number}
 */
export const tripled = (value) => incremented(value) + doubled(value);
