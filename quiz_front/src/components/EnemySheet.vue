<template>
  <!-- 부모가 absolute 중앙정렬을 하든, 그냥 inline으로 두든 문제 없게 block -->
  <canvas ref="canvasRef" class="block" />
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from "vue"

const props = defineProps({
  src: { type: String, required: true },

  // 한 프레임 크기
  frameWidth: { type: Number, required: true },
  frameHeight: { type: Number, required: true },

  // 스프라이트 시트에서 "한 줄에 몇 프레임(열)"인지
  cols: { type: Number, required: true },

  // 현재 재생할 클립 정보
  row: { type: Number, default: 0 },     // 0-based row
  start: { type: Number, default: 0 },   // row 안에서 시작 프레임(0-based)
  frames: { type: Number, default: 1 },  // 재생 프레임 수

  fps: { type: Number, default: 8 },
  loop: { type: Boolean, default: true },
  play: { type: Boolean, default: true },

  // 렌더링 스케일
  scale: { type: Number, default: 1 },

  // ✅ (선택) 중앙 기준 미세 보정 (캐릭터 피벗 맞추기)
  offsetX: { type: Number, default: 0 },
  offsetY: { type: Number, default: 0 },

  // ✅ 좌우/상하 반전
  flipX: { type: Boolean, default: false },
  flipY: { type: Boolean, default: false },
})

const emit = defineEmits(["finished"])

const canvasRef = ref(null)

let img = null
let rafId = null
let lastTick = 0
let localFrame = 0 // 0..frames-1

function stop() {
  if (rafId) {
    cancelAnimationFrame(rafId)
    rafId = null
  }
}

function start() {
  stop()
  rafId = requestAnimationFrame(tick)
}

function reset() {
  localFrame = 0
  lastTick = 0
  draw()
  if (props.play) start()
}

function tick(t) {
  if (!props.play) {
    stop()
    return
  }

  const interval = 1000 / Math.max(1, props.fps)

  if (!lastTick) lastTick = t
  if (t - lastTick >= interval) {
    lastTick = t
    localFrame += 1

    if (localFrame >= props.frames) {
      if (props.loop) {
        localFrame = 0
      } else {
        localFrame = Math.max(0, props.frames - 1)
        draw()
        stop()
        emit("finished")
        return
      }
    }

    draw()
  }

  rafId = requestAnimationFrame(tick)
}

function draw() {
  const canvas = canvasRef.value
  if (!canvas || !img) return

  const ctx = canvas.getContext("2d")
  ctx.imageSmoothingEnabled = false
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  // ✅ 클립 기준 실제 프레임 인덱스
  const absoluteFrame = props.start + localFrame

  // ✅ 현재 구현은 "한 row 안에서 cols 기준"으로만 순환
  const col = absoluteFrame % props.cols

  const sx = col * props.frameWidth
  const sy = props.row * props.frameHeight

  const dw = props.frameWidth * props.scale
  const dh = props.frameHeight * props.scale

  // ✅ 캔버스 중앙 배치 + offset
  // flip일 때 offset이 직관적으로 느껴지도록 X/Y는 반전 시 부호 반대로 적용
  const ox = props.flipX ? -props.offsetX : props.offsetX
  const oy = props.flipY ? -props.offsetY : props.offsetY

  const x = (canvas.width - dw) / 2 + ox
  const y = (canvas.height - dh) / 2 + oy

  ctx.save()

  // ✅ flip 적용: 좌표계를 뒤집고 그리기
  // flipX면 (x+dw)로 이동 후 scaleX(-1)
  // flipY면 (y+dh)로 이동 후 scaleY(-1)
  const tx = props.flipX ? x + dw : x
  const ty = props.flipY ? y + dh : y
  ctx.translate(tx, ty)
  ctx.scale(props.flipX ? -1 : 1, props.flipY ? -1 : 1)

  ctx.drawImage(
    img,
    sx,
    sy,
    props.frameWidth,
    props.frameHeight,
    0,
    0,
    dw,
    dh
  )

  ctx.restore()
}

function resizeCanvas() {
  const canvas = canvasRef.value
  if (!canvas) return
  canvas.width = props.frameWidth * props.scale
  canvas.height = props.frameHeight * props.scale
}

function loadImageIfNeeded() {
  if (img && img.src === props.src) return

  img = new Image()
  img.onload = () => reset()
  img.src = props.src
}

onMounted(() => {
  resizeCanvas()
  loadImageIfNeeded()
})

onBeforeUnmount(() => {
  stop()
})

// ✅ props 변경 시 재시작(클립/속도/재생상태 변경 대응)
watch(
  () => [
    props.src,
    props.frameWidth,
    props.frameHeight,
    props.scale,
    props.cols,
    props.row,
    props.start,
    props.frames,
    props.fps,
    props.loop,
    props.play,
    props.offsetX,
    props.offsetY,
    props.flipX,
    props.flipY,
  ],
  () => {
    resizeCanvas()
    loadImageIfNeeded()

    // src가 같고 이미지 로딩이 끝난 상태라면 바로 reset
    // (src가 바뀐 경우는 onload에서 reset됨)
    if (img && img.src === props.src && img.complete) {
      reset()
    }
  }
)
</script>
