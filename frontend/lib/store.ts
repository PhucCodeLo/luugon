import { create } from 'zustand'

interface CompressionStore {
  isLoading: boolean
  setIsLoading: (loading: boolean) => void
  error: string | null
  setError: (error: string | null) => void
  contentType: 'text' | 'image' | null
  setContentType: (type: 'text' | 'image' | null) => void
  result: {
    itemId: string
    shortCode: string
    shortUrl: string
    qrCodeUrl: string
    originalSizeKb: number
    compressedSizeKb: number
    compressionRatio: number
  } | null
  setResult: (
    result: {
      itemId: string
      shortCode: string
      shortUrl: string
      qrCodeUrl: string
      originalSizeKb: number
      compressedSizeKb: number
      compressionRatio: number
    } | null
  ) => void
}

export const useCompressionStore = create<CompressionStore>((set) => ({
  isLoading: false,
  setIsLoading: (loading) => set({ isLoading: loading }),
  error: null,
  setError: (error) => set({ error }),
  contentType: null,
  setContentType: (type) => set({ contentType: type }),
  result: null,
  setResult: (result) => set({ result }),
}))
