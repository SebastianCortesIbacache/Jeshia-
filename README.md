# Jeshia — Brand Identity & High-Resolution Label Suite

Este repositorio contiene la identidad visual, la suite completa de **etiquetas para producción impresa (HD/300+ DPI)** y las **propuestas de sitio web e-commerce** para la marca de cosmética y perfumes **Jeshia**.

---

## 🌿 Estructura del Proyecto

```
Logo Jeshia/
├── index.html                   # Dashboard principal de presentación del proyecto
├── generar_revision.js          # Script principal de generación automática de etiquetas HD
├── generate_labels.js           # Generador de etiquetas para suite web
├── README.md                    # Documentación del proyecto
├── .gitignore                   # Archivos ignorados para Git
├── assets/                      # Logos e ilustraciones botánicasvectorizadas/limpias
│   ├── logos/                   # Logotipo oficial de Jeshia
│   ├── aromas_botanicos/        # Ilustraciones botánicas transparentes por aroma
│   └── envases/                 # Fotografías y montajes realistas de producto
├── etiquetas/                   # Suite interactiva y manual de marca
│   ├── index.html               # Galería interactiva con vista de productos y montajes
│   └── manual_logo.html         # Manual interactivo de uso del logo
├── etiquetas_impresion/         # Portal de descarga de etiquetas HD (listas para imprenta)
│   ├── index.html               # Visor HD con descarga directa de PNGs
│   ├── 01_Mikado_50x25mm/       # 13 etiquetas formato horizontal Mikado (50x25 mm)
│   ├── 02_Home_Spray_60x75mm/   # 13 etiquetas formato vertical Home Spray 250 ML (60x75 mm)
│   ├── 04_Recarga_250ml_60x75mm/# 13 etiquetas formato vertical Recarga Eco 250 ML (60x75 mm)
│   └── 05_Recarga_500ml_60x100mm/# 13 etiquetas formato vertical Recarga Familiar 500 ML (75x120 mm)
├── revision_manual/             # Salida de la suite oficial completa de etiquetas
└── propuesta-a / b / c /        # 3 propuestas completas de tienda e-commerce
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
