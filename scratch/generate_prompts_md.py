import os

# 9 Escenarios Únicos de Lifestyle Editorial
SCENES = [
    {
        "id": 1,
        "name": "Salón Principal & Sofá de Lino (Living Contemporáneo)",
        "desc": """Crear un ambiente de salón principal contemporáneo, cálido y acogedor, con fuerte presencia de textiles de alta calidad.
El producto debe estar colocado sobre una mesa de centro o mesa auxiliar de roble natural macizo.
Crear un ambiente editorial de diseño de interiores:
* luz natural suave y difusa entrando por un gran ventanal con cortinas de lino
* sofá tapizado en lino crudo o tela bouclé neutra en segundo plano desenfocado
* manta de punto grueso doblada sobre el respaldo
* materiales nobles: madera de roble claro, lino, cerámica artesanal y algodón
* planta interior de hojas verdes estilizadas (Ficus elástica o Monstera) en maceta de arcilla
* sensación de frescura textil, serenidad y hogar impecable""",
        "props": """* taza de cerámica artesanal humeante (~8-9 cm de alto)
* libro de fotografía o diseño abierto (~22 cm de largo)
* cojín o manta de lino en textura suave al fondo
* pequeño plato cerámico decorativo (~10-12 cm de diámetro)
* vegetación de interior en maceta de arcilla al fondo desenfocado""",
        "lighting": """Luz natural matutina suave y envolvente, tamizada por cortinas translúcidas.
Sombras suaves y difusas que realzan las texturas de la tela y la madera.
Reflejos limpios sobre el vidrio ámbar del frasco.
Atmósfera luminosa, aireada y relajante."""
    },
    {
        "id": 2,
        "name": "Consola de Recibidor & Espejo Orgánico (Hall de Entrada)",
        "desc": """Crear un ambiente de recibidor elegante, sobrio y arquitectónico, pensado para dar una bienvenida aromática refinada.
El producto debe estar colocado sobre una consola de entrada de madera de nogal pulida de líneas puras.
Crear un ambiente similar al de una editorial de arquitectura y decoración:
* luz lateral rasante y suave que entra por un ventanal cercano
* pared con textura sutil de lino, microcemento o tono alabastro neutro
* espejo de pared con marco orgánico de madera en segundo plano desenfocado
* jarrón escultórico de cerámica mate con pequeñas ramas botánicas secas
* libros de arte apilados de forma sobria
* atmósfera de calma zen, diseño refinado y orden impecable""",
        "props": """* jarrón escultórico de cerámica mate (~15-18 cm de alto)
* libro de arte o catálogo de diseño apilado en la mesa
* pequeño cuenco decorativo de piedra o madera (~8-10 cm)
* marco de espejo con curvas suaves al fondo
* lámpara de diseño escultórica apagada en segundo plano desenfocado""",
        "lighting": """Luz natural lateral y rasante de media tarde, suave y direccional.
Genera sombras elegantes y sutiles que destacan la silueta del frasco y sus acabados.
Reflejos naturales sobre el vidrio y tonos cálidos en la madera de nogal.
Atmósfera editorial, tranquila y sofisticada."""
    },
    {
        "id": 3,
        "name": "Rincón de Lectura & Butaca Escandinava (Reading Nook)",
        "desc": """Crear un ambiente íntimo de rincón de lectura, silencio y desconexión personal.
El producto debe estar colocado sobre una mesa velador redonda de madera de fresno o travertino pulido.
Crear un ambiente acogedor y sereno:
* luz natural suave entrando por una ventana lateral alta
* butaca de lectura tapizada en terciopelo o lino cálido en segundo plano
* manta de lana ligera doblada sobre el brazo de la butaca
* estantería minimalista con libros en segundo plano desenfocado
* lámpara de pie de diseño con estructura de latón apagada
* sensación de confort acústico, tranquilidad y calidez de hogar""",
        "props": """* libro de tapa dura abierto con marcapáginas de tela (~20-22 cm)
* gafas de lectura de acetato (~14 cm de ancho)
* pequeño plato cerámico artesanal (~10 cm)
* taza de té o café con textura artesanal (~8 cm)
* textura suave de manta y tapicería al fondo desenfocado""",
        "lighting": """Luz natural cálida y difusa de tarde, filtrada suavemente.
Sombras aterciopeladas que acentúan la sensación de recogimiento e intimidad.
Reflejos dorados suaves sobre el envase de vidrio y superficies nobles.
Atmósfera templada, acogedora y contemplativa."""
    },
    {
        "id": 4,
        "name": "Dormitorio & Suite Principal (Master Bedroom)",
        "desc": """Crear un ambiente de suite principal de alta gama, enfocado en el descanso profundo, la pureza y la relajación.
El producto debe estar colocado sobre una mesa de noche o velador de roble claro o madera decapada.
Crear un ambiente de descanso editorial:
* luz natural matutina dorada y etérea que entra por un gran ventanal
* cama con cabecero tapizado y sábanas de lino o algodón blanco con caída natural
* cojines en tonos crudos, tostados y arena
* cortina vaporosa mecida suavemente por la brisa
* lámpara de sobremesa de cerámica esmaltada apagada
* sensación de pureza, sábanas limpias y bienestar absoluto""",
        "props": """* vaso de vidrio con agua fresca (~10 cm)
* pequeño libro de poesía o notas de tapa dura (~15 cm)
* bandeja pequeña de cerámica o madera clara (~12 cm)
* sábanas y almohadas de lino blanco al fondo desenfocado
* lámpara de noche de cerámica artesanal al fondo (~18 cm)""",
        "lighting": """Luz matutina dorada y muy suave, creando destellos etéreos y limpios.
Sombras tenues que realzan la suavidad de las telas y el brillo natural del vidrio.
Atmósfera pacífica, luminosa y profundamente relajante."""
    },
    {
        "id": 5,
        "name": "Tocador & Vestidor Contemporáneo (Dressing Room)",
        "desc": """Crear un ambiente sofisticado de tocador moderno o vestidor iluminado, enfocado en el cuidado personal y el estilo de vida exclusivo.
El producto debe estar colocado sobre una bandeja de piedra travertino pulido o mármol mate sobre tocador de madera clara.
Crear un ambiente de lifestyle elegante:
* luz natural clara, luminosa y directa de mañana
* espejo con marco curvo de madera o latón al fondo desenfocado
* detalles textiles de vestidor (lino, seda, prendas neutras colgadas)
* pequeño jarrón de vidrio o cerámica individual con una flor fresca
* atmósfera de dinamismo elegante, cuidado personal y sofisticación moderna""",
        "props": """* bandeja de travertino o mármol mate (~15 cm de largo)
* libreta de cuero suave con pluma de metal (~14 cm)
* gafas de sol de acetato de diseño (~14 cm)
* pequeño florero individual con flor fresca (~10 cm)
* espejo de tocador con reflejo suave al fondo desenfocado""",
        "lighting": """Luz natural limpia, nítida y brillante de mañana.
Reflejos nítidos y cristalinos en el vidrio, destacando la precisión de las etiquetas y accesorios.
Atmósfera contemporánea, fresca, nítida y de alta definición."""
    },
    {
        "id": 6,
        "name": "Baño Spa Botánico & Autocuidado (Botanical Spa)",
        "desc": """Crear un ambiente de baño estilo spa nórdico o rincón de bienestar y recarga botánica consciente.
El producto debe estar colocado sobre una mesada de piedra caliza clara, terrazo suave o madera tratada resistente al agua.
Crear un ambiente de autocuidado, pureza y sustentabilidad:
* luz natural suave y filtrada, transmitiendo frescura y serenidad
* toallas de algodón orgánico o lino blanco enrolladas con delicadeza
* plantas de humedad interior (helecho, eucalipto fresco o pothos)
* pared con revestimiento de azulejo artesanal mate o piedra natural
* plato con jabón botánico artesanal
* sensación de ritual de purificación, aire puro y desconexión total""",
        "props": """* toallas de algodón orgánico enrolladas o dobladas (~10-12 cm de alto)
* jabonera de cerámica artesanal con jabón botánico natural (~10 cm)
* pequeña planta botánica de hojas verdes frescas en maceta de arcilla
* cuenco de piedra con sales de baño
* vela aromática apagada en vaso de vidrio (~8 cm)""",
        "lighting": """Luz natural suave, pura y tamizada, como la de un spa nórdico de lujo.
Reflejos luminosos sobre el envase y las superficies pulidas de piedra.
Atmósfera fresca, limpia, revitalizante y equilibrada."""
    },
    {
        "id": 7,
        "name": "Comedor Luminoso & Mesa Rústica Noble (Dining Room)",
        "desc": """Crear un ambiente de comedor amplio y luminoso con mesa de tablones de madera maciza o mueble aparador noble.
El producto debe estar colocado sobre la superficie de madera de roble o castaño con textura natural visible.
Crear un ambiente de abundancia hogareña y encuentro familiar:
* luz natural cálida y abundante que entra por un gran ventanal con vistas al jardín
* cortinas de lino natural en tonos tierra
* jarrón de cerámica con ramas de olivo o follaje verde abundante
* vajilla rústica o cuencos de barro en segundo plano desenfocado
* cesta de fibras naturales en un rincón
* sensación de hogar lleno de vida, hospitalidad y calidez compartida""",
        "props": """* bandeja de fibras naturales o madera rústica (~30 cm)
* jarrón grande de cerámica artesanal con ramas de olivo (~25 cm)
* servilleta de lino doblada con textura rústica
* libro de cocina o recetas de diseño
* luz cálida de sol proyectada sobre la veta de la madera""",
        "lighting": """Luz natural dorada y abundante de media tarde, cálida y envolvente.
Sombras largas y suaves que llenan el espacio de calidez y sensación de hogar habitado.
Reflejos brillantes que realzan la presencia noble del producto.
Atmósfera generosa, reconfortante y hogareña."""
    },
    {
        "id": 8,
        "name": "Cocina & Rincón Gourmet (Kitchen & Coffee Bar)",
        "desc": """Crear un ambiente de cocina contemporánea y luminosa o rincón de café gourmet de alta gama.
El producto debe estar colocado sobre una isla de cocina de madera maciza cálida o mesón de cuarzo/piedra mate.
Crear un ambiente fresco, pulcro y gastronómico refinado:
* luz natural directa pero suave matutina entrando por una ventana de cocina
* azulejos cerámicos artesanales (estilo zellige blanco/crema) al fondo
* repisas abiertas de madera con frascos de vidrio y vajilla rústica
* planta aromática fresca en maceta pequeña (romero, albahaca o menta)
* atmósfera de frescura culinaria, pulcritud absoluta y energía matutina""",
        "props": """* tabla de corte de madera de olivo (~20-25 cm)
* taza de café de especialidad o té artesanal (~8 cm)
* pequeño cuenco de cerámica con cuchara de madera (~8 cm)
* mortero de piedra o molinillo rústico al fondo desenfocado
* maceta pequeña con hierba fresca al fondo""",
        "lighting": """Luz natural de mañana radiante y fresca, creando contrastes limpios y luminosos.
Reflejos nítidos sobre superficies de piedra, vidrio y madera aceitada.
Atmósfera revitalizante, limpia, cristalina y estimulante."""
    },
    {
        "id": 9,
        "name": "Espacio de Trabajo & Home Office Sereno (Studio / Office)",
        "desc": """Crear un ambiente de estudio de trabajo creativo o home office contemporáneo, sereno y ordenado.
El producto debe estar colocado sobre un escritorio amplio de madera de nogal o roble oscuro de acabado mate.
Crear un ambiente de concentración, inspiración y serenidad mental:
* luz natural diurna lateral uniforme, clara y sin reflejos molestos
* pared en tono verde salvia suave, gris cálido o madera alistonada
* estantería minimalista con libros de arquitectura, arte y diseño
* lámpara de sobremesa de diseño escandinavo apagada
* planta colgante discreta (pothos o helecho) en una esquina
* sensación de claridad mental, foco creativo y ambiente puro""",
        "props": """* libreta de notas de diseño con tapas duras (~20 cm)
* pluma estilográfica o lápiz de madera noble
* taza de cerámica japonesa o cuenco para té (~8 cm)
* pisapapeles de cristal o piedra natural
* lámpara de escritorio de diseño apagada al fondo desenfocado""",
        "lighting": """Luz natural lateral uniforme, clara y no cegadora.
Sombras suaves que definen los volúmenes sin oscurecer la escena.
Reflejos sobrios y mates que transmiten profesionalismo y paz.
Atmósfera lúcida, equilibrada, inspiradora y sofisticada."""
    }
]

