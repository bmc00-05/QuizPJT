export const ANIMS = {
  idle_0: { row: 0, start: 0, frames: 8, fps: 8, loop: true },

  idle_1: { row: 2, start: 0, frames: 8, fps: 8, loop: true },
  idle_4: { row: 5, start: 0, frames: 8, fps: 8, loop: true },
  idle_7: { row: 8, start: 0, frames: 8, fps: 8, loop: true },
  idle_10: { row: 11, start: 0, frames: 8, fps: 8, loop: true },

  switch_2: { row: 1, start: 0, frames: 10, fps: 8, loop: false },
  switch_5: { row: 4, start: 0, frames: 10, fps: 8, loop: false },
  switch_8: { row: 7, start: 0, frames: 10, fps: 8, loop: false },
  switch_11: { row: 10, start: 0, frames: 10, fps: 8, loop: false },

  attack_3: { row: 3, start: 0, frames: 10, fps: 14, loop: false },
  attack_6: { row: 6, start: 0, frames: 10, fps: 14, loop: false },
  attack_9: { row: 9, start: 0, frames: 10, fps: 14, loop: false },
  attack_12: { row: 12, start: 0, frames: 10, fps: 14, loop: false },

  hurt: {
      row: 13,      // ✅ 피격 모션이 있는 row
      start: 0,    // ✅ 시작 프레임
      frames: 8,   // ✅ 프레임 수
      fps: 12,
      loop: false, // ✅ once로 끝나야 finished 발생
  },
  
}

export const PICK_RULES = {
  1: { switchOnce: "switch_2", idle: "idle_1", attackOnce: "attack_3" },
  2: { switchOnce: "switch_5", idle: "idle_4", attackOnce: "attack_6" },
  3: { switchOnce: "switch_8", idle: "idle_7", attackOnce: "attack_9" },
  4: { switchOnce: "switch_11", idle: "idle_10", attackOnce: "attack_12" },
}