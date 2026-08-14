# Memoria y Registro del Proyecto Jeshia

Este archivo registra las decisiones clave, requerimientos, preferencias y estado del proyecto acordados en nuestras conversaciones.

## 📌 Contexto General
- **Proyecto:** Jeshia (Branding, etiquetas, montajes de producto y presentación web).
- **Repositorio local:** `e:\Logo Jeshia`
- **Repositorio GitHub:** `https://github.com/SebastianCortesIbacache/Jeshia-.git`
- **URL pública (GitHub Pages):** `https://sebastiancortesibacache.github.io/Jeshia-/` *(activar en Settings → Pages)*

---

## 🗂️ Arquitectura de Archivos Web (Oficial)

```
e:\Logo Jeshia\
├── index.html           ← Portal e-commerce oficial (782 líneas)
├── css\
│   └── main.css         ← Sistema de diseño maestro (~2350 líneas)
├── js\
│   ├── products.js      ← Base de datos de fragancias y productos (552 líneas)
│   └── main.js          ← Motor interactivo (1031 líneas)
├── assets\
│   ├── logos\           ← Logos transparentes (Jeshia Colores_Transparent.png, Logo V3_Transparent.png)
│   ├── aromas_botanicos\← 13 ilustraciones botánicas en PNG transparente
│   └── visuales\        ← Familia.png, visuales de producto
├── visuales\            ← Imágenes principales de producto (Home Spray, Mikado, Aromatizador, Recargas)
└── .nojekyll            ← Para compatibilidad con GitHub Pages
```

---

## 💰 Precios Oficiales Confirmados (CLP)

| Producto | Precio | ID |
|----------|--------|----|
| Home Spray Textil & Ambiental 250ml | **$12.990** | `home-spray-250` |
| Difusor de Varillas Mikado 50ml | **$13.990** | `mikado-50` |
| Aromatizador Compacto & Auto 15ml | **$5.490** | `aromatizador-15` |
| Recarga Eco-Refill 250ml | **$7.490** | `recarga-250` |
| Recarga Familiar Maxi-Refill 500ml | **$11.990** | `recarga-500` |

---

## 📡 Contacto & Canal de Ventas
- **WhatsApp:** Placeholder actual `+56912345678` → **pendiente reemplazar con número real de Jeshia**
- **Canal de venta:** 100% WhatsApp. El carrito genera un mensaje formateado automáticamente.

---

## 📝 Registro de Conversaciones y Decisiones

### [2026-08-03]
- **Inicio de guardado en memoria:** Se activa el registro continuo de requerimientos y notas clave del proyecto.
- **Logos con Fondo Transparente:**
  - El logo en colores (`Jeshia Colores.webp`) cuenta con fondo 100% transparente.
  - Versiones PNG: `assets/logos/Jeshia Colores_Transparent.png` (2520x2520 px) y `assets/logos/Logo V3_Transparent.png`.
- **Pieza Gráfica Publicitaria Home Spray:**
  - Formato Feed Retrato 4:5 (1080x1350 px) en [`visuales/home_spray_mkt_1.png`].
  - Estructura 2 columnas: izquierda editorial con precio $12.990, derecha foto producto Mokka.

### [2026-08-13] — Desarrollo Web Completo
- **Limpieza total:** Eliminadas carpetas `propuesta-a/`, `propuesta-b/`, `propuesta-c/` y `web/`.
- **Nueva web oficial construida desde cero** con estética *Botanical Luxury*:
  - Paleta: alabastro `#FBF8F3`, terracota `#C47A47`, verde bosque `#2A4031`, obsidiano `#0C0F0C`
  - Tipografías: `Playfair Display` (serif editorial) + `Plus Jakarta Sans` (UI)
- **7 módulos interactivos implementados (aprobados por el usuario):**
  1. 🌙 **Dark Mode Obsidian** — Toggle persistente en `localStorage` con variable `jeshia_theme`
  2. 🎁 **Gift Box Builder (Mix & Match)** — 3 formatos (Dúo 15% OFF, Trío 20% OFF, Solo), 2 selectores de aroma + addon, resumen con precio en tiempo real
  3. 🧠 **Neuro-Aromaterapia Mood Wheel** — 4 moods (Dormir, Foco, Calidez, Alegría) con fragancias recomendadas y rituales
  4. 🏠 **Simulador de Ambientes & Cobertura** — 5 espacios (Living, Dormitorio, Oficina, Cocina, Auto) con m², formato y tips
  5. 🏢 **B2B & Mayoristas Calculator** — Slider 20-200 uds, tiers 15%/25%/35%, cotización WhatsApp automática
  6. ♻️ **Eco-Refill Savings Calculator** — Slider de consumo mensual, ahorro anual en CLP y envases divertidos
  7. 🎀 **Gift Dedication Card Designer** — Panel en el carrito con preview en vivo de tarjeta botánica y campos Para/De/Mensaje

