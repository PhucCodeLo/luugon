import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Toaster } from 'react-hot-toast'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'LưuGọn - Chia sẻ nhanh chóng',
  description: 'Nén và chia sẻ văn bản hoặc hình ảnh thành liên kết rút gọn hoặc mã QR',
  keywords: 'LưuGọn, chia sẻ, nén, QR code, link shortener',
  viewport: 'width=device-width, initial-scale=1.0, maximum-scale=5.0',
  robots: 'index, follow',
  openGraph: {
    title: 'LưuGọn - Chia sẻ nhanh chóng',
    description: 'Nén và chia sẻ văn bản hoặc hình ảnh thành liên kết rút gọn hoặc mã QR',
    type: 'website',
    url: 'https://luugon.com',
    siteName: 'LưuGọn',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="vi" className="dark">
      <body className={inter.className}>
        {children}
        <Toaster
          position="top-right"
          reverseOrder={false}
          toastOptions={{
            style: {
              background: '#1a1a1a',
              color: '#fff',
              borderRadius: '8px',
              border: '1px solid #333',
            },
          }}
        />
      </body>
    </html>
  )
}
