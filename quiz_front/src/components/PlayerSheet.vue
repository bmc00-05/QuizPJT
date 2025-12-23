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

function reset() {
  localFrame = 0
  lastTick = 0
  draw()
  if (props.play) start()
}

function start() {
  stop()
  rafId = requestAnimationFrame(tick)
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

    // 마지막 프레임 처리
    if (localFrame >= props.frames) {
      if (props.loop) {
        localFrame = 0
      } else {
        // loop=false면 마지막 프레임에서 멈추고 finished emit
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
  // 픽셀 아트는 스무딩 끄기
  ctx.imageSmoothingEnabled = false

  ctx.clearRect(0, 0, canvas.width, canvas.height)

  // ✅ "클립" 기준 실제 프레임 인덱스
  const absoluteFrame = props.start + localFrame

  // 한 줄(cols) 기준으로 col 계산
  const col = absoluteFrame % props.cols

  const sx = col * props.frameWidth
  const sy = props.row * props.frameHeight

  const dw = props.frameWidth * props.scale
  const dh = props.frameHeight * props.scale

  // ✅ 캔버스 중앙 배치 + offset 보정
  const x = (canvas.width - dw) / 2 + props.offsetX
  const y = (canvas.height - dh) / 2 + props.offsetY

  ctx.drawImage(
    img,
    sx,
    sy,
    props.frameWidth,
    props.frameHeight,
    x,
    y,
    dw,
    dh
  )
}

onMounted(() => {
  const canvas = canvasRef.value

  // ✅ 캔버스 크기는 "한 프레임 크기"에 맞추는 게 일반적
  canvas.width = props.frameWidth * props.scale
  canvas.height = props.frameHeight * props.scale

  img = new Image()
  img.onload = () => reset()
  img.src = props.src
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
  ],
  () => {
    const canvas = canvasRef.value
    if (!canvas) return

    // scale이나 frame size가 바뀌면 캔버스 사이즈도 갱신
    canvas.width = props.frameWidth * props.scale
    canvas.height = props.frameHeight * props.scale

    // 이미지 소스가 바뀐 경우: 다시 로딩 후 reset
    if (img && img.src !== props.src) {
      img = new Image()
      img.onload = () => reset()
      img.src = props.src
      return
    }

    reset()
  }
)
</script>
