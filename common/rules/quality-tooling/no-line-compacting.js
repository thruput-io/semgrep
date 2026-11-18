// ruleid: no-horizontal-line-cramming
export const crammedTotal = firstAlphaMetricValue + secondBravoMetricValue + thirdCharlieMetricValue + fourthDeltaMetricValue + fifthEchoMetricValue + sixthFoxtrotMetricValue + seventhGolfMetricValue + eighthHotelMetricValue;

// ok: no-horizontal-line-cramming
export const readableTotal = firstAlphaMetricValue + secondBravoMetricValue;

// ok: no-horizontal-line-cramming
export const referenceUrl = "https://thruput.se/agents/#single-purpose-components-and-read-far-more-than-written-with-a-very-long-anchor-path-segment-exceeding-two-hundred-characters-for-url-exemption-verification-test-case-coverage";

// ruleid: no-multi-statement-line-packing
const firstStep = 1; const secondStep = 2; const thirdStep = firstStep + secondStep;

// ok: no-multi-statement-line-packing
for (let index = 0; index < 3; index++) {
  console.log(index);
}
