import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000,
})

export interface CompressResponse {
  item_id: string
  short_code: string
  short_url: string
  qr_code_url: string
  original_size_kb: number
  compressed_size_kb: number
  compression_ratio: number
}

export async function compressText(content: string): Promise<CompressResponse> {
  const formData = new FormData()
  formData.append('content', content)
  formData.append('type', 'text')

  const response = await apiClient.post<CompressResponse>('/api/compress', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  return response.data
}

export async function compressImage(file: File): Promise<CompressResponse> {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('type', 'image')

  const response = await apiClient.post<CompressResponse>('/api/compress', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  return response.data
}

export async function getItem(shortCode: string): Promise<{ type: string; content?: string; file_path?: string }> {
  const response = await apiClient.get(`/api/item/${shortCode}`)
  return response.data
}

export async function getQRCode(shortCode: string): Promise<Blob> {
  const response = await apiClient.get(`/api/qr/${shortCode}`, {
    responseType: 'blob',
  })

  return response.data
}

export default apiClient
