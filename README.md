# Jeshia — Brand Identity & High-Resolution Label Suite

Este repositorio contiene la identidad visual, la suite completa de **etiquetas para producción impresa (HD/300+ DPI)** y las **propuestas de sitio web e-commerce** para la marca de cosmética y perfumes **Jeshia**.

---

## 🌿 Estructura del Proyecto

```
Logo Jeshia/
├── index.html                   # Sitio web oficial e-commerce interactivo
├── css/
│   └── main.css                 # Sistema de diseño, tokens, responsive y glassmorphism
├── js/
│   ├── products.js              # Base de datos de productos, 13 aromas y pirámides olfativas
│   └── main.js                  # Lógica interactiva, carrito drawer, filtros y WhatsApp checkout
├── README.md                    # Documentación del proyecto
├── MEMORY.md                    # Memoria viva de decisiones y requerimientos
├── assets/                      # Logos e ilustraciones botánicas transparentes
│   ├── logos/                   # Logotipo oficial de Jeshia en alta resolución
│   ├── aromas_botanicos/        # Ilustraciones botánicas transparentes por aroma
│   └── visuales/                # Renders oficiales y montajes de producto
├── visuales/                    # Piezas de marketing y montajes de producto
└── etiquetas_impresion/         # Portal de descarga de etiquetas HD (listas para imprenta)
```

---

## 🏷️ Línea de Aromas Incluidos (13 Fragancias)

1. **Vainilla Coco** (*Vainilla Bourbon & Coco*)
2. **Citric** (*Cítricos Frescos & Bergamota*)
3. **Berries** (*Frutos Rojos & Silvestres*)
4. **Coco Nut** (*Nuez de Coco & Crema*)
5. **Sugar** (*Azúcar Dulce & Caramelo*)
6. **Chicle** (*Bubblegum & Dulce Infancia*)
7. **Manzana Canela** (*Manzana Asada & Canela*)
8. **Coco Flower** (*Flor de Coco & Jazmín*)
9. **Mokka** (*Café Moka & Cacao Tostado*)
10. **Limón** (*Limón Verde*)
11. **Pino** (*Pino Silvestre & Bosque*)
12. **Lavanda** (*Lavanda Francesa*)
13. **Frutal Mango** (*Mango Tropical*)

---

## 🛠️ Generar / Actualizar Etiquetas Automáticamente

Para regenerar las 52 etiquetas de producción con Puppeteer:

1. Asegúrate de tener Node.js instalado.
2. Instala las dependencias necesarias:
   ```bash
   npm install puppeteer-core
   ```
3. Ejecuta el script de generación:
   ```bash
   node generar_revision.js
   ```

El script renderizará y exportará automáticamente todas las etiquetas en ultra alta resolución a las carpetas `revision_manual/` y `etiquetas_impresion/`.

---

## 🌐 Publicación / Visualización Web

Puedes abrir `index.html` directamente en cualquier navegador o servir la carpeta mediante GitHub Pages, Netlify o Vercel. 

### Pasos para subir a GitHub:

```bash
git init
git add .
git commit -m "Initial commit: Jeshia Fragrance Suite & Labels"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/jeshia-branding.git
git push -u origin main
```

---

© 2026 Jeshia. Todos los derechos reservados.
