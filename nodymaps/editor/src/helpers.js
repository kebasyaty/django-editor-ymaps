/*
 * Global support solutions.
 */

export default {
  // Rounding Coordinates.
  roundCoord: (num) => Math.round(+num * 1000000) / 1000000,
  // Coordinate check
  checkLatitude: (coord) => /^-?([1-8]?\d(\.\d+)?|90(\.0+)?)$/.test(coord),
  checkLongitude: (coord) =>
    /^-?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$/.test(coord),
};
