// ruleid: scripts-abort-on-error
process.on('unhandledRejection', (reason) => {
  console.warn('Ignored rejection:', reason);
});

// ruleid: scripts-abort-on-error
process.on('uncaughtException', (err) => {
  console.error('Continuing after uncaught exception:', err);
});

// ok: scripts-abort-on-error
process.on('unhandledRejection', (reason) => {
  console.error(reason);
  process.exit(1);
});
