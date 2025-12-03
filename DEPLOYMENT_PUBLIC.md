# 🚀 LưuGọn - Deployment Guide (Public)

## 📌 Các Bước Deploy

### **1. Frontend (Vercel) - 5 phút**

1. Vào https://vercel.com và đăng nhập bằng GitHub
2. Nhấp "Add New..." → "Project"
3. Chọn repository `luugon`
4. Cấu hình:
   - Framework: Next.js
   - Root Directory: `frontend`
   - Environment Variables:
     ```
     NEXT_PUBLIC_API_URL=https://api.yourdomain.com
     ```
5. Nhấp "Deploy"
6. Vercel sẽ tự động deploy mỗi khi bạn push code

**Kết quả:** 
- URL: `https://luugon.vercel.app` (tạm thời)
- Custom domain: Thêm domain tại Vercel Settings

---

### **2. Backend (Railway) - 5 phút**

1. Vào https://railway.app và đăng nhập bằng GitHub
2. Nhấp "New Project" → "Deploy from GitHub repo"
3. Chọn repository `luugon`
4. Cấu hình:
   - Root Directory: `backend`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Environment Variables:
   ```
   SUPABASE_URL=your_url
   SUPABASE_KEY=your_key
   BASE_URL=https://yourdomain.com
   CORS_ORIGINS=https://yourdomain.com
   DEBUG=False
   ```
6. Railway tự động deploy

**Kết quả:**
- URL: `https://railway-app-name.up.railway.app`
- Custom domain: Thêm tại Railway Settings

---

### **3. Domain (Namecheap) - 10 phút**

1. Mua domain tại https://namecheap.com (~$10-15/năm)
2. DNS Settings:
   ```
   yourdomain.com  → A record → Vercel IP
   api.yourdomain.com → CNAME → railway-app.up.railway.app
   ```
3. Hoặc dễ hơn: Vercel & Railway có hỗ trợ custom domain tích hợp

---

### **4. Database (Supabase) - Đã Có**

Bạn đã setup Supabase, chỉ cần:
1. Chạy SQL từ `backend/init_db.sql`
2. Tạo storage buckets: `luugon-files`
3. Bật RLS policies

---

## 🔒 Security Checklist

- [ ] Debug mode = False
- [ ] CORS chỉ cho domain bạn
- [ ] Rate limiting bật
- [ ] HTTPS/SSL (Vercel & Railway tự động)
- [ ] Environment variables không commit
- [ ] Database backups enabled
- [ ] Password/secrets trong .env, không hardcode

---

## 📊 Estimated Costs/Month

| Service | Cost | Notes |
|---------|------|-------|
| Vercel | $0 | Free tier OK |
| Railway | $5 | Includes $5 credits/month |
| Supabase | $0 | Free tier OK (auth optional) |
| Domain | $1 | ~$15/year |
| **Total** | **~$6** | Rất rẻ! |

---

## 🆘 Troubleshooting

### Frontend không kết nối Backend
- Kiểm tra `NEXT_PUBLIC_API_URL` ở Vercel environment
- Kiểm tra CORS settings ở backend config
- Backend phải bật CORS cho domain frontend

### 503 Bad Gateway
- Backend đang starting, chờ 1-2 phút
- Kiểm tra Railway logs

### Images không hiển thị
- Kiểm tra Supabase storage bucket public access
- Kiểm tra file permissions

---

## 📚 Tài Liệu Thêm

- Vercel Docs: https://vercel.com/docs
- Railway Docs: https://docs.railway.app
- Supabase Docs: https://supabase.com/docs

Chúc may mắn! 🎉
