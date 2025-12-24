import slimeSheet from "@/assets/enemies/slime.png"
// import batSheet from "@/assets/enemies/bat.png"
// import goblinSheet from "@/assets/enemies/goblin.png"

// ✅ 적마다 애니메이션 맵이 다를 수 있으니 enemyAnims를 함께 둠
const SLIME_ANIMS = {
  idle:   { row: 0, start: 0, frames: 6, fps: 8, loop: true },
  hit:    { row: 4, start: 0, frames: 4, fps: 12, loop: false },
  attack: { row: 3, start: 0, frames: 12, fps: 14, loop: false },
  death: { row: 5, start: 0, frames: 4, fps: 14, loop: false },
}

const AXEMAN_ANIMS = {
  idle:   { row: 0, start: 0, frames: 8, fps: 10, loop: true },
  hit:    { row: 5, start: 0, frames: 4, fps: 14, loop: false },
  attack: { row: 4, start: 0, frames: 12, fps: 16, loop: false },
  death: { row: 6, start: 0, frames: 4, fps: 16, loop: false },
}

const ORC_ANIMS = {
  idle:   { row: 0, start: 0, frames: 8, fps: 10, loop: true },
  hit:    { row: 6, start: 0, frames: 4, fps: 14, loop: false },
  attack: { row: 3, start: 0, frames: 8, fps: 16, loop: false },
  death: { row: 7, start: 0, frames: 4, fps: 16, loop: false },
}

const ELETEORC_ANIMS = {
  idle:   { row: 0, start: 0, frames: 8, fps: 10, loop: true },
  attack: { row: 4, start: 0, frames: 9, fps: 16, loop: false },
  hit:   { row: 5, start: 0, frames: 4, fps: 14, loop: false },
  death: { row: 6, start: 0, frames: 4, fps: 16, loop: false },
}

const SKELETON_ANIMS = {
  idle:   { row: 0, start: 0, frames: 8, fps: 10, loop: true },
  hit:    { row: 4, start: 0, frames: 4, fps: 14, loop: false },
  attack: { row: 3, start: 0, frames: 9, fps: 16, loop: false },
  death: { row: 5, start: 0, frames: 4, fps: 16, loop: false },
}

const SWORDSKELETON_ANIMS = {
  idle:   { row: 0, start: 0, frames: 8, fps: 10, loop: true },
  hit:    { row: 5, start: 0, frames: 4, fps: 14, loop: false },
  attack: { row: 3, start: 0, frames: 12, fps: 16, loop: false },
  death:  { row: 6, start: 0, frames: 4, fps: 16, loop: false },
}

const TEMPLER_ANIMS = {
  idle:   { row: 0, start: 0, frames: 8, fps: 10, loop: true },
  hit:    { row: 5, start: 0, frames: 4, fps: 14, loop: false },
  attack: { row: 3, start: 0, frames: 12, fps: 16, loop: false },
  death:  { row: 6, start: 0, frames: 4, fps: 16, loop: false },
}









export const ENEMIES = {
  slime: {
    id: "slime",
    sheet: slimeSheet,
    frameWidth: 100,
    frameHeight: 100,
    cols: 12,
    scale: 3,
    flipX: true,
    offsetX: -10,
    offsetY: 30,
    anims: SLIME_ANIMS,
  },
//   bat: {
//     id: "bat",
//     sheet: batSheet,
//     frameWidth: 64,
//     frameHeight: 64,
//     cols: 8,
//     scale: 4,
//     flipX: true,
//     offsetX: 0,
//     offsetY: -10,
//     anims: BAT_ANIMS,
//   },
//   goblin: {
//     id: "goblin",
//     sheet: goblinSheet,
//     frameWidth: 64,
//     frameHeight: 64,
//     cols: 7,
//     scale: 4,
//     flipX: true,
//     offsetX: 0,
//     offsetY: 0,
//     anims: SLIME_ANIMS, // 예시: 같으면 공유 가능
//   },
}