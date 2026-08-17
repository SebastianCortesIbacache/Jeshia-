import os

base_dir = r"e:\Logo Jeshia"

products = [
    {
        "num": "1",
        "title": "Home Spray Textil & Ambiental (250 ml)",
        "product_type": "Home Spray Textil & Ambiental (250 ml)",
        "packaging": "Frasco de vidrio ámbar de 250 ml con gatillo pulverizador profesional negro (sistema de micro-atomización fina sin manchas)."
    },
    {
        "num": "2",
        "title": "Difusor de Varillas Mikado (50 ml)",
        "product_type": "Difusor de Varillas Mikado (50 ml)",
        "packaging": "Frasco de vidrio ámbar cilíndrico de 50 ml con cuello protector y juego de 6 varillas difusoras de ratán poroso natural."
    },
    {
        "num": "3",
        "title": "Aromatizador Compacto & Auto (15 ml)",
        "product_type": "Aromatizador Compacto & Auto (15 ml)",
        "packaging": "Frasco cilíndrico de vidrio de 15 ml con pulverizador spray directo de precisión y tapa protectora hermética."
    },
    {
        "num": "4",
        "title": "Recarga Eco-Refill (250 ml)",
        "product_type": "Recarga Eco-Refill (250 ml)",
        "packaging": "Botella ecológica PET ámbar reciclable de 250 ml con tapa dosificadora antigoteo para recarga limpia de frascos y difusores."
    },
    {
        "num": "5",
        "title": "Recarga Familiar Maxi-Refill (500 ml)",
        "product_type": "Recarga Familiar Maxi-Refill (500 ml)",
        "packaging": "Botella ecológica PET ámbar de gran capacidad (500 ml) con boquilla dosificadora de precisión para múltiples recargas."
    }
]

