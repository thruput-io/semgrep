export function swallowSync(action) {
  // ruleid: no-silent-catch
  try {
    action();
  } catch (error) {
    console.warn(error);
  }
}

export function swallowPromise(promise) {
  // ruleid: no-silent-catch
  return promise.catch(() => {});
}

export function rethrowOnError(action) {
  // ok: no-silent-catch
  try {
    return action();
  } catch (error) {
    throw new Error('Action failed', { cause: error });
  }
}
