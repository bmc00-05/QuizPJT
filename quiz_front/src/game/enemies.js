import slimeSheet from "@/assets/enemies/slime.png"
import axemanSheet from "@/assets/enemies/armored_axeman.png"
import armoredorcSheet from "@/assets/enemies/armored_orc.png"
import armoredskeletonSheet from "@/assets/enemies/armored_skeleton.png"
import eliteorcSheet from "@/assets/enemies/elite_orc.png"
import swordskeletonSheet from "@/assets/enemies/greatsword_skeleton.png"
import templerSheet from "@/assets/enemies/knight_templar.png"
import knightSheet from "@/assets/enemies/knight.png"
import lancerSheet from "@/assets/enemies/lancer.png"
import orcriderSheet from "@/assets/enemies/orc_rider.png"
import orcSheet from "@/assets/enemies/orc.png"
import skeletonarcherSheet from "@/assets/enemies/skeleton_archer.png"
import skeletonSheet from "@/assets/enemies/skeleton.png"
import soldierSheet from "@/assets/enemies/soldier.png"
import swordmanSheet from "@/assets/enemies/swordsman.png"
import werebearSheet from "@/assets/enemies/werebear.png"
import werewolfSheet from "@/assets/enemies/werewolf.png"


// ✅ 적마다 애니메이션 맵이 다를 수 있으니 enemyAnims를 함께 둠
const SLIME_ANIMS = {
  idle:   { row: 0, start: 0, frames: 6, fps: 8, loop: true },
  hit:    { row: 4, start: 0, frames: 4, fps: 12, loop: false },
  attack: { row: 3, start: 0, frames: 12, fps: 14, loop: false },
  death: { row: 5, start: 0, frames: 4, fps: 14, loop: false },
  walk: { row: 1, start: 0, frames: 8, fps: 14, loop: true },
}

const AXEMAN_ANIMS = {
  idle:   { row: 0, start: 0, frames: 6, fps: 10, loop: true },
  hit:    { row: 5, start: 0, frames: 4, fps: 14, loop: false },
  attack: { row: 4, start: 0, frames: 12, fps: 16, loop: false },
  death: { row: 6, start: 0, frames: 4, fps: 16, loop: false },
  walk: { row: 1, start: 0, frames: 8, fps: 14, loop: true },
}

const ARMOREDORC_ANIMS = {
  idle:   { row: 0, start: 0, frames: 6, fps: 10, loop: true },
  hit:    { row: 6, start: 0, frames: 4, fps: 14, loop: false },
  attack: { row: 3, start: 0, frames: 8, fps: 16, loop: false },
  death: { row: 7, start: 0, frames: 4, fps: 16, loop: false },
  walk: { row: 1, start: 0, frames: 8, fps: 14, loop: true },
}

const ORC_ANIMS = {
  idle:   { row: 0, start: 0, frames: 6, fps: 10, loop: true },
  hit:    { row: 4, start: 0, frames: 4, fps: 14, loop: false },
  attack: { row: 3, start: 0, frames: 6, fps: 16, loop: false },
  death: { row: 5, start: 0, frames: 4, fps: 16, loop: false },
  walk: { row: 1, start: 0, frames: 8, fps: 14, loop: true },
}

const ELETEORC_ANIMS = {
  idle:   { row: 0, start: 0, frames: 6, fps: 10, loop: true },
  attack: { row: 4, start: 0, frames: 9, fps: 16, loop: false },
  hit:   { row: 5, start: 0, frames: 4, fps: 14, loop: false },
  death: { row: 6, start: 0, frames: 4, fps: 16, loop: false },
  walk: { row: 1, start: 0, frames: 8, fps: 14, loop: true },
}

const ARMOREDSKELETON_ANIMS = {
  idle:   { row: 0, start: 0, frames: 6, fps: 10, loop: true },
  hit:    { row: 4, start: 0, frames: 4, fps: 14, loop: false },
  attack: { row: 3, start: 0, frames: 9, fps: 16, loop: false },
  death: { row: 5, start: 0, frames: 4, fps: 16, loop: false },
  walk: { row: 1, start: 0, frames: 8, fps: 14, loop: true },
}

const SKELETON_ANIMS = {
  idle:   { row: 0, start: 0, frames: 6, fps: 10, loop: true },
  hit:    { row: 5, start: 0, frames: 4, fps: 14, loop: false },
  attack: { row: 3, start: 0, frames: 7, fps: 16, loop: false },
  death: { row: 6, start: 0, frames: 4, fps: 16, loop: false },
  walk: { row: 1, start: 0, frames: 8, fps: 14, loop: true },
}

