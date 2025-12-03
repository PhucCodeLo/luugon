'use client'

import { CompressionForm } from '@/components/compression-form'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-background to-background/80 flex items-center justify-center p-4">
      <div className="w-full max-w-4xl">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-2 bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            LưuGọn
          </h1>
          <p className="text-lg text-muted-foreground">Chia sẻ nhanh chóng, an toàn, ẩn danh</p>
        </div>

        <div className="flex justify-center">
          <CompressionForm />
        </div>

        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
          <div>
            <div className="text-3xl mb-2">🔒</div>
            <h3 className="font-semibold mb-2">Ẩn danh</h3>
            <p className="text-sm text-muted-foreground">Không cần đăng nhập hoặc tạo tài khoản</p>
          </div>
          <div>
            <div className="text-3xl mb-2">⚡</div>
            <h3 className="font-semibold mb-2">Nhanh chóng</h3>
            <p className="text-sm text-muted-foreground">Nén và chia sẻ chỉ trong vài giây</p>
          </div>
          <div>
            <div className="text-3xl mb-2">📱</div>
            <h3 className="font-semibold mb-2">Mã QR</h3>
            <p className="text-sm text-muted-foreground">Tạo mã QR để chia sẻ dễ dàng</p>
          </div>
        </div>
      </div>
    </main>
  )
}
