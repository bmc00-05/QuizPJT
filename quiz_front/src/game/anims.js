export const ANIMS = {
  idle_0: { row: 0, start: 0, frames: 8, fps: 8, loop: true },
  idle_2: { row: 2, start: 0, frames: 8, fps: 8, loop: true },
  idle_4: { row: 4, start: 0, frames: 8, fps: 8, loop: true },
  idle_6: { row: 6, start: 0, frames: 8, fps: 8, loop: true },
  idle_8: { row: 8, start: 0, frames: 8, fps: 8, loop: true },

  switch_1: { row: 1, start: 0, frames: 10, fps: 14, loop: false },
  switch_3: { row: 3, start: 0, frames: 10, fps: 14, loop: false },
  switch_5: { row: 5, start: 0, frames: 10, fps: 14, loop: false },
  switch_7: { row: 7, start: 0, frames: 10, fps: 14, loop: false },
}

export const PICK_RULES = {
  1: { once: "switch_1", loop: "idle_2" },
  2: { once: "switch_3", loop: "idle_4" },
  3: { once: "switch_5", loop: "idle_6" },
  4: { once: "switch_7", loop: "idle_8" },
}