const SKELETONARCHER_ANIMS = {
  idle:   { row: 0, start: 0, frames: 6, fps: 10, loop: true },
  hit:    { row: 3, start: 0, frames: 4, fps: 14, loop: false },
  attack: { row: 2, start: 0, frames: 9, fps: 16, loop: false },
  death: { row: 4, start: 0, frames: 4, fps: 16, loop: false },
  walk: { row: 1, start: 0, frames: 8, fps: 14, loop: true },
}

const SWORDSKELETON_ANIMS = {
  idle:   { row: 0, start: 0, frames: 6, fps: 10, loop: true },
  hit:    { row: 5, start: 0, frames: 4, fps: 14, loop: false },
  attack: { row: 3, start: 0, frames: 12, fps: 16, loop: false },
  death:  { row: 6, start: 0, frames: 4, fps: 16, loop: false },
  walk: { row: 1, start: 0, frames: 8, fps: 14, loop: true },
}
const SOLDIER_ANIMS = {
  idle:   { row: 0, start: 0, frames: 6, fps: 10, loop: true },
  hit:    { row: 5, start: 0, frames: 4, fps: 14, loop: false },
  attack: { row: 2, start: 0, frames: 6, fps: 16, loop: false },
  death:  { row: 6, start: 0, frames: 4, fps: 16, loop: false },
  walk: { row: 1, start: 0, frames: 8, fps: 14, loop: true },
}

const TEMPLER_ANIMS = {
  idle:   { row: 0, start: 0, frames: 6, fps: 10, loop: true },
  hit:    { row: 7, start: 0, frames: 4, fps: 14, loop: false },
  attack: { row: 5, start: 0, frames: 12, fps: 16, loop: false },
  death:  { row: 8, start: 0, frames: 4, fps: 16, loop: false },
  walk: { row: 1, start: 0, frames: 8, fps: 14, loop: true },
}

const KNIGHT_ANIMS = {
  idle:   { row: 0, start: 0, frames: 6, fps: 10, loop: true },
  hit:    { row: 6, start: 0, frames: 4, fps: 14, loop: false },
  attack: { row: 4, start: 0, frames: 11, fps: 16, loop: false },
  death:  { row: 7, start: 0, frames: 4, fps: 16, loop: false },
  walk: { row: 1, start: 0, frames: 8, fps: 14, loop: true },
}

const LANCER_ANIMS = {
  idle:   { row: 0, start: 0, frames: 6, fps: 10, loop: true },
  hit:    { row: 6, start: 0, frames: 4, fps: 14, loop: false },
  attack: { row: 4, start: 0, frames: 9, fps: 16, loop: false },
  death:  { row: 7, start: 0, frames: 4, fps: 16, loop: false },
  walk: { row: 1, start: 0, frames: 8, fps: 14, loop: true },
}

const ORCRIDER_ANIMS = {
  idle:   { row: 0, start: 0, frames: 6, fps: 10, loop: true },
  hit:    { row: 6, start: 0, frames: 4, fps: 14, loop: false },
  attack: { row: 4, start: 0, frames: 11, fps: 16, loop: false },
  death:  { row: 7, start: 0, frames: 4, fps: 16, loop: false },
  walk: { row: 1, start: 0, frames: 8, fps: 14, loop: true },
}

const SWORDMAN_ANIMS  = {
  idle:   { row: 0, start: 0, frames: 6, fps: 10, loop: true },
  hit:    { row: 5, start: 0, frames: 4, fps: 14, loop: false },
  attack: { row: 3, start: 0, frames: 15, fps: 16, loop: false },
  death:  { row: 6, start: 0, frames: 4, fps: 16, loop: false },
  walk: { row: 1, start: 0, frames: 8, fps: 14, loop: true },
}

const WEREBERE_ANIMS  = {
  idle:   { row: 0, start: 0, frames: 6, fps: 10, loop: true },
  hit:    { row: 5, start: 0, frames: 4, fps: 14, loop: false },
  attack: { row: 3, start: 0, frames: 13, fps: 16, loop: false },
  death:  { row: 6, start: 0, frames: 4, fps: 16, loop: false },
  walk: { row: 1, start: 0, frames: 8, fps: 14, loop: true },
}

