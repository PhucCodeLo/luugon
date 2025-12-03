import { z } from 'zod'

const MAX_TEXT_LENGTH = 1000000 // 1MB
const MAX_FILE_SIZE = 10 * 1024 * 1024 // 10MB
const ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
const ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp', '.gif']

export const compressTextSchema = z.object({
  content: z
    .string()
    .min(1, 'Vui lòng nhập nội dung')
    .max(MAX_TEXT_LENGTH, `Nội dung không được vượt quá ${MAX_TEXT_LENGTH / 1024}KB`),
})

export const compressImageSchema = z.object({
  file: z
    .instanceof(File)
    .refine(
      (file) => file.size > 0,
      'Vui lòng chọn tệp'
    )
    .refine(
      (file) => file.size <= MAX_FILE_SIZE,
      `Kích thước tệp không được vượt quá ${MAX_FILE_SIZE / (1024 * 1024)}MB`
    )
    .refine(
      (file) => ALLOWED_IMAGE_TYPES.includes(file.type),
      'Chỉ hỗ trợ các định dạng ảnh: JPEG, PNG, WebP, GIF'
    ),
})

export type CompressTextInput = z.infer<typeof compressTextSchema>
export type CompressImageInput = z.infer<typeof compressImageSchema>
