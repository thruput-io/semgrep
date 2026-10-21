const PULL_REQUEST_URL = /^https:\/\/github\.com\/([^/]+)\/([^/]+)\/pull\/(\d+)/;

export function locate(target) {
  const match = PULL_REQUEST_URL.exec(target);
  if (match === null) {
    // ruleid: no-optionality
    return undefined;
  }
  return { owner: match[1], repository: match[2], number: Number(match[3]) };
}

// ruleid: no-optionality
export function runWithDefault(command, args, encoding = 'utf8') {
  return { command, args, encoding };
}

// ok: no-optionality
export function runUtf8(command, args) {
  return { command, args, encoding: 'utf8' };
}
