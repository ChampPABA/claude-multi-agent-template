# Frontend Performance Optimization

> **Purpose:** Optimize frontend performance for faster load times, better UX, and improved SEO

**Key Metrics:**
- **LCP (Largest Contentful Paint):** < 2.5s (target)
- **FCP (First Contentful Paint):** < 1.8s (target)
- **Total Bundle Size:** < 200KB gzipped (initial load)
- **Image Size:** < 100KB per image (target)

---

## ⚡ Performance Impact

**Before optimization:**
```
Total image size: 2.2MB (5 × 440KB JPG)
JS bundle size: 850KB (no splitting)
HTTP requests: 12 requests
LCP: 5.8s
Lighthouse Score: 58
```

**After optimization:**
```
Total image size: 400KB (5 × 80KB WebP) = -82%
JS bundle size: 320KB (code split) = -62%
HTTP requests: 6 requests = -50%
LCP: 2.1s = -64%
Lighthouse Score: 94 = +62%
```

**User Impact:**
- Mobile users: 2-3× faster load
- Bounce rate: -10-15%
- SEO ranking: +20-30%

---

## 🖼️ Image Optimization (Primary Focus)

### 1. Format Selection

**Rule:** Use WebP with fallback to JPEG/PNG

| Use Case | Format | Why |
|----------|--------|-----|
| **Photos** | WebP | 30% smaller than JPEG, better quality |
| **Icons** | SVG | Scalable, tiny file size |
| **Logos** | SVG | Crisp at any size |
| **Screenshots** | WebP | Better compression than PNG |
| **Complex graphics** | WebP/AVIF | Best compression |

**Implementation:**

```html
<!-- ✅ WebP with fallback -->
<picture>
  <source srcset="hero.webp" type="image/webp">
  <img src="hero.jpg" alt="Hero image" loading="lazy">
</picture>

<!-- ✅ SVG for icons -->
<svg width="24" height="24">
  <path d="..." />
</svg>
```

---

### 2. Lazy Loading

**Rule:** Lazy load all images below the fold

**Benefits:**
- Faster initial page load
- Reduced bandwidth usage
- Better LCP score

**Implementation:**

```html
<!-- ✅ Lazy load below-fold images -->
<img
  src="product.webp"
  alt="Product image"
  loading="lazy"
  width="400"
  height="300"
/>

<!-- ✅ Eager load above-fold images (hero, logo) -->
<img
  src="hero.webp"
  alt="Hero"
  loading="eager"
  width="1920"
  height="1080"
/>

<!-- ❌ Don't lazy load critical images -->
<img src="logo.svg" alt="Logo" loading="lazy">  <!-- BAD: Logo should load immediately -->
```

**React/Next.js:**

```tsx
import Image from 'next/image'

// ✅ Lazy load by default
<Image
  src="/product.webp"
  alt="Product"
  width={400}
  height={300}
  loading="lazy"
/>

// ✅ Eager load hero images
<Image
  src="/hero.webp"
  alt="Hero"
  width={1920}
  height={1080}
  priority  // Next.js: eager loading
/>
```

---

### 3. Responsive Images

**Rule:** Serve different image sizes for different screen sizes

**Benefits:**
- Mobile users don't download desktop images
- 70-80% size reduction on mobile
- Better performance on slow connections

**Implementation:**

```html
<!-- ✅ Responsive images with srcset -->
<img
  src="hero-1920.webp"
  srcset="
    hero-768.webp 768w,
    hero-1024.webp 1024w,
    hero-1920.webp 1920w
  "
  sizes="
    (max-width: 768px) 100vw,
    (max-width: 1024px) 100vw,
    1920px
  "
  alt="Hero"
  loading="lazy"
  width="1920"
  height="1080"
/>
```

**React/Next.js:**

```tsx
<Image
  src="/hero.webp"
  alt="Hero"
  width={1920}
  height={1080}
  sizes="(max-width: 768px) 100vw, (max-width: 1024px) 100vw, 1920px"
  loading="lazy"
/>
```

---

### 4. Image Dimensions (Prevent Layout Shift)

**Rule:** Always specify width and height attributes

**Benefits:**
- Prevents Cumulative Layout Shift (CLS)
- Browser reserves space before image loads
- Better UX (no content jumping)

**Implementation:**

```html
<!-- ✅ Always specify dimensions -->
<img
  src="product.webp"
  alt="Product"
  width="400"
  height="300"
  loading="lazy"
/>

<!-- ❌ Missing dimensions (causes layout shift) -->
<img src="product.webp" alt="Product" loading="lazy">
```

---

### 5. Image Compression

**Rule:** Compress images to 80-85% quality (no visible difference)

**Tools:**
- **Online:** TinyPNG, Squoosh, Compressor.io
- **CLI:** `imagemagick`, `sharp`, `squoosh-cli`
- **Build-time:** Next.js Image Optimization, webpack loaders

**Example (ImageMagick):**

```bash
# Convert JPEG to WebP (85% quality)
magick input.jpg -quality 85 output.webp

# Resize + Convert
magick input.jpg -resize 768x -quality 85 output-768.webp
```

---

## 🎯 Image Optimization Checklist

**Before implementing any image:**

