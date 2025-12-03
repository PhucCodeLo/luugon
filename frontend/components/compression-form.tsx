'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { compressText, compressImage } from '@/lib/api'
import { useCompressionStore } from '@/lib/store'
import { copyToClipboard, formatFileSize, downloadFile } from '@/lib/utils'
import toast from 'react-hot-toast'

export function CompressionForm() {
  const [textInput, setTextInput] = useState('')
  const [fileInput, setFileInput] = useState<File | null>(null)
  const { isLoading, setIsLoading, contentType, setContentType, error, setError, result, setResult } =
    useCompressionStore()

  const handleTypeChange = (type: 'text' | 'image') => {
    setContentType(type)
    setTextInput('')
    setFileInput(null)
    setError(null)
    setResult(null)
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setFileInput(file)
      setError(null)
    }
  }

  const handleCompress = async () => {
    try {
      setError(null)
      setIsLoading(true)

      if (contentType === 'text') {
        if (!textInput.trim()) {
          setError('Vui lòng nhập nội dung')
          return
        }

        const response = await compressText(textInput)
        setResult({
          itemId: response.item_id,
          shortCode: response.short_code,
          shortUrl: response.short_url,
          qrCodeUrl: response.qr_code_url,
          originalSizeKb: response.original_size_kb,
          compressedSizeKb: response.compressed_size_kb,
          compressionRatio: response.compression_ratio,
        })

        toast.success('Nén thành công!')
      } else if (contentType === 'image') {
        if (!fileInput) {
          setError('Vui lòng chọn tệp hình ảnh')
          return
        }

        const response = await compressImage(fileInput)
        setResult({
          itemId: response.item_id,
          shortCode: response.short_code,
          shortUrl: response.short_url,
          qrCodeUrl: response.qr_code_url,
          originalSizeKb: response.original_size_kb,
          compressedSizeKb: response.compressed_size_kb,
          compressionRatio: response.compression_ratio,
        })

        toast.success('Nén hình ảnh thành công!')
      }
    } catch (err: any) {
      const errorMessage = err?.response?.data?.detail || err?.message || 'Có lỗi xảy ra'
      setError(errorMessage)
      toast.error(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  const handleCopyLink = () => {
    if (result?.shortUrl) {
      copyToClipboard(result.shortUrl).then(() => {
        toast.success('Đã sao chép liên kết!')
      })
    }
  }

  const handleDownloadQR = async () => {
    if (result?.qrCodeUrl) {
      try {
        const response = await fetch(result.qrCodeUrl)
        const blob = await response.blob()
        downloadFile(blob, `qr-${result.shortCode}.png`)
        toast.success('Đã tải xuống mã QR!')
      } catch (err) {
        toast.error('Không thể tải xuống mã QR')
      }
    }
  }

  if (result) {
    return (
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Kết quả</CardTitle>
          <CardDescription>Liên kết và mã QR của bạn</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label>Liên kết rút gọn:</Label>
            <div className="flex gap-2">
              <Input value={result.shortUrl} readOnly className="flex-1" />
              <Button onClick={handleCopyLink} className="px-4">
                Sao chép
              </Button>
            </div>
          </div>

          <div className="space-y-2">
            <Label>Mã QR:</Label>
            <img src={result.qrCodeUrl} alt="QR Code" className="w-48 h-48 bg-white p-2 rounded" />
            <Button onClick={handleDownloadQR} className="w-full">
              Tải xuống QR
            </Button>
          </div>

          <div className="grid grid-cols-2 gap-2 pt-4 border-t">
            <div>
              <p className="text-xs text-muted-foreground">Kích thước gốc</p>
              <p className="font-semibold">{formatFileSize(result.originalSizeKb * 1024)}</p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground">Kích thước nén</p>
              <p className="font-semibold">{formatFileSize(result.compressedSizeKb * 1024)}</p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground">Tỉ lệ nén</p>
              <p className="font-semibold">{(result.compressionRatio * 100).toFixed(1)}%</p>
            </div>
          </div>

          <Button
            onClick={() => {
              setResult(null)
              setTextInput('')
              setFileInput(null)
              setContentType(null)
            }}
            className="w-full"
          >
            Nén tiếp
          </Button>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>LưuGọn</CardTitle>
        <CardDescription>Chia sẻ nhanh chóng, an toàn</CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {!contentType ? (
          <div className="space-y-3">
            <p className="text-sm text-muted-foreground">Chọn loại nội dung:</p>
            <div className="grid grid-cols-2 gap-3">
              <Button
                onClick={() => handleTypeChange('text')}
                variant="outline"
                className="h-24 flex-col text-base"
              >
                📝 Văn bản
              </Button>
              <Button
                onClick={() => handleTypeChange('image')}
                variant="outline"
                className="h-24 flex-col text-base"
              >
                🖼️ Hình ảnh
              </Button>
            </div>
          </div>
        ) : (
          <>
            <Button onClick={() => handleTypeChange(null)} variant="ghost" className="w-full justify-start">
              ← Quay lại
            </Button>

            {contentType === 'text' && (
              <div className="space-y-2">
                <Label htmlFor="text-input">Nhập văn bản:</Label>
                <Textarea
                  id="text-input"
                  placeholder="Nhập nội dung để nén..."
                  value={textInput}
                  onChange={(e) => setTextInput(e.target.value)}
                  disabled={isLoading}
                  rows={6}
                />
              </div>
            )}

            {contentType === 'image' && (
              <div className="space-y-2">
                <Label htmlFor="file-input">Chọn hình ảnh:</Label>
                <Input
                  id="file-input"
                  type="file"
                  accept="image/jpeg,image/png,image/webp,image/gif"
                  onChange={handleFileChange}
                  disabled={isLoading}
                />
                {fileInput && (
                  <p className="text-sm text-muted-foreground">
                    {fileInput.name} ({formatFileSize(fileInput.size)})
                  </p>
                )}
              </div>
            )}

            {error && <div className="p-3 bg-destructive/20 text-destructive rounded text-sm">{error}</div>}

            <Button onClick={handleCompress} disabled={isLoading} className="w-full">
              {isLoading ? 'Đang xử lý...' : 'Nén & Tạo Link'}
            </Button>
          </>
        )}
      </CardContent>
    </Card>
  )
}
