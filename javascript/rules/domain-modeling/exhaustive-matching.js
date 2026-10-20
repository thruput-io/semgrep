export function labelForSide(side) {
  switch (side) {
    case 'head':
      return 'RIGHT';
    case 'base':
      return 'LEFT';
    // ruleid: exhaustive-matching
    default:
      return 'UNKNOWN';
  }
}

// ok: exhaustive-matching
const HOST_SIDE_OF = { head: 'RIGHT', base: 'LEFT' };
export const mappedSide = (side) => HOST_SIDE_OF[side];