# Matriz de asignación de escenarios (Garantiza exactamente 9 escenarios únicos y 4 repetidos por cada producto)
# Cada fila corresponde a un producto (13 aromas). Los 9 escenarios aparecen al menos una vez, y 4 se repiten.
SCENE_DISTRIBUTION = [
    # Home Spray: Escenarios 1 al 9, repite 1, 2, 3, 4
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4],
    # Mikado: Escenarios 2 al 9 + 1, repite 2, 3, 4, 5
    [2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5],
    # Aromatizador: Escenarios 5 al 9 + 1 al 4, repite 5, 6, 7, 8
    [5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8],
    # Recarga 250: Escenarios 6 al 9 + 1 al 5, repite 6, 7, 8, 9
    [6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    # Recarga 500: Escenarios 7 al 9 + 1 al 6, repite 7, 8, 9, 1
    [7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
]

products = [
    {
        "filename": "PROMPTS_HOME_SPRAY.md",
        "title": "Prompts para Montajes Visuales — Home Spray Textil & Ambiental (250 ml)",
        "product_type": "Home Spray Textil & Ambiental (250 ml)",
        "packaging": "Frasco de vidrio ámbar de 250 ml con gatillo pulverizador profesional negro (sistema de micro-atomización fina sin manchas).",
        "dimensions": "17,5 cm de alto × 5,7 cm de ancho",
        "scale_details": "17,5 cm de alto × 5,7 cm de ancho (formato medio estilizado). Guardar estricta escala física con los objetos circundantes: el envase es aproximadamente el doble de alto que una taza de café estándar (8-9 cm) y ligeramente más bajo que un libro de pie o jarrón mediano (22-25 cm).",
        "composition_scale": "El producto mide exactamente 17,5 cm de alto × 5,7 cm de ancho. Mantener una escala física y óptica estrictamente realista respecto a todos los objetos secundarios (tazas, libros, platos y elementos botánicos). Evitar que los objetos circundantes se vean desproporcionadamente grandes o pequeños."
    },
    {
        "filename": "PROMPTS_MIKADO.md",
        "title": "Prompts para Montajes Visuales — Difusor de Varillas Mikado (50 ml)",
        "product_type": "Difusor de Varillas Mikado (50 ml)",
        "packaging": "Frasco de vidrio ámbar cilíndrico de 50 ml con cuello protector y juego de 6 varillas difusoras de ratán poroso natural.",
        "dimensions": "7 cm de alto × 4,7 cm de ancho (frasco de vidrio; las 6 varillas alcanzan ~18-20 cm de altura total)",
        "scale_details": "El frasco de vidrio mide solo 7 cm de alto × 4,7 cm de ancho (cuerpo compacto, similar en altura a una taza pequeña de espresso). Las 6 varillas de ratán sobresalen del cuello alcanzando una altura total de ~18-20 cm. Los elementos de la mesa deben guardar estricta proporción con este frasco pequeño y elegante.",
        "composition_scale": "El frasco de vidrio mide 7 cm de alto × 4,7 cm de ancho. Es fundamental respetar su escala compacta: una taza estándar (8-9 cm) o un jarrón cercano son más altos que el frasco de vidrio. Las varillas de ratán aportan la altura vertical (~18-20 cm) de forma estilizada."
    },
    {
        "filename": "PROMPTS_AROMATIZADOR.md",
        "title": "Prompts para Montajes Visuales — Aromatizador Compacto & Auto (15 ml)",
        "product_type": "Aromatizador Compacto & Auto (15 ml)",
        "packaging": "Frasco cilíndrico de vidrio de 15 ml con pulverizador spray directo de precisión y tapa protectora hermética.",
        "dimensions": "5 cm de alto × 4,5 cm de ancho",
        "scale_details": "5 cm de alto × 4,5 cm de ancho (formato ultra compacto de bolsillo / viaje). Es un frasco miniatura que cabe perfectamente en la palma de la mano. Los objetos circundantes (gafas de sol de 14 cm de largo, una libreta de 15 cm o un plato de 10 cm) deben evidenciar con total fidelidad su tamaño pequeño y exclusivo.",
        "composition_scale": "El producto es muy compacto (5 cm de alto × 4,5 cm de ancho). La cámara y los objetos en primer plano deben reflejar con exactitud su escala pequeña, portátil y de bolsillo, evitando agigantarlo artificialmente frente a los elementos decorativos."
    },
    {
        "filename": "PROMPTS_RECARGA_250ML.md",
        "title": "Prompts para Montajes Visuales — Recarga Eco-Refill (250 ml)",
        "product_type": "Recarga Eco-Refill (250 ml)",
        "packaging": "Botella ecológica PET ámbar reciclable de 250 ml con tapa dosificadora antigoteo para recarga limpia.",
        "dimensions": "17,5 cm de alto × 6 cm de ancho",
        "scale_details": "17,5 cm de alto × 6 cm de ancho (botella cilíndrica de 250 ml). Guarda escala física idéntica en altura con el Home Spray de 250 ml y es claramente más alta que los difusores de 50 ml y aromatizadores de 15 ml.",
        "composition_scale": "La botella mide 17,5 cm de alto × 6 cm de ancho. Su escala en primer plano debe guardar estricta relación física con toallas enrolladas (~12 cm de diámetro), jaboneras artesanales (10-12 cm) y plantas de baño."
    },
    {
        "filename": "PROMPTS_RECARGA_500ML.md",
        "title": "Prompts para Montajes Visuales — Recarga Familiar Maxi-Refill (500 ml)",
        "product_type": "Recarga Familiar Maxi-Refill (500 ml)",
        "packaging": "Botella ecológica PET ámbar de gran capacidad (500 ml) con boquilla dosificadora de precisión para múltiples recargas.",
        "dimensions": "19 cm de alto × 6,3 cm de ancho",
        "scale_details": "19 cm de alto × 6,3 cm de ancho (formato familiar de gran capacidad). Es el envase más alto y corpulento de toda la colección de Jeshia (19 cm), superando en tamaño a todos los demás frascos.",
        "composition_scale": "La botella mide 19 cm de alto × 6,3 cm de ancho. Debe transmitir con total realismo su presencia generosa y capacidad de 500 ml, manteniendo proporciones físicas físicamente correctas con bandejas grandes, jarras y frascos secundarios."
    }
]

aromas = [
    {
        "id": "vainilla-coco",
        "name": "Vainilla Coco",
        "family": "Gourmand & Dulce",
        "liquid_color": "Tono marfil cálido / vainilla dorada muy suave, brillante y translúcido.",
        "refs": "Vainas de vainilla bourbon (~15 cm de largo, delgadas), pulpa y leche de coco rallada, flor de vainilla, azúcar moreno, madera de sándalo y haba tonka.",
        "concept": "Cálido, Dulce, Envolvente, Reconfortante, Relajante.",
        "example": "Una o dos vainas de vainilla bourbon natural (~15 cm, delgadas y flexibles) y un trozo sutil de coco seco o rallado sobre un pequeño platillo cerámico artesanal (~10 cm), acompañado de textiles de lino en tonos crema y beige."
    },
    {
        "id": "citric",
        "name": "Citric",
        "family": "Cítrico & Fresco",
        "liquid_color": "Tono amarillo cítrico / dorado solar muy suave, limpio y translúcido.",
        "refs": "Cáscaras de bergamota, rodajas de pomelo rosado (~6-7 cm), mandarina italiana, flor de azahar, hojas de lemongrass y cedro claro.",
        "concept": "Cítrico, Fresco, Revitalizante, Chispeante, Energizante.",
        "example": "Pequeñas rodajas deshidratadas (~5 cm) o cáscaras frescas de bergamota y pomelo rosado sobre una bandeja de madera clara, junto a una hoja verde fresca de lemongrass."
    },
    {
        "id": "berries",
        "name": "Berries",
        "family": "Frutal & Silvestre",
        "liquid_color": "Tono rojo rubí / frambuesa muy claro, sutil, elegante y translúcido.",
        "refs": "Frambuesas silvestres (~1,5-2 cm), moras negras (~2 cm), grosellas rojas, arándanos frescos (~1 cm) y hojas verdes de bosque.",
        "concept": "Frutal, Jugoso, Vibrante, Dulce silvestre, Dinámico.",
        "example": "Un pequeño puñado de frambuesas silvestres y moras frescas (escala real 1,5-2 cm cada fruto) dispuestas elegantemente sobre un platillo de cerámica mate (~10 cm) o bandeja de madera, aportando un acento de color granate natural sin sobrecargar."
    },
    {
        "id": "coco-nut",
        "name": "Coco Nut",
        "family": "Gourmand & Dulce",
        "liquid_color": "Tono crema marfil / coco suave muy sutil, cálido y translúcido.",
        "refs": "Nuez de coco abierta, pulpa fresca de coco, agua de coco, avellanas tostadas (~1,5 cm), almendras amargas y vainilla pura.",
        "concept": "Cremoso, Cálido, Exótico, Tostado, Tropical.",
        "example": "Un trozo rústico de cáscara o pulpa de coco natural (~5-6 cm) junto a dos avellanas tostadas en un cuenco artesanal de arcilla, transmitiendo una textura tropical sobria y sofisticada en escala proporcional."
    },
    {
        "id": "sugar",
        "name": "Sugar",
        "family": "Gourmand & Dulce",
        "liquid_color": "Tono dorado miel / caramelo muy claro, suave, brillante y translúcido.",
        "refs": "Cristales de azúcar dorada, hilos finos de caramelo artesanal, sirope de arce, mantequilla tostada y vainilla de Madagascar.",
        "concept": "Dulce, Goloso, Cálido, Nostálgico, Acogedor.",
        "example": "Una pequeña cuchara de cerámica (~10 cm) o cuenco con cristales de azúcar dorada o caramelo artesanal seco, junto a una taza de cerámica artesanal y textiles cálidos."
    },
    {
        "id": "chicle",
        "name": "Chicle",
        "family": "Frutal & Lúdico",
        "liquid_color": "Tono rosa suave / chicle muy claro, delicado, luminoso y translúcido.",
        "refs": "Fresas glaseadas (~2,5 cm), cerezas silvestres (~1,5 cm), plátano dulce, manzana rosa confitada y azúcar glass.",
        "concept": "Dulce, Efervescente, Lúdico, Alegre, Creativo.",
        "example": "Un par de fresas frescas y pequeñas cerezas silvestres dispuestas sobre un platillo decorativo contemporáneo (~10 cm), con iluminación luminosa y vibrante pero refinada en escala natural."
    },
    {
        "id": "manzana-canela",
        "name": "Manzana Canela",
        "family": "Especiado & Cálido",
        "liquid_color": "Tono ámbar canela / dorado cobrizo suave, cálido y translúcido.",
        "refs": "Un par de gajos de manzana roja fresca cortada con piel (uno de los gajos mostrando sutilmente un par de semillas oscuras visibles), astillas de canela en rama de Ceilán (~8-10 cm de largo), nuez moscada y corteza de cedro.",
        "concept": "Cálido, Especiado, Acogedor, Festivo, Reconfortante.",
        "example": "Un par de gajos de manzana fresca cortada con piel roja brillante (uno de ellos con algunas pocas semillas visibles) y dos ramas delgadas de canela de Ceilán (~8-10 cm) atadas con cordel natural sobre una superficie de madera noble o pequeño plato cerámico."
    },
    {
        "id": "coco-flower",
        "name": "Coco Flower",
        "family": "Floral & Delicado",
        "liquid_color": "Tono cristalino etéreo con suave reflejo floral / blanco sedoso translúcido.",
        "refs": "Flores blancas de coco, pétalos de jazmín nocturno (~2 cm), flor de tiaré (~4-5 cm), gardenias blancas y notas acuáticas suaves.",
        "concept": "Floral, Elegante, Delicado, Sedoso, Relajante, Etéreo.",
        "example": "Pequeñas flores blancas delicadas (jazmín o flor de tiaré de 3-4 cm) dispuestas sobre una servilleta de lino blanco o flotando sutilmente en un cuenco cerámico con agua cristalina."
    },
    {
        "id": "mokka",
        "name": "Mokka",
        "family": "Gourmand & Especiado",
        "liquid_color": "Tono ámbar suave / dorado tostado café claro, elegante y translúcido.",
        "refs": "Granos de café arábica tostado (~1 cm de tamaño), nibs de cacao amargo, licor de café, semillas de cardamomo, madera de roble y vainilla bourbon.",
        "concept": "Cálido, Elegante, Profundo, Estimulante, Sofisticado.",
        "example": "Un pequeño puñado de granos de café arábica recién tostados (~1 cm cada grano) y nibs de cacao oscuro sobre la mesa de madera o en un platillo cerámico rústico (~8-10 cm), junto a un libro de tapa dura."
    },
    {
        "id": "limon",
        "name": "Limón",
        "family": "Cítrico & Fresco",
        "liquid_color": "Tono ligeramente amarillo / amarillo suave translúcido, brillante y limpio.",
        "refs": "Limón amarillo fresco maduro (~5-6 cm de diámetro, entero o con un gajo/rodaja fina), corteza de limón amarillo brillante, hojas de verbena silvestre, menta fresca y cedro blanco.",
        "concept": "Cítrico, Fresco, Efervescente, Purificante, Limpio.",
        "example": "Un limón amarillo fresco maduro (~5-6 cm) entero o con una rodaja/gajo junto a hojas frescas de verbena o menta silvestre sobre una tabla de madera o piedra clara, aportando luminosidad cítrica y máxima pulcritud en escala real."
    },
    {
        "id": "pino",
        "name": "Pino",
        "family": "Amaderado & Bosque",
        "liquid_color": "Tono verde bosque / salvia suave muy claro, natural y translúcido.",
        "refs": "Acículas de pino silvestre, piñas de pino pequeñas (~4-5 cm), eucalipto azul, musgo de roble húmedo, corteza balsámica y resina de ámbar.",
        "concept": "Boscoso, Fresco, Resinoso, Purificante, Natural, Sereno.",
        "example": "Una pequeña ramita de pino silvestre verde con agículas frescas y una pequeña piña seca (~4 cm) reposando de forma natural sobre la mesa de madera, evocando la frescura del bosque andino."
    },
    {
        "id": "lavanda",
        "name": "Lavanda",
        "family": "Floral & Terapéutico",
        "liquid_color": "Tono lila / violeta lavanda muy claro, sutil, delicado y translúcido.",
        "refs": "Espigas y flores de lavanda francesa (~10-12 cm de espiga), hojas de salvia silvestre, romero fresco y flores de manzanilla.",
        "concept": "Floral, Relajante, Aromaterapéutico, Calmante, Sereno.",
        "example": "Un pequeño ramillete de espigas delgadas de lavanda francesa (~10-12 cm de largo, fresca o seca) atado con fibra natural, reposando junto a un libro abierto o sobre una manta de punto suave."
    },
    {
        "id": "frutal-mango",
        "name": "Frutal Mango",
        "family": "Frutal & Tropical",
        "liquid_color": "Tono naranja mango / durazno dorado muy claro, luminoso, fresco y translúcido.",
        "refs": "Pulpa dorada de mango maduro, néctar de papaya dulce, fruta de la pasión / maracuyá (~5-6 cm), flores de hibisco y caña de azúcar.",
        "concept": "Frutal, Tropical, Jugoso, Exótico, Solar, Dinámico.",
        "example": "Cortes sutiles de mango maduro o rodajas deshidratadas de fruta tropical (~4-5 cm) en un pequeño plato de cerámica artesanal, aportando luminosidad dorada y calidez exótica refinada."
    }
]

def generate_prompt(prod, aroma, aroma_idx, p_idx):
    scene_id = SCENE_DISTRIBUTION[p_idx][aroma_idx]
    scene = next(s for s in SCENES if s["id"] == scene_id)

    return f"""## {aroma_idx + 1}. Aroma: {aroma['name']} ({aroma['family']}) — Escenario: {scene['name']}

```text
Crear una fotografía publicitaria lifestyle de alta gama para presentar un producto aromático de hogar, utilizando como referencias principales la imagen del envase base y la etiqueta adjunta correspondiente al aroma.

### PRODUCTO

* Tipo de producto: {prod['product_type']}
* Envase: {prod['packaging']}
* Dimensiones reales del envase: {prod['dimensions']}
* Escala física y proporción: {prod['scale_details']}
* Color del líquido en el envase: {aroma['liquid_color']}
* Aroma: {aroma['name']}
* Familia olfativa: {aroma['family']}
* Referencias visuales del aroma: {aroma['refs']}
* Concepto sensorial: {aroma['concept']}

### PRODUCTO Y ENVASE

Mantener exactamente la identidad visual y estructura del envase proporcionado como referencia.

REGLA DE ENVASE Y ETIQUETA:
El diseño físico del envase (forma, proporciones reales de {prod['dimensions']}, material, color base, tapa, atomizador/varillas) no se modifica y permanece constante.
Lo ÚNICO que cambia en el envase es la etiqueta, la cual debe corresponder exactamente al diseño de la etiqueta oficial del aroma "{aroma['name']}" adjunta como referencia.

Conservar:

* forma y proporciones reales del envase base ({prod['dimensions']}) sin alteraciones
* material del envase (vidrio ámbar / PET ecológico según corresponda)
* color y transparencia del vidrio o envase, mostrando el líquido en su interior con un matiz {aroma['liquid_color']}
* tapa, cuello, atomizador y accesorios originales
* etiqueta: aplicar con total fidelidad el diseño de la etiqueta oficial del aroma "{aroma['name']}" adjunta como referencia
* logotipo Jeshia, tipografías, colores, ilustraciones botánicas y textos de la etiqueta adjunta
* proporciones y ubicación correcta de la etiqueta sobre el envase
* detalles y acabados del producto

El líquido visible en el envase debe tener una apariencia translúcida, limpia y natural que corresponda al aroma ({aroma['liquid_color']}), reflejando sutilmente la luz ambiental.

El producto debe ser el protagonista absoluto de la imagen, claramente visible y correctamente orientado hacia la cámara.

NO modificar el diseño ni la forma del envase.
NO distorsionar la escala ni las proporciones reales ({prod['dimensions']}).
NO rediseñar, reinterpretar ni deformar la etiqueta adjunta.
NO inventar textos ni tipografías.
NO cambiar el nombre del producto.
NO agregar elementos gráficos sobre el envase.

### ESCENA: {scene['name'].upper()}

{scene['desc']}

El fondo debe estar desenfocado mediante profundidad de campo fotográfica realista, manteniendo el producto perfectamente enfocado.

### REPRESENTACIÓN DEL AROMA

Utilizar el aroma "{aroma['name']}" como inspiración visual para construir pequeños elementos naturales relacionados con su fragancia.

Las referencias del aroma deben aparecer de manera elegante, realista y sutil dentro de la escena, respetando la escala física real 1:1 respecto al envase de {prod['dimensions']}, nunca como una colección artificial de ingredientes.

Utilizar:
{aroma['refs']}

Los elementos aromáticos deben:

* respetar el tamaño físico real de los ingredientes (frutas, flores, especias o ramas a escala 1:1)
* complementar visualmente el producto sin agigantarse frente al envase
* reforzar la percepción del aroma
* parecer parte natural de la decoración
* utilizarse en cantidades moderadas
* mantener una estética premium
* tener apariencia fotográfica real
* estar integrados naturalmente en la composición

NO colocar los ingredientes directamente sobre la etiqueta.
NO cubrir el producto.
NO hacer una composición tipo catálogo de ingredientes.
NO utilizar ilustraciones.
NO crear frutas, flores o elementos flotando alrededor del producto.
NO convertir la escena en una fotografía gastronómica.

### EJEMPLO DE INTERPRETACIÓN DEL AROMA

{aroma['example']}

Las referencias deben adaptarse automáticamente al aroma indicado y nunca deben utilizarse si no tienen relación con la fragancia.

### COMPOSICIÓN Y ESCALA FÍSICA

Composición fotográfica vertical, premium y editorial.

REGLA DE ESCALA Y PROPORCIÓN FÍSICA REAL:
{prod['composition_scale']}
Todos los elementos en primer y segundo plano (vajilla, libros, accesorios, frutas, especias, flores y ramas) deben tener un tamaño físicamente coherente y realista respecto a los {prod['dimensions']} del producto. Ningún elemento decorativo o fruto debe verse sobredimensionado o miniaturizado de forma irreal.

El producto debe ocupar aproximadamente entre 25% y 40% de la altura del encuadre, ubicado en una zona visualmente dominante, en primer plano y ligeramente descentrado para generar una composición más natural.

Incluir algunos elementos secundarios relacionados con el estilo de vida de este espacio ({scene['name']}):

{scene['props']}

Estos elementos deben permanecer en segundo plano mediante profundidad de campo óptica, guardando su escala física real y nunca compitiendo visualmente con el producto.

Crear una composición equilibrada utilizando profundidad, escala y perspectiva fotográfica real.

### ILUMINACIÓN

{scene['lighting']}
Sin sobreexposición.
Sin sombras artificiales excesivamente marcadas.
Sin iluminación de estudio demasiado dura.

### ESTÉTICA

Fotografía comercial premium de producto.
Editorial de decoración y lifestyle.
Minimalismo cálido.
Elegancia natural.
Sensación de bienestar, hogar y sofisticación.

Paleta cromática adaptada al aroma y al producto, utilizando tonos naturales y armónicos.

La escena debe sentirse:
realista, aspiracional, cálida, sofisticada, limpia y auténtica.

### CÁMARA Y CALIDAD

Fotografía hiperrealista.
Aspecto de cámara profesional full-frame.
Lente fotográfica de aproximadamente 50–85 mm.
Profundidad de campo reducida.
Producto perfectamente enfocado en su escala física real.
Fondo suavemente desenfocado.
Bokeh natural.
Texturas realistas.
Vidrio, líquido translúcido, madera, tela, cerámica y materiales naturales físicamente correctos.
Perspectiva realista.
Alta resolución.
Calidad de fotografía publicitaria profesional.
Sin apariencia de render 3D ni desproporción de escala.

### REGLA PRINCIPAL

El producto y su identidad visual son la prioridad absoluta: el diseño del envase base es constante y lo único que se reemplaza es la etiqueta adjunta de cada aroma. Mantiene todos los aspectos de la imagen de referencias original.

Los elementos relacionados con el aroma y la tonalidad del líquido visible deben funcionar únicamente como recursos narrativos para comunicar sensorialmente la fragancia, respetando en todo momento las dimensiones físicas reales ({prod['dimensions']}) en relación con los objetos de la escena.

La imagen debe hacer que el espectador pueda asociar visualmente el producto con su aroma sin necesidad de leer una explicación.

Resultado final: una fotografía lifestyle premium, cálida, elegante y comercial, donde el envase sea el protagonista inalterable, la etiqueta oficial adjunta identifique con exactitud el aroma, las dimensiones del producto guarden perfecta coherencia óptica con los objetos de primer plano y el ambiente comunique de manera visual la personalidad de la fragancia.
```

---
"""

base_dir = r"e:\Logo Jeshia"

for p_idx, prod in enumerate(products):
    filepath = os.path.join(base_dir, prod["filename"])
    
    # Calcular lista de escenarios asignados para el encabezado
    assigned_scenes = [SCENE_DISTRIBUTION[p_idx][i] for i in range(13)]
    unique_count = len(set(assigned_scenes))
    
    content = f"""# {prod['title']}

Colección de prompts fotográficos adaptados para la generación de montajes visuales y fotografía publicitaria lifestyle de alta gama para **{prod['product_type']}** en las 13 fragancias de Jeshia.

> **Dimensiones Reales del Envase:** `{prod['dimensions']}`  
> **Distribución de Escenarios:** Este formato cuenta con **{unique_count} escenarios únicos** distribuidos entre sus 13 aromas (9 únicos + 4 repeticiones controladas), garantizando variedad visual sin perder la coherencia de marca.  
> **Regla de Escala y Proporción:** Relación física y óptica estricta 1:1 entre el envase y todos los elementos circundantes.  
> **Regla de Envase y Etiqueta:** El diseño del envase base se mantiene constante (forma, materiales y accesorios). Lo **único que cambia** en el envase es la etiqueta oficial adjunta de cada aroma. Mantiene todos los aspectos de la imagen de referencias original.

---

"""
    for aroma_idx, aroma in enumerate(aromas):
        content += generate_prompt(prod, aroma, aroma_idx, p_idx)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated {prod['filename']} with 9 unique scenes distribution")

print("All 5 prompt files successfully generated with 9 unique scenes distributed!")