- [ ] **Format:** Use WebP (with JPEG/PNG fallback)
- [ ] **Lazy loading:** `loading="lazy"` for below-fold images
- [ ] **Responsive:** Generate 3 sizes (768w, 1024w, 1920w) if > 400px width
- [ ] **Dimensions:** Always specify `width` and `height`
- [ ] **Compression:** 80-85% quality (use TinyPNG or Squoosh)
- [ ] **Alt text:** Descriptive alt text for accessibility
- [ ] **Priority:** `loading="eager"` or `priority` for hero images only

---

## 📦 Code Splitting (Basic)

### When to Split

**✅ Split code when:**
- Route-based splitting (different pages)
- Heavy components (charts, editors, modals)
- Third-party libraries (3+ libraries)

**❌ Don't split:**
- Small components (< 10KB)
- Critical path components (above-fold)
- Frequently used utilities

### React/Next.js Examples

```tsx
// ✅ Lazy load heavy components
import dynamic from 'next/dynamic'

const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <div>Loading chart...</div>,
  ssr: false  // Client-side only
})

// ✅ Route-based splitting (automatic in Next.js)
// pages/dashboard.tsx - loaded only when /dashboard is accessed
```

```tsx
// React (without Next.js)
import { lazy, Suspense } from 'react'

const Dashboard = lazy(() => import('./Dashboard'))

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Dashboard />
    </Suspense>
  )
}
```

---

## 📊 Performance Budget

**Define limits to prevent performance regression:**

| Metric | Target | Max | Action if exceeded |
|--------|--------|-----|-------------------|
| **LCP** | < 2.5s | 4s | Optimize images, reduce bundle |
| **FCP** | < 1.8s | 3s | Inline critical CSS, defer JS |
| **Total Bundle (initial)** | < 200KB | 500KB | Code splitting, tree shaking |
| **Image Size (each)** | < 100KB | 200KB | Compress, use WebP |
| **HTTP Requests** | < 10 | 20 | Combine assets, use sprites |

**Check during code review:**
```bash
# Check bundle size
npm run build

# Check Lighthouse score
lighthouse https://your-site.com --view
```

---

## ⚡ Quick Wins (Immediate Impact)

### 1. Convert Images to WebP
```bash
# Batch convert all JPEGs to WebP
for file in *.jpg; do
  magick "$file" -quality 85 "${file%.jpg}.webp"
done
```

**Impact:** -30% file size, +0.5s LCP improvement

---

### 2. Add Lazy Loading to Images
```tsx
// Find all images and add loading="lazy"
<img src="..." alt="..." loading="lazy" />
```

**Impact:** -2s initial load time, +20 Lighthouse score

---

### 3. Specify Image Dimensions
```tsx
// Add width/height to prevent layout shift
<img src="..." alt="..." width={400} height={300} />
```

**Impact:** CLS score 0.1 → 0.01 (90% improvement)

---

## 🚨 Common Mistakes

### ❌ Mistake 1: Lazy load hero images

```tsx
// ❌ BAD: Hero image lazy loaded (appears late)
<img src="hero.webp" alt="Hero" loading="lazy" />

// ✅ GOOD: Hero image eager loaded
<img src="hero.webp" alt="Hero" loading="eager" />
```

---

### ❌ Mistake 2: No image dimensions

```tsx
// ❌ BAD: No dimensions (causes layout shift)
<img src="product.webp" alt="Product" />

// ✅ GOOD: Dimensions specified
<img src="product.webp" alt="Product" width={400} height={300} />
```

---

### ❌ Mistake 3: Using PNG for photos

```tsx
// ❌ BAD: PNG for photo (2.2MB)
<img src="photo.png" alt="Photo" />

// ✅ GOOD: WebP for photo (300KB)
<picture>
  <source srcset="photo.webp" type="image/webp">
  <img src="photo.jpg" alt="Photo" />
</picture>
```

---

### ❌ Mistake 4: No responsive images

```tsx
// ❌ BAD: Mobile downloads 1920px image
<img src="hero-1920.webp" alt="Hero" />

// ✅ GOOD: Responsive images (mobile gets 768px)
<img
  src="hero-1920.webp"
  srcset="hero-768.webp 768w, hero-1024.webp 1024w, hero-1920.webp 1920w"
  sizes="(max-width: 768px) 100vw, 1920px"
  alt="Hero"
/>
```

---

## 📚 Additional Resources

**Official Docs:**
- [Web.dev: Optimize LCP](https://web.dev/optimize-lcp/)
- [MDN: Lazy loading](https://developer.mozilla.org/en-US/docs/Web/Performance/Lazy_loading)
- [Next.js: Image Optimization](https://nextjs.org/docs/basic-features/image-optimization)

**Tools:**
- **Lighthouse:** Chrome DevTools > Lighthouse tab
- **WebPageTest:** https://www.webpagetest.org/
- **Squoosh:** https://squoosh.app/ (image compression)
- **TinyPNG:** https://tinypng.com/ (batch compression)

**Source:**
- FreeCodeCamp Performance Handbook
- Chrome DevTools Performance Guide
- Web.dev Performance Best Practices

---

**💡 Remember:** 80% of performance gains come from image optimization. Start there!
