# 🎯 Quick Start Guide - Public Launch

Hướng dẫn nhanh để public dự án LưuGọn cho mọi người dùng.

## 📋 TL;DR (Tóm tắt 2 phút)

```
1. Mua domain ($10-15/năm)
2. Deploy frontend → Vercel (miễn phí)
3. Deploy backend → Railway ($5/tháng)
4. Setup DNS records (domain → Vercel, api.domain → Railway)
5. Done! ✅
```

**Tổng chi phí:** ~$5-6/tháng (Railway) + domain

---

## 🚀 3 Lựa Chọn Deploy

### **Option 1: Dễ Nhất (Recommended) ⭐**

| Phần | Nơi Deploy | Chi Phí | Thời Gian |
|------|-----------|--------|----------|
| Frontend | Vercel | Miễn phí | 5 phút |
| Backend | Railway | $5/tháng | 5 phút |
| Database | Supabase | Miễn phí | Có rồi |
| Domain | Namecheap | ~$15/năm | 10 phút |
| **Total** | | **~$5/tháng** | **20 phút** |

**Lợi ích:**
- ✅ Cực dễ setup
- ✅ Rẻ
- ✅ Auto scale
- ✅ CI/CD tự động

---

### **Option 2: Full Control (VPS)**

Mua VPS (DigitalOcean $6-12/tháng) và chạy Docker:

```bash
docker-compose up -d
```

**Lợi ích:**
- ✅ Kiểm soát hoàn toàn
- ✅ Có thể tùy chỉnh
- ❌ Phải tự manage

---

### **Option 3: Free (Render.com + Vercel)**

```
Frontend: Vercel (free)
Backend: Render.com (free tier, nhưng slow)
Database: Supabase (free)
Domain: Free subdomain hoặc mua
```

**Lợi ích:**
- ✅ Hoàn toàn miễn phí
- ❌ Backend có thể slow

---

## 🎯 Deploy Step-by-Step (Option 1)

### **Bước 1: Chuẩn Bị**

1. Tạo GitHub account (nếu chưa có)
2. Push code lên GitHub:
```powershell
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/luugon.git
git branch -M main
git push -u origin main
```

### **Bước 2: Deploy Frontend (5 phút)**

1. Vào https://vercel.com
2. Đăng nhập bằng GitHub
3. Nhấp "Add New" → "Project"
4. Chọn repository `luugon`
5. Settings:
   - **Framework Preset:** Next.js
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
6. **Environment Variables:**
   ```
   NEXT_PUBLIC_API_URL=https://api.yourdomain.com
   ```
7. Nhấp "Deploy"
8. Chờ 2-3 phút
9. Frontend ready tại `https://luugon.vercel.app`

### **Bước 3: Deploy Backend (5 phút)**

1. Vào https://railway.app
2. Đăng nhập bằng GitHub
3. Nhấp "Create New" → "GitHub Repo"
4. Chọn repository `luugon`
5. Settings:
   - **Root Directory:** `backend`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. **Environment Variables:**
   ```
   SUPABASE_URL=https://xxx.supabase.co
   SUPABASE_KEY=eyxx...
   BASE_URL=https://yourdomain.com
   CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
   DEBUG=False
   ```
7. Deploy tự động
8. Backend ready tại `https://railway-app.up.railway.app`

### **Bước 4: Setup Domain (10 phút)**

1. Mua domain: https://namecheap.com (~$15/năm)
   - VD: `luugon.com`

2. Cấu hình DNS:
   - **yourdomain.com** → Vercel IP (lấy từ Vercel > Settings > Domains)
   - **api.yourdomain.com** → Railway domain
   
   Hoặc dễ hơn:
   - Trong Vercel Settings: Thêm custom domain
   - Trong Railway: Thêm custom domain
   - Nó sẽ tự hướng dẫn

3. Chờ DNS propagate (có thể mất 24 giờ)

### **Bước 5: Test**

1. Vào https://yourdomain.com
2. Test compress text
3. Test compress image
4. Test QR code
5. Thành công! 🎉

---

## 🔐 Security Check

Trước khi public:

```bash
# Backend config.py
[ ] DEBUG = False
[ ] CORS_ORIGINS = specific domain (không dùng *)
[ ] rate_limit_requests = 50
[ ] base_url = domain thật (không localhost)

# Supabase
[ ] Storage bucket = public readable
[ ] RLS policies = configured

# .env files
[ ] .env files IN .gitignore
[ ] Không commit secrets lên GitHub
[ ] Environment variables SET tại Vercel & Railway
```

---

## 📊 Chi Phí Thực Tế

```
Vercel:        $0    (free tier sufficient)
Railway:       $5    (includes $5 free credits/month)
Supabase:      $0    (free tier sufficient)
Domain:        $1-2  (~$15/year = $1.25/month)
================
Total:         ~$6-7 per month
```

Cheap! 💰

---

## 🆘 Troubleshooting

### Frontend không load
- Kiểm tra Vercel deploy logs
- Refresh cache (Cmd+Shift+R)

### "Cannot reach backend"
- Kiểm tra Railway deploy status
- Kiểm tra NEXT_PUBLIC_API_URL
- Kiểm tra CORS settings

### "Bad gateway" từ backend
- Backend còn starting, chờ 1-2 phút
- Kiểm tra Railway logs
- Kiểm tra environment variables

### Images không hiển thị
- Supabase storage bucket phải public
- Kiểm tra file permissions

---

## 📚 Tài Liệu Chi Tiết

- 📖 **DEPLOYMENT_PUBLIC.md** - Hướng dẫn chi tiết
- 📋 **PRE_LAUNCH_CHECKLIST.md** - Checklist trước launch
- 📋 **PRIVACY_TERMS.md** - Privacy & Terms templates
- 🔧 **deploy-setup.sh** / **deploy-setup.ps1** - Automation scripts

---

## ✅ Final Checklist

- [ ] Code pushed to GitHub
- [ ] Vercel project created & deployed
- [ ] Railway project created & deployed
- [ ] Domain registered & DNS configured
- [ ] Environment variables set
- [ ] Tested all features
- [ ] Privacy policy & terms available
- [ ] Monitoring setup (optional but recommended)
- [ ] Shared with friends! 🎉

---

## 🎉 Bạn Sẵn Sàng!

Dự án của bạn đã sẵn sàng để public. Nó hoàn chỉnh, bảo mật, và sạch.

**Next steps:**
1. Chọn Option 1 (recommended)
2. Follow steps 1-5
3. Test thoroughly
4. Share URL với mọi người!

Chúc may mắn! 🚀

---

**Cần giúp?** Mở GitHub Issues hoặc liên hệ support.