### [2026-08-14] — Optimización Técnica, Mobile y Despliegue
- **12 bugs técnicos corregidos:**
  - Grids sin colapsar en mobile: `builder-wrap`, `b2b-grid`, `room-detail-card`, `modal-grid`, `philo-features`, `mood-frag-cards`
  - `floating-pill` causaba overflow horizontal → ocultas en ≤992px
  - Top bar desbordaba en 768px → separadores ocultos
  - Precio hardcodeado `$12.000` en modal de fragancias → reemplazado por valor dinámico desde `PRODUCTS`
  - Menú mobile no respetaba dark mode → añadidos `z-index: 999` + `border-bottom`
  - Cart footer ocultaba botón WhatsApp en móvil → `max-height: 60vh` + scroll
- **Optimización mobile completa — 3 breakpoints:**
  - `992px` (Tablet): todos los grids a 1 columna, nav colapsado, pills ocultas
  - `768px` (Mobile): hero-buttons en columna, top bar simplificado, tabs y grids ajustados
  - `480px` (Mobile small): **tabs con scroll horizontal suave** (sin overflow), quiz 1 columna, `font-size: 16px` en inputs (evita zoom iOS), secciones con padding mínimo
- **Precios reales actualizados en `js/products.js`** (ver tabla de precios arriba)
- **Despliegue en GitHub:**
  - Commit: `feat: optimizacion mobile completa + precios reales + deploy GitHub Pages`
  - Hash: `ac33f79..3f930d9` en rama `main`
  - `.nojekyll` creado para compatibilidad con GitHub Pages
  - **Push exitoso** a `https://github.com/SebastianCortesIbacache/Jeshia-.git`
  - **Pendiente:** Activar GitHub Pages en Settings → Pages → Branch: `main`, folder: `/`

---

## ✅ Estado Actual del Proyecto Web

| Módulo | Estado |
|--------|--------|
| Hero con imagen Mokka y pills flotantes | ✅ Completo |
| Aroma ticker animado (13 fragancias) | ✅ Completo |
| Catálogo con filtros y selector de aromas | ✅ Completo |
| Biblioteca olfativa (13 aromas, filtros de familia) | ✅ Completo |
| Quiz "Descubre tu Aroma" (3 pasos) | ✅ Completo |
| Carrito drawer + checkout WhatsApp | ✅ Completo |
| Quick View modal (pirámide olfativa) | ✅ Completo |
| Dark Mode Obsidian (persistente) | ✅ Completo |
| Gift Box Builder (Mix & Match) | ✅ Completo |
| Neuro-Aromaterapia Mood Wheel | ✅ Completo |
| Simulador de Ambientes & Cobertura | ✅ Completo |
| B2B & Mayoristas Calculator | ✅ Completo |
| Eco-Refill Savings Calculator | ✅ Completo |
| Gift Dedication Card en Carrito | ✅ Completo |
| Sección Filosofía y Sustentabilidad | ✅ Completo |
| Reseñas de clientes (social proof) | ✅ Completo |
| Optimización mobile (992/768/480px) | ✅ Completo |
| Precios reales en CLP | ✅ Completo |
| Push a GitHub (`main`) | ✅ Completo |
| GitHub Pages activo | ⏳ Pendiente (2 clics en Settings) |
| WhatsApp número real | ⏳ Pendiente (reemplazar placeholder) |

---

## 🔑 Decisiones de Diseño Fijadas
1. **Sin frameworks CSS externos** — Solo Vanilla CSS con variables `--var()`
2. **Checkout 100% WhatsApp** — No hay pasarela de pago, todo va por WhatsApp formateado
3. **Carrito en localStorage** bajo clave `jeshia_cart`, tema en `jeshia_theme`
4. **13 fragancias** con IDs fijos: `vainilla-coco`, `citric`, `berries`, `mokka`, `lavanda`, `pino`, `limon`, `manzana-canela`, `sugar`, `coco-nut`, `coco-flower`, `frutal-mango`, `chicle`
5. **5 líneas de producto** con sus visuales en `visuales/` referenciados por path relativo
6. **Descuentos del Box Builder:** Dúo 15% OFF, Trío 20% OFF, Solo = precio normal

---
*Nota: Este documento se actualiza automáticamente en cada sesión de desarrollo.*
