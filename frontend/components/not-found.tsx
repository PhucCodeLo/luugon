'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import Link from 'next/link'

export function NotFound() {
  return (
    <Card className="w-full max-w-md border-destructive">
      <CardHeader>
        <CardTitle className="text-destructive">404 - Không tìm thấy</CardTitle>
        <CardDescription>Liên kết này không tồn tại hoặc đã hết hạn</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-sm text-muted-foreground">
          Có thể liên kết đã hết hạn, được xóa hoặc không chính xác. Vui lòng kiểm tra và thử lại.
        </p>
        <Link href="/">
          <Button className="w-full">Quay lại trang chủ</Button>
        </Link>
      </CardContent>
    </Card>
  )
}
