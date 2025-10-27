# npm Registration Guide

## 🎯 Quick Answer

**ต้องสมัคร:** npm account (ฟรี!)
**ราคา:** ฟรี 100% สำหรับ public packages
**เวลา:** 5 นาที

---

## 📝 Step-by-Step Registration

### 1. สมัคร npm Account

**เข้าไปที่:** https://www.npmjs.com/signup

**กรอกข้อมูล:**
```
Username: yourname           # ชื่อที่จะแสดงบน npm
Email: your@email.com        # Email สำหรับ verify
Password: ****************   # รหัสผ่าน (min 8 ตัวอักษร)
```

**คลิก:** "Sign Up"

### 2. Verify Email Address

1. เช็ค email inbox
2. หา email จาก "npm <support@npmjs.com>"
3. หัวข้อ: "Verify your npm account"
4. คลิก "Verify Email Address" button
5. เห็นหน้า "Email verified successfully" ✅

### 3. Login ผ่าน Terminal

เปิด terminal แล้วพิมพ์:

```bash
npm login
```

**จะถามข้อมูล:**
```
Username: yourname
Password: ********
Email: your@email.com
```

**ผลลัพธ์:**
```
Logged in as yourname on https://registry.npmjs.org/
```

### 4. ตรวจสอบว่า Login สำเร็จ

```bash
npm whoami
```

**ควรแสดง:**
```
yourname
```

✅ **สำเร็จ!** คุณพร้อม publish package แล้ว

---

## 💰 ค่าใช้จ่าย

### Free Account (Public Packages)

✅ **ฟรีตลอดไป**
- Unlimited public packages
- Unlimited downloads
- npm publish (ไม่จำกัด)
- 2FA security
- npm search listing
- Package statistics

### Pro Account ($7/month)

ถ้าต้องการ:
- Private packages (แพคเกจส่วนตัว)
- Team collaboration
- Advanced security features

**สรุป:** ทำ public package อย่าง `create-claude-agent` → **ใช้ Free account ก็พอ** ✅

---

## 🔐 เปิด 2-Factor Authentication (แนะนำ)

เพิ่มความปลอดภัยให้บัญชี npm:

### ขั้นตอนเปิด 2FA:

1. **ไปที่:** https://www.npmjs.com/settings/yourname/tfa

2. **เลือกโหมด:**
   - **Authorization Only** (แนะนำ): ถามรหัสตอน login
   - **Authorization and Publishing**: ถามรหัสตอน login + publish

3. **Scan QR Code:**
   - ใช้ authenticator app (Google Authenticator, Authy, 1Password)
   - Scan QR code ที่แสดงบนหน้าจอ

4. **ใส่รหัส 6 หลัก:**
   - ดูรหัสจาก authenticator app
   - กรอกเพื่อ verify

5. **เก็บ Recovery Codes:**
   - npm จะให้ recovery codes (เก็บไว้ในที่ปลอดภัย)
   - ใช้ตอนที่เข้าไม่ได้หรือหาย authenticator app

### Publish ด้วย 2FA เปิดอยู่:

```bash
# ดูรหัส 6 หลักจาก authenticator app ก่อน
npm publish --otp=123456
```

หรือ npm จะถามเอง:
```bash
npm publish
# This operation requires a one-time password.
# Enter OTP: 123456
```

---

## 🚀 พร้อม Publish แล้ว

หลังจากสมัครและ login เสร็จ:

```bash
# ไปที่ package directory
cd create-claude-agent

# Publish เลย!
npm publish --access public

# ถ้าเปิด 2FA
npm publish --access public --otp=123456
```

**ผลลัพธ์:**
```
+ create-claude-agent@1.0.0
```

**ตรวจสอบ:**
```bash
# ใน terminal
npm info create-claude-agent

# ใน browser
open https://www.npmjs.com/package/create-claude-agent
```

**ใช้งานได้เลย:**
```bash
npx create-claude-agent
```

---

## ❓ FAQ

### Q: ต้องจ่ายเงินไหม?
**A:** ไม่ต้อง! Public packages ฟรีตลอดไป

### Q: ต้องมีบัตรเครดิตไหม?
**A:** ไม่ต้อง (เว้นแต่จะซื้อ Pro account)

### Q: Package name ต้องไม่ซ้ำใครใช่ไหม?
**A:** ใช่! ถ้าซ้ำให้ใช้ scoped package `@yourname/package-name`

### Q: ลบ package ได้ไหม?
**A:** ได้ ภายใน 72 ชั่วโมงหลัง publish:
```bash
npm unpublish create-claude-agent --force
```
หลัง 72 ชั่วโมง: ต้องติดต่อ npm support

### Q: Update package ทำยังไง?
**A:** เปลี่ยน version แล้ว publish ใหม่:
```bash
npm version patch  # 1.0.0 -> 1.0.1
npm publish
```

### Q: ถ้าลืมรหัสผ่าน?
**A:** Reset ที่: https://www.npmjs.com/forgot

### Q: ถ้าหาย authenticator app?
**A:** ใช้ recovery codes ที่เก็บไว้

### Q: npm login แล้ว session หมดอายุไหม?
**A:** ไม่หมดอายุ เว้นแต่คุณ `npm logout`

---

## 🎉 สรุป

**ขั้นตอนทั้งหมด (5 นาที):**

1. ✅ สมัคร: https://www.npmjs.com/signup
2. ✅ Verify email
3. ✅ `npm login` ใน terminal
4. ✅ `npm whoami` → ตรวจสอบ
5. ✅ `npm publish --access public`
6. ✅ Done!

**ฟรี 100%** สำหรับ public packages 🎉

**Next:** ดู PUBLISH-GUIDE.md สำหรับขั้นตอน publish แบบละเอียด
