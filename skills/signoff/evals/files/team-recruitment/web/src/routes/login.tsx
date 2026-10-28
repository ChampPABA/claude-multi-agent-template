// /login, approved. Auth and the older advisor sales pages are Thai; admin and team pages are English.
export function LoginPage() {
  return (
    <AuthCard title="เข้าสู่ระบบ">
      <TextField label="อีเมล" name="email" />
      <TextField label="รหัสผ่าน" name="password" type="password" />
      <Button type="submit">เข้าสู่ระบบ</Button>
    </AuthCard>
  )
}
