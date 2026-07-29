<template>
  <BaseModal v-if="dialog.isOpen" @close="dialog.close(false)">
    <div class="text-black space-y-3">
      <h2 v-if="dialog.title" class="text-lg font-bold">
        {{ dialog.title }}
      </h2>

      <p class="text-sm whitespace-pre-wrap leading-relaxed">
        {{ dialog.message }}
      </p>

      <div class="flex justify-end gap-2 pt-2">
        <button
          v-if="dialog.mode === 'confirm'"
          class="p-1 button-red"
          @click="dialog.close(false)"
        >
          취소
        </button>

        <button
          class="p-1"
          :class="dialog.tone === 'danger' ? 'button-red' : 'button-green'"
          @click="dialog.close(true)"
        >
          {{ dialog.confirmText }}
        </button>
      </div>
    </div>
  </BaseModal>
</template>

<script setup>
import BaseModal from "@/components/common/BaseModal.vue"
import { useDialogStore } from "@/stores/dialog"

const dialog = useDialogStore()
</script>
