<template>
  <canvas ref="canvasRef" class="block" />
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from "vue"

const props = defineProps({
  src: { type: String, required: true },

  frameWidth: { type: Number, required: true },
  frameHeight: { type: Number, required: true },
  cols: { type: Number, required: true },

  row: { type: Number, default: 0 },
  start: { type: Number, default: 0 },
  frames: { type: Number, default: 1 },

  fps: { type: Number, default: 8 },
  loop: { type: Boolean, default: true },
  play: { type: Boolean, default: true },

  scale: { type: Number, default: 1 },

  offsetX: { type: Number, default: 0 },
  offsetY: { type: Number, default: 0 },

  flipX: { type: Boolean, default: false },
})

const emit = defineEmits(["finished"])
const canvasRef = ref(null)

let img = null
let rafId = null
let lastTick = 0
let localFrame = 0
let imgReady = false

function stop() {
  if (rafId) cancelAnimationFrame(rafId)
  rafId = null
}

function start() {
  stop()
  rafId = requestAnimationFrame(tick)
}

function setCanvasSizeIfNeeded() {
  const canvas = canvasRef.value
  if (!canvas) return

  const w = Math.round(props.frameWidth * props.scale)
  const h = Math.round(props.frameHeight * props.scale)

  // ✅ 같으면 건드리지 않기 (여기서 깜빡임 대부분 제거됨)
  if (canvas.width !== w) canvas.width = w
  if (canvas.height !== h) canvas.height = h
}

function resetFrame(shouldRestart = true) {
  localFrame = 0
  lastTick = 0
  draw()                // ✅ 즉시 1프레임 그려서 “공백 프레임” 방지
  if (shouldRestart && props.play) start()
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
  if (!canvas || !img || !imgReady) return

  const ctx = canvas.getContext("2d")
  ctx.imageSmoothingEnabled = false

  // ✅ “그릴 수 있을 때만” 지우기 (이미지 준비 전 clear하면 빈 프레임)
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  const absoluteFrame = props.start + localFrame
  const col = absoluteFrame % props.cols

  const sx = col * props.frameWidth
  const sy = props.row * props.frameHeight

  const dw = props.frameWidth * props.scale
  const dh = props.frameHeight * props.scale

  const x = (canvas.width - dw) / 2 + props.offsetX
  const y = (canvas.height - dh) / 2 + props.offsetY

  ctx.save()

  if (props.flipX) {
    ctx.translate(x + dw, y)
    ctx.scale(-1, 1)
    ctx.drawImage(img, sx, sy, props.frameWidth, props.frameHeight, 0, 0, dw, dh)
  } else {
    ctx.drawImage(img, sx, sy, props.frameWidth, props.frameHeight, x, y, dw, dh)
  }

  ctx.restore()
}

async function loadImage(src) {
  imgReady = false
  img = new Image()
  img.src = src

  // ✅ decode 가능하면 decode가 깜빡임 줄이는데 도움 큼
  try {
    await img.decode?.()
  } catch (_) {
    // decode 미지원/실패 시 onload로 fallback
    await new Promise((resolve) => (img.onload = resolve))
  }

  imgReady = true
  setCanvasSizeIfNeeded()
  resetFrame(true)
}

onMounted(() => {
  setCanvasSizeIfNeeded()
  loadImage(props.src)
})

onBeforeUnmount(() => stop())

// ✅ 1) 사이즈 관련만: 캔버스 크기만 조절 (필요할 때만)
watch(
  () => [props.frameWidth, props.frameHeight, props.scale],
  () => {
    setCanvasSizeIfNeeded()
    // 크기 바뀌면 현재 프레임 다시 그리기
    draw()
  }
)

// ✅ 2) src 바뀔 때만: 이미지 재로딩
watch(
  () => props.src,
  (src) => {
    if (!src) return
    stop()
    loadImage(src)
  }
)

// ✅ 3) “클립 변경”만: 프레임 리셋(여기서 깜빡임 가장 많이 줄어듦)
watch(
  () => [props.cols, props.row, props.start, props.frames],
  () => {
    resetFrame(true)
  }
)

// ✅ 4) play만: 재생/정지
watch(
  () => props.play,
  (v) => {
    if (v) start()
    else stop()
  }
)

// ✅ 5) 그 외(오프셋/flip)는 그냥 다시 그리기만 (리셋 금지)
watch(
  () => [props.offsetX, props.offsetY, props.flipX],
  () => draw()
)
</script>