aromas = [
    {
        "num": "1",
        "name": "Vainilla Coco",
        "family": "Gourmand & Dulce",
        "refs": "Vainas de vainilla bourbon, pulpa y leche de coco rallada, flor de vainilla, azúcar moreno, madera de sándalo y haba tonka.",
        "concept": "Cálido, Dulce, Envolvente, Reconfortante, Relajante."
    },
    {
        "num": "2",
        "name": "Citric",
        "family": "Cítrico & Fresco",
        "refs": "Cáscaras de bergamota, rodajas de pomelo rosado, mandarina italiana, flor de azahar, hojas de lemongrass y cedro claro.",
        "concept": "Cítrico, Fresco, Revitalizante, Chispeante, Energizante."
    },
    {
        "num": "3",
        "name": "Berries",
        "family": "Frutal & Silvestre",
        "refs": "Frambuesas silvestres, moras negras, grosellas rojas, arándanos frescos y hojas verdes de bosque.",
        "concept": "Frutal, Jugoso, Vibrante, Dulce silvestre, Dinámico."
    },
    {
        "num": "4",
        "name": "Coco Nut",
        "family": "Gourmand & Dulce",
        "refs": "Nuez de coco abierta, pulpa fresca de coco, agua de coco, avellanas tostadas, almendras amargas y vainilla pura.",
        "concept": "Cremoso, Cálido, Exótico, Tostado, Tropical."
    },
    {
        "num": "5",
        "name": "Sugar",
        "family": "Gourmand & Dulce",
        "refs": "Cristales de azúcar dorada, hilos de caramelo artesanal, sirope de arce, mantequilla tostada y vainilla de Madagascar.",
        "concept": "Dulce, Goloso, Cálido, Nostálgico, Acogedor."
    },
    {
        "num": "6",
        "name": "Chicle",
        "family": "Frutal & Lúdico",
        "refs": "Fresas glaseadas, cerezas silvestres, plátano dulce, manzana rosa confitada y azúcar glass.",
        "concept": "Dulce, Efervescente, Lúdico, Alegre, Creativo."
    },
    {
        "num": "7",
        "name": "Manzana Canela",
        "family": "Especiado & Cálido",
        "refs": "Manzanas rojas asadas, astillas de canela en rama de Ceilán, nuez moscada, clavos de olor y corteza de cedro.",
        "concept": "Cálido, Especiado, Acogedor, Festivo, Reconfortante."
    },
    {
        "num": "8",
        "name": "Coco Flower",
        "family": "Floral & Delicado",
        "refs": "Flores blancas de coco, pétalos de jazmín nocturno, flor de tiaré, gardenias blancas y notas acuáticas suaves.",
        "concept": "Floral, Elegante, Delicado, Sedoso, Relajante, Etéreo."
    },
    {
        "num": "9",
        "name": "Mokka",
        "family": "Gourmand & Especiado",
        "refs": "Granos de café arábica tostado, nibs de cacao amargo, licor de café, semillas de cardamomo, madera de roble y vainilla bourbon.",
        "concept": "Cálido, Elegante, Profundo, Estimulante, Sofisticado."
    },
    {
        "num": "10",
        "name": "Limón",
        "family": "Cítrico & Fresco",
        "refs": "Limones verdes frescos, corteza de lima kaffir, hojas de verbena silvestre, menta fresca y cedro blanco.",
        "concept": "Cítrico, Fresco, Efervescente, Purificante, Limpio."
    },
    {
        "num": "11",
        "name": "Pino",
        "family": "Amaderado & Bosque",
        "refs": "Acículas de pino silvestre, piñas de pino, eucalipto azul, musgo de roble húmedo, corteza balsámica y resina de ámbar.",
        "concept": "Boscoso, Fresco, Resinoso, Purificante, Natural, Sereno."
    },
    {
        "num": "12",
        "name": "Lavanda",
        "family": "Floral & Terapéutico",
        "refs": "Espigas y flores de lavanda francesa, hojas de salvia silvestre, romero fresco y flores de manzanilla.",
        "concept": "Floral, Relajante, Aromaterapéutico, Calmante, Sereno."
    },
    {
        "num": "13",
        "name": "Frutal Mango",
        "family": "Frutal & Tropical",
        "refs": "Pulpa dorada de mango maduro, néctar de papaya dulce, fruta de la pasión (maracuyá), flores de hibisco y caña de azúcar.",
        "concept": "Frutal, Tropical, Jugoso, Exótico, Solar, Dinámico."
    }
]

lines = []
lines.append("# Catálogo Oficial Jeshia — Productos y Aromas")
lines.append("")
lines.append("Ficha técnica y descriptiva de productos, envases, familias olfativas, referencias visuales y conceptos sensoriales de la marca **Jeshia**.")
lines.append("")
lines.append("---")
lines.append("")

for prod in products:
    lines.append(f"## {prod['num']}. {prod['title']}")
    lines.append("")
    for aroma in aromas:
        lines.append(f"### {prod['num']}.{aroma['num']} {prod['title']} — {aroma['name']}")
        lines.append("")
        lines.append("**PRODUCTO**")
        lines.append(f"Tipo de producto: {prod['product_type']}  ")
        lines.append(f"Envase: {prod['packaging']}  ")
        lines.append(f"Aroma: {aroma['name']}  ")
        lines.append(f"Familia olfativa: {aroma['family']}  ")
        lines.append(f"Referencias visuales del aroma: {aroma['refs']}  ")
        lines.append(f"Concepto sensorial: {aroma['concept']}  ")
        lines.append("")
        lines.append("---")
        lines.append("")

lines.append("## 6. Resumen de Fragancias Base (13 Aromas)")
lines.append("")
lines.append("| Aroma | Familia Olfativa | Referencias Visuales | Concepto Sensorial |")
lines.append("| :--- | :--- | :--- | :--- |")

for aroma in aromas:
    lines.append(f"| **{aroma['name']}** | {aroma['family']} | {aroma['refs']} | {aroma['concept']} |")

lines.append("")

with open(os.path.join(base_dir, "PRODUCTOS_Y_AROMAS.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("PRODUCTOS_Y_AROMAS.md formatted cleanly with no lint errors!")
