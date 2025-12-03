'use client'

import { useEffect, useState } from 'react'
import { getItem } from '@/lib/api'
import { sanitizeHtml } from '@/lib/utils'
import { NotFound } from '@/components/not-found'
import Link from 'next/link'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

export default function ItemPage({ params }: { params: { shortCode: string } }) {
  const [content, setContent] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  useEffect(() => {
    const fetchItem = async () => {
      try {
        const item = await getItem(params.shortCode)
        if (item.type === 'text' && item.content) {
          setContent(sanitizeHtml(item.content))
        } else if (item.type === 'image' && item.file_path) {
          window.location.href = item.file_path
        } else {
          setError(true)
        }
      } catch (err) {
        setError(true)
      } finally {
        setLoading(false)
      }
    }

    fetchItem()
  }, [params.shortCode])

  if (loading) {
    return (
      <main className="min-h-screen flex items-center justify-center p-4">
        <div className="text-center">
          <div className="animate-spin w-8 h-8 border-4 border-primary border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-muted-foreground">Đang tải...</p>
        </div>
      </main>
    )
  }

  if (error) {
    return (
      <main className="min-h-screen flex items-center justify-center p-4">
        <NotFound />
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-background to-background/80 flex items-center justify-center p-4">
      <Card className="w-full max-w-2xl">
        <CardHeader>
          <CardTitle>Nội dung được chia sẻ</CardTitle>
          <CardDescription>Dưới đây là nội dung từ liên kết LưuGọn</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="bg-card/50 p-6 rounded-lg border border-border max-h-96 overflow-auto">
            <p className="whitespace-pre-wrap break-words text-foreground">{content}</p>
          </div>

          <div className="flex gap-2 pt-4">
            <Link href="/" className="flex-1">
              <Button className="w-full">Nén tiếp</Button>
            </Link>
          </div>
        </CardContent>
      </Card>
    </main>
  )
}