const WEREWOLF_ANIMS  = {
  idle:   { row: 0, start: 0, frames: 6, fps: 10, loop: true },
  hit:    { row: 4, start: 0, frames: 4, fps: 14, loop: false },
  attack: { row: 3, start: 0, frames: 13, fps: 16, loop: false },
  death:  { row: 5, start: 0, frames: 4, fps: 16, loop: false },
  walk: { row: 1, start: 0, frames: 8, fps: 14, loop: true },
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
    offsetX: -30,
    offsetY: 30,
    anims: SLIME_ANIMS,
  },

  axeman: {
    id: "axeman",
    sheet: axemanSheet,
    frameWidth: 100,
    frameHeight: 100,
    cols: 12,
    scale: 2.8,
    flipX: true,
    offsetX: -30,
    offsetY: 30,
    anims: AXEMAN_ANIMS,
  },

  armored_orc: {
    id: "armored_orc",
    sheet: armoredorcSheet,
    frameWidth: 100,
    frameHeight: 100,
    cols: 12,
    scale: 2.8,
    flipX: true,
    offsetX: -30,
    offsetY: 30,
    anims: ARMOREDORC_ANIMS,
  },

  orc: {
    id: "orc",
    sheet: orcSheet,
    frameWidth: 100,
    frameHeight: 100,
    cols: 12,
    scale: 2.8,
    flipX: true,
    offsetX: -10,
    offsetY: 30,
    anims: ORC_ANIMS,
  },

  elite_orc: {
    id: "elite_orc",
    sheet: eliteorcSheet,
    frameWidth: 100,
    frameHeight: 100,
    cols: 12,
    scale: 3.0,
    flipX: true,
    offsetX: -30,
    offsetY: 30,
    anims: ELETEORC_ANIMS,
  },

  armored_skeleton: {
    id: "armored_skeleton",
    sheet: armoredskeletonSheet,
    frameWidth: 100,
    frameHeight: 100,
    cols: 12,
    scale: 2.8,
    flipX: true,
    offsetX: -30,
    offsetY: 30,
    anims: ARMOREDSKELETON_ANIMS,
  },

  skeleton: {
    id: "skeleton",
    sheet: skeletonSheet,
    frameWidth: 100,
    frameHeight: 100,
    cols: 12,
    scale: 2.8,
    flipX: true,
    offsetX: -30,
    offsetY: 30,
    anims: SKELETON_ANIMS,
  },

  skeleton_archer: {
    id: "skeleton_archer",
    sheet: skeletonarcherSheet,
    frameWidth: 100,
    frameHeight: 100,
    cols: 12,
    scale: 2.8,
    flipX: true,
    offsetX: -30,
    offsetY: 30,
    anims: SKELETONARCHER_ANIMS,
  },

  greatsword_skeleton: {
    id: "greatsword_skeleton",
    sheet: swordskeletonSheet,
    frameWidth: 100,
    frameHeight: 100,
    cols: 12,
    scale: 3.0,
    flipX: true,
    offsetX: -30,
    offsetY: 30,
    anims: SWORDSKELETON_ANIMS,
  },

  knight_templer: {
    id: "knight_templer",
    sheet: templerSheet,
    frameWidth: 100,
    frameHeight: 100,
    cols: 12,
    scale: 3.0,
    flipX: true,
    offsetX: -30,
    offsetY: 30,
    anims: TEMPLER_ANIMS,
  },

  knight: {
    id: "knight",
    sheet: knightSheet,
    frameWidth: 100,
    frameHeight: 100,
    cols: 12,
    scale: 3.0,
    flipX: true,
    offsetX: -30,
    offsetY: 30,
    anims: KNIGHT_ANIMS,
  },

  lancer: {
    id: "lancer",
    sheet: lancerSheet,
    frameWidth: 100,
    frameHeight: 100,
    cols: 12,
    scale: 3.0,
    flipX: true,
    offsetX: -30,
    offsetY: 30,
    anims: LANCER_ANIMS,
  },

  orc_rider: {
    id: "orc_rider",
    sheet: orcriderSheet,
    frameWidth: 100,
    frameHeight: 100,
    cols: 12,
    scale: 3.2,
    flipX: true,
    offsetX: -30,
    offsetY: 30,
    anims: ORCRIDER_ANIMS ,
  },

  swordman: {
    id: "swordman",
    sheet: swordmanSheet,
    frameWidth: 100,
    frameHeight: 100,
    cols: 12,
    scale: 3.0,
    flipX: true,
    offsetX: -30,
    offsetY: 30,
    anims: SWORDMAN_ANIMS ,
  },

  soldier: {
    id: "soldier",
    sheet: soldierSheet,
    frameWidth: 100,
    frameHeight: 100,
    cols: 12,
    scale: 3.0,
    flipX: true,
    offsetX: -30,
    offsetY: 30,
    // ✅ soldier는 애님 정의가 없어서 일단 swordman 애님 재사용(나중에 교체)
    anims: SOLDIER_ANIMS,
  },

  werebear: {
    id: "werebear",
    sheet: werebearSheet,
    frameWidth: 100,
    frameHeight: 100,
    cols: 12,
    scale: 3.2,
    flipX: true,
    offsetX: -30,
    offsetY: 30,
    anims: WEREBERE_ANIMS ,
  },

  werewolf: {
    id: "werewolf",
    sheet: werewolfSheet,
    frameWidth: 100,
    frameHeight: 100,
    cols: 12,
    scale: 3.2,
    flipX: true,
    offsetX: -30,
    offsetY: 30,
    anims: WEREWOLF_ANIMS ,
  },
}