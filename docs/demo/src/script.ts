// The session replayed in the demo. Prompts and tool output are taken from the real
// run that produced projects/sofia_garden (see public/*-build.txt for the raw output).

export type Line =
  | {kind: "user"; text: string; at: number; typeFor: number}
  | {kind: "claude"; text: string; at: number}
  | {kind: "tool"; text: string; at: number}
  | {kind: "out" | "ok" | "err"; text: string; at: number};

export const FPS = 30;
export const DURATION = 640; // ends on the revised drawing, no title card

export const LINES: Line[] = [
  {kind: "user", at: 0, typeFor: 45,
    text: "Design a garden for my house in Sofia. Plot 12 × 18 m, Japanese style, a small pond."},
  {kind: "claude", at: 62, text: "Before I draw anything, five questions:"},
  {kind: "out", at: 70, text: "1. Where is the house, and which way is north?"},
  {kind: "out", at: 77, text: "2. Who uses the garden: kids, pets?"},
  {kind: "out", at: 84, text: "3. Neighbours close? Where do you need privacy?"},
  {kind: "out", at: 91, text: "4. Grill or fire? Evening use?"},
  {kind: "out", at: 98, text: "5. How many hours a week for upkeep?"},
  {kind: "user", at: 125, typeFor: 55,
    text: "House on the north, 10×6 m. Two of us and a dog. Neighbours east. Grill: yes, evenings. ~2 h a week."},
  {kind: "claude", at: 200,
    text: "Plan: deck + grill by the house, pond as the centre of the view, gravel garden by the gate, yew hedge on the east, lit stepping-stone path. Saved plan.md."},
  {kind: "tool", at: 232, text: "uv run cad-helper build sofia_garden"},
  {kind: "out", at: 252, text: "186 entities on 24 layers  →  sofia_garden.dxf"},
  {kind: "ok", at: 260, text: "Checks: all passed"},
  {kind: "claude", at: 290, text: "Done. Checked preview.png: path, pond and deck read well."},
  {kind: "user", at: 345, typeFor: 38,
    text: "Love it. Bigger pond, and swap the gravel garden for a fire pit."},
  {kind: "tool", at: 398, text: "uv run cad-helper build sofia_garden"},
  {kind: "err", at: 420, text: "Checks: 2 error(s)"},
  {kind: "err", at: 427, text: "FIRE_PIT ↔ NIWAKI is 1549 mm, needs ≥ 3000 mm (sparks vs pine crown)"},
  {kind: "err", at: 434, text: "FIRE_PIT_SEATING ↔ POND is 0 mm, needs ≥ 300 mm"},
  {kind: "claude", at: 455,
    text: "Fire is too close to the pine and the bench hits the bigger pond. Moving the pine 1.4 m east, the pit 0.5 m south-west."},
  {kind: "tool", at: 488, text: "uv run cad-helper build sofia_garden"},
  {kind: "out", at: 508, text: "149 entities on 26 layers  →  sofia_garden.dxf"},
  {kind: "ok", at: 515, text: "Checks: all passed"},
  {kind: "claude", at: 545,
    text: "Updated. Also pulled the lawn off the pond and added a path to the fire circle."},
];

// Workflow phase shown in the header, by frame.
export const PHASES: {from: number; label: string}[] = [
  {from: 0, label: "brief"},
  {from: 200, label: "plan"},
  {from: 232, label: "build"},
  {from: 285, label: "review"},
  {from: 345, label: "brief"},
  {from: 398, label: "build"},
  {from: 540, label: "review"},
];

export const V1_AT = 262; // first drawing appears
export const V2_AT = 518; // revised drawing replaces it
export const FIRE_PIT = {x: 0.3425, y: 0.807}; // fire pit in v2.png, as a fraction of the image
