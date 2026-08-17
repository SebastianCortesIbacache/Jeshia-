/**
 * Jeshia — Catálogo Oficial de Fragancias y Productos
 * Datos estructurados para la tienda y experiencia interactiva
 */

const FRAGRANCES = [
  {
    id: 'vainilla-coco',
    name: 'Vainilla Coco',
    subtitle: 'Vainilla Bourbon & Crema de Coco',
    family: 'dulce',
    familyName: 'Gourmand & Dulce',
    color: '#D4A373',
    icon: '🥥',
    image: 'assets/aromas_botanicos/vainilla_coco.png',
    bgNote: 'Cálido, envolvente y reconfortante',
    description: 'Una fusión sedosa de vainilla madura con leche de coco recién rallada y un toque tostado. Transmite calidez, serenidad y sensación de hogar.',
    notes: {
      top: 'Crema de Coco, Néctar de Vainilla',
      heart: 'Flor de Vainilla, Azúcar Moreno',
      base: 'Madera de Sándalo, Haba Tonka'
    },
    mood: 'Relajación, calidez y momentos de descanso',
    space: 'Dormitorios, salas de estar y spas',
    intensity: 4
  },
  {
    id: 'citric',
    name: 'Citric',
    subtitle: 'Cítricos Frescos & Bergamota',
    family: 'citrico',
    familyName: 'Cítrico & Fresco',
    color: '#E9C46A',
    icon: '🍊',
    image: 'assets/aromas_botanicos/citric.png',
    bgNote: 'Revitalizante, chispeante y luminoso',
    description: 'Explosión de cáscaras de bergamota, pomelo rosado y mandarina italiana. Despeja la mente, eleva el ánimo y purifica la atmósfera.',
    notes: {
      top: 'Bergamota, Pomelo Rosado, Mandarina',
      heart: 'Flor de Azahar, Lemongrass',
      base: 'Almizcle Blanco, Cedro Claro'
    },
    mood: 'Concentración, energía matutina y frescura',
    space: 'Espacios de trabajo, cocinas y recepciones',
    intensity: 4
  },
  {
    id: 'berries',
    name: 'Berries',
    subtitle: 'Frutos Rojos & Silvestres',
    family: 'frutal',
    familyName: 'Frutal & Silvestre',
    color: '#9E2A2B',
    icon: '🫐',
    image: 'assets/aromas_botanicos/berries.png',
    bgNote: 'Jugoso, vibrante y tentador',
    description: 'Cosecha de frambuesas silvestres, moras y grosellas negras con un sutil corazón aterciopelado. Aporta vitalidad y alegría a cada rincón.',
    notes: {
      top: 'Frambuesa Silvestre, Mora Negra',
      heart: 'Grosella Roja, Arándanos',
      base: 'Almizcle Dulce, Madera de Guayaco'
    },
    mood: 'Alegría, dinamismo y optimismo',
    space: 'Salas comunes, recibidores y terrazas',
    intensity: 5
  },
  {
    id: 'coco-nut',
    name: 'Coco Nut',
    subtitle: 'Nuez de Coco & Crema',
    family: 'dulce',
    familyName: 'Gourmand & Dulce',
    color: '#C89F77',
    icon: '🌴',
    image: 'assets/aromas_botanicos/coco_nut.png',
    bgNote: 'Cremoso, exótico y tostado',
    description: 'Textura cremosa de nuez de coco con acordes de avellana tostada y mantequilla dulce. Una experiencia tropical sofisticada.',
    notes: {
      top: 'Agua de Coco, Almendra Amarga',
      heart: 'Pulpa de Coco, Crema de Avellana',
      base: 'Vainilla Pura, Almizcle Ámbar'
    },
    mood: 'Confort, bienestar y evasión tropical',
    space: 'Salones, baños principales y salas de lectura',
    intensity: 3
  },
  {
    id: 'sugar',
    name: 'Sugar',
    subtitle: 'Azúcar Dulce & Caramelo',
    family: 'dulce',
    familyName: 'Gourmand & Dulce',
    color: '#E76F51',
    icon: '🍬',
    image: 'assets/aromas_botanicos/sugar.png',
    bgNote: 'Dulce, goloso y nostálgico',
    description: 'El encanto del azúcar cristalizada al fuego con hilos de caramelo dorado y toques avainillados. Un tributo a la repostería artesanal.',
    notes: {
      top: 'Azúcar Hilada, Sirope de Arce',
      heart: 'Caramelo Artesanal, Mantequilla Tostada',
      base: 'Vainilla de Madagascar, Benjuí'
    },
    mood: 'Ternura, calidez familiar e indulgencia',
    space: 'Cocinas, comedores y áreas de café',
    intensity: 4
  },
  {
    id: 'chicle',
    name: 'Chicle',
    subtitle: 'Bubblegum & Dulce Infancia',
    family: 'frutal',
    familyName: 'Frutal & Lúdico',
    color: '#F4A261',
    icon: '🎈',
    image: 'assets/aromas_botanicos/chicle.png',
    bgNote: 'Lúdico, efervescente y alegre',
    description: 'Evoca los recuerdos más dulces con notas de fresa silvestre, plátano dulce y cereza. Llena el ambiente de sonrisas y desenfado.',
    notes: {
      top: 'Fresa Glaseada, Plátano Dulce',
      heart: 'Cereza Silvestre, Manzana Rosa',
      base: 'Azúcar Glass, Almizcle Suave'
    },
    mood: 'Diversión, creatividad y nostalgia feliz',
    space: 'Habitaciones juveniles, áreas de juego y boutiques',
    intensity: 5
  },
  {
    id: 'manzana-canela',
    name: 'Manzana Canela',
    subtitle: 'Manzana Asada & Canela',
    family: 'especiado',
    familyName: 'Especiado & Cálido',
    color: '#BC6C25',
    icon: '🍎',
    image: 'assets/aromas_botanicos/manzana_canela.png',
    bgNote: 'Acogedor, festivo y especiado',
    description: 'Manzanas horneadas con astillas de canela de Ceilán, nuez moscada y clavo de olor. El aroma definitivo del hogar acogedor.',
    notes: {
      top: 'Manzana Roja Crujiente, Ralladura de Limón',
      heart: 'Canela en Rama, Nuez Moscada, Clavo',
      base: 'Corteza de Cedro, Vainilla Especiada'
    },
    mood: 'Intimidad, festividad y hospitalidad',
    space: 'Entradas, comedores y salas de estar',
    intensity: 4
  },
  {
    id: 'coco-flower',
    name: 'Coco Flower',
    subtitle: 'Flor de Coco & Jazmín',
    family: 'floral',
    familyName: 'Floral & Delicado',
    color: '#E0A96D',
    icon: '🌸',
    image: 'assets/aromas_botanicos/coco_flower.png',
    bgNote: 'Elegante, sedoso y etéreo',
    description: 'Un bouquet refinado de flores blancas de coco, jazmín nocturno y gardenias con fondo acuático transparente. Pura sofisticación botánica.',
    notes: {
      top: 'Pétalos de Jazmín, Flor de Tiaré',
      heart: 'Flor de Coco, Gardenia Blanca',
      base: 'Almizcle de Seda, Madera Clara'
    },
    mood: 'Paz mental, armonía y elegancia pura',
    space: 'Suites principales, vestidores y spas',
    intensity: 3
  },
  {
    id: 'mokka',
    name: 'Mokka',
    subtitle: 'Café Moka & Cacao Tostado',
    family: 'especiado',
    familyName: 'Gourmand & Especiado',
    color: '#6F4E37',
    icon: '☕',
    image: 'assets/aromas_botanicos/mokka.png',
    bgNote: 'Profundo, estimulante y sofisticado',
    description: 'Granos de café arábica recién molidos mezclados con nibs de cacao amargo y crema batida. La esencia de una mañana perfecta.',
    notes: {
      top: 'Grano de Café Tostado, Cardamomo',
      heart: 'Cacao Negro, Licor de Café',
      base: 'Madera de Roble, Vainilla Bourbon'
    },
    mood: 'Inspiración, energía y placer sensorial',
    space: 'Bibliotecas, oficinas, cafeterías y salones',
    intensity: 5
  },
  {
    id: 'limon',
    name: 'Limón',
    subtitle: 'Limón Verde & Verbena',
    family: 'citrico',
    familyName: 'Cítrico & Fresco',
    color: '#A3B18A',
    icon: '🍋',
    image: 'assets/aromas_botanicos/limon.png',
    bgNote: 'Puro, efervescente y limpio',
    description: 'Limones verdes cosechados al rocío matutino junto a hojas frescas de verbena y hierbabuena. Desinfecta la sensación del aire.',
    notes: {
      top: 'Limón Verde, Lima Kaffir',
      heart: 'Hojas de Verbena, Menta Fresca',
      base: 'Cedro Blanco, Almizcle Limpio'
    },
    mood: 'Claridad, vitalidad y limpieza absoluta',
    space: 'Cocinas, baños, terrazas y pasillos',
    intensity: 4
  },
  {
    id: 'pino',
    name: 'Pino',
    subtitle: 'Pino Silvestre & Bosque',
    family: 'bosque',
    familyName: 'Amaderado & Bosque',
    color: '#2D6A4F',
    icon: '🌲',
    image: 'assets/aromas_botanicos/pino.png',
    bgNote: 'Fresco, resinoso y purificante',
    description: 'Caminar por un bosque húmedo de coníferas tras la lluvia. Acículas de pino, musgo verde y corteza balsámica que llenan los pulmones de aire puro.',
    notes: {
      top: 'Acículas de Pino, Eucalipto Azul',
      heart: 'Musgo de Roble, Enebro',
      base: 'Madera de Pino Boreal, Resina de Ámbar'
    },
    mood: 'Respiración profunda, conexión natural y paz',
    space: 'Salas de meditación, salas de estar y oficinas',
    intensity: 4
  },
  {
    id: 'lavanda',
    name: 'Lavanda',
    subtitle: 'Lavanda Francesa & Notas Herbales',
    family: 'floral',
    familyName: 'Floral & Terapéutico',
    color: '#7B68EE',
    icon: '🪻',
    image: 'assets/aromas_botanicos/lavanda.png',
    bgNote: 'Calmante, aromaterapéutico y sereno',
    description: 'Campos de lavanda en flor bajo el sol provenzal con toques de salvia y romero. El calmante natural por excelencia para la mente.',
    notes: {
      top: 'Flores de Lavanda, Hojas de Salvia',
      heart: 'Romero Silvestre, Manzanilla',
      base: 'Maderas Suaves, Almizcle Blanco'
    },
    mood: 'Inducción al sueño, relajación y antiestrés',
    space: 'Dormitorios, almohadas, áreas de yoga y descanso',
    intensity: 3
  },
  {
    id: 'frutal-mango',
    name: 'Frutal Mango',
    subtitle: 'Mango Tropical & Papaya',
    family: 'frutal',
    familyName: 'Frutal & Tropical',
    color: '#F39A59',
    icon: '🥭',
    image: 'assets/aromas_botanicos/frutal_mango.png',
    bgNote: 'Exótico, jugoso y solar',
    description: 'Pulpa dorada de mango madurado al sol con nectar de papaya, maracuyá y toques de flores tropicales. Un rayo de sol cálido y envolvente.',
    notes: {
      top: 'Mango Maduro, Papaya Dorada',
      heart: 'Maracuyá, Flor de Hibisco',
      base: 'Caña de Azúcar, Almizcle Cálido'
    },
    mood: 'Vitalidad, optimismo veraniego y frescura',
    space: 'Living, terrazas, recibidores y comedores',
    intensity: 5
  }
];

const PRODUCTS = [
  {
    id: 'home-spray-250',
    name: 'Home Spray Textil & Ambiental',
    volume: '250 ML',
    price: 12990,
    category: 'home-spray',
    categoryName: 'Home Spray',
    badge: 'Más Vendido ✦',
    image: 'assets/visuales/Home Spray/Por Aroma/h_mooka.jpg',
    altImages: [
      'assets/visuales/Home Spray/Por Aroma/h_vainilla_coco.jpg',
      'assets/visuales/Home Spray/Por Aroma/h_lavanda.jpg',
      'assets/visuales/Home Spray/Por Aroma/h_citric.jpg'
    ],
    tagline: 'Bruma instantánea de alta concentración para textiles, sábanas, cortinas y ambientes.',
    description: 'Envase de vidrio ámbar protector con gatillo pulverizador profesional. Formulado con aceites esenciales botánicos de fijación prolongada.',
    features: [
      'Vidrio ámbar reciclable de alta durabilidad',
      'Gatillo con micro-atomización fina sin manchas',
      'Apto para textiles de algodón, lino y sofás',
      'Rinde más de 1.200 pulverizaciones'
    ],
    defaultFragrance: 'mokka'
  },
  {
    id: 'mikado-50',
    name: 'Difusor de Varillas Mikado',
    volume: '50 ML',
    price: 13990,
    category: 'mikado',
    categoryName: 'Difusores Mikado',
    badge: 'Aroma Continuo ✦',
    image: 'assets/visuales/Mikado/Por Aroma/m_berries.jpg',
    altImages: [
      'assets/visuales/Mikado/Por Aroma/m_vainilla_coco.jpg',
      'assets/visuales/Mikado/Por Aroma/m_citric.jpg',
      'assets/visuales/Mikado/Por Aroma/m_mokka.jpg'
    ],
    tagline: 'Difusión pasiva homogénea y constante las 24 horas del día.',
    description: 'Frasco de vidrio ámbar compacto con juego de varillas de ratán de alta absorción que propagan el aroma de forma sutil y continua.',
    features: [
      '6 Varillas de ratán poroso premium',
      'Difusión continua durante 35 a 45 días',
      'Sin consumo eléctrico ni combustión',
      'Diseño decorativo minimalista'
    ],
    defaultFragrance: 'berries'
  },
  {
    id: 'aromatizador-15',
    name: 'Aromatizador Compacto & Auto',
    volume: '15 ML',
    price: 5490,
    category: 'aromatizador',
    categoryName: 'Aromatizador 15ml',
    badge: 'Portátil ✦',
    image: 'assets/visuales/Aromatizador/Por Aroma/a_lavanda.jpg',
    altImages: [
      'assets/visuales/Aromatizador/Por Aroma/a_vanilla_coco.jpg',
      'assets/visuales/Aromatizador/Por Aroma/a_citric.jpg'
    ],
    tagline: 'Para vehículos, vestidores, bolsos o tu rincón favorito.',
    description: 'Frasco de precisión con spray directo. Llévalo contigo a donde vayas para una recarga inmediata de bienestar sensorial.',
    features: [
      'Formato ultra portátil de bolsillo',
      'Ideal para auto, clósets y maletas',
      'Fijación instantánea',
      'Tapa protectora hermética'
    ],
    defaultFragrance: 'lavanda'
  },
  {
    id: 'recarga-250',
    name: 'Recarga Eco-Refill',
    volume: '250 ML',
    price: 7490,
    category: 'recarga',
    categoryName: 'Recargas Eco',
    badge: 'Eco-Friendly 🌱',
    image: 'assets/visuales/Recarga 250/Por Aroma/r250_sugar.jpg',
    altImages: [
      'assets/visuales/Recarga 250/Por Aroma/r250_vainilla_coco.jpg',
      'assets/visuales/Recarga 250/Por Aroma/r250_berries.jpg'
    ],
    tagline: 'Rellena tus envases favoritos y reduce la huella ambiental.',
    description: 'Botella ecológica de 250 ml con tapa dosificadora, lista para rellenar tus difusores Mikado o frascos de Home Spray.',
    features: [
      'Ahorra hasta un 25% frente al envase completo',
      'Reduce consumo de plástico y vidrio nuevo',
      'Equivale a 5 difusores de 50 ml',
      'Fórmula 100% idéntica al envase original'
    ],
    defaultFragrance: 'sugar'
  },
  {
    id: 'recarga-500',
    name: 'Recarga Familiar Maxi-Refill',
    volume: '500 ML',
    price: 11990,
    category: 'recarga',
    categoryName: 'Recargas Eco',
    badge: 'Mejor Rendimiento ⭐',
    image: 'assets/visuales/Recarga 500/Por Aroma/r500_vainilla_coco.jpg',
    altImages: [
      'assets/visuales/Recarga 500/Por Aroma/r500_berries.jpg',
      'assets/visuales/Recarga 500/Por Aroma/r500_citric.jpg'
    ],
    tagline: 'El formato más conveniente para hogares con aroma continuo.',
    description: 'Formato familiar de 500 ml para rellenar múltiples frascos del hogar. Máxima economía y duración.',
    features: [
      'Rinde 10 recargas de Mikado o 2 Home Sprays completos',
      'Máximo ahorro por mililitro',
      'Boquilla antigoteo para fácil trasvasije',
      'Conserva intacta la concentración olfativa'
    ],
    defaultFragrance: 'vainilla-coco'
  }
];

// Mapa Oficial Exhaustivo de 65 Imágenes Reales por Formato y Aroma
const PRODUCT_AROMA_IMAGES = {
  'home-spray-250': {
    'vainilla-coco': 'assets/visuales/Home Spray/Por Aroma/h_vainilla_coco.jpg',
    'citric': 'assets/visuales/Home Spray/Por Aroma/h_citric.jpg',
    'berries': 'assets/visuales/Home Spray/Por Aroma/h_berries.jpg',
    'coco-nut': 'assets/visuales/Home Spray/Por Aroma/h_coco_nut.jpg',
    'sugar': 'assets/visuales/Home Spray/Por Aroma/h_sugar.jpg',
    'chicle': 'assets/visuales/Home Spray/Por Aroma/h_chicle.jpg',
    'manzana-canela': 'assets/visuales/Home Spray/Por Aroma/h_manzana_canela.jpg',
    'coco-flower': 'assets/visuales/Home Spray/Por Aroma/h_coco_flower.jpg',
    'mokka': 'assets/visuales/Home Spray/Por Aroma/h_mooka.jpg',
    'limon': 'assets/visuales/Home Spray/Por Aroma/h_limon.jpg',
    'pino': 'assets/visuales/Home Spray/Por Aroma/h_pino.jpg',
    'lavanda': 'assets/visuales/Home Spray/Por Aroma/h_lavanda.jpg',
    'frutal-mango': 'assets/visuales/Home Spray/Por Aroma/h_frutal_mango.jpg'
  },
  'mikado-50': {
    'vainilla-coco': 'assets/visuales/Mikado/Por Aroma/m_vainilla_coco.jpg',
    'citric': 'assets/visuales/Mikado/Por Aroma/m_citric.jpg',
    'berries': 'assets/visuales/Mikado/Por Aroma/m_berries.jpg',
    'coco-nut': 'assets/visuales/Mikado/Por Aroma/m_coconut.jpg',
    'sugar': 'assets/visuales/Mikado/Por Aroma/m_sugar.jpg',
    'chicle': 'assets/visuales/Mikado/Por Aroma/m_chicle.jpg',
    'manzana-canela': 'assets/visuales/Mikado/Por Aroma/m_manzana_canela.jpg',
    'coco-flower': 'assets/visuales/Mikado/Por Aroma/m_coco_flower.jpg',
    'mokka': 'assets/visuales/Mikado/Por Aroma/m_mokka.jpg',
    'limon': 'assets/visuales/Mikado/Por Aroma/m_limon.jpg',
    'pino': 'assets/visuales/Mikado/Por Aroma/m_pino.jpg',
    'lavanda': 'assets/visuales/Mikado/Por Aroma/m_lavanda.jpg',
    'frutal-mango': 'assets/visuales/Mikado/Por Aroma/m_frutal_mango.jpg'
  },
  'aromatizador-15': {
    'vainilla-coco': 'assets/visuales/Aromatizador/Por Aroma/a_vanilla_coco.jpg',
    'citric': 'assets/visuales/Aromatizador/Por Aroma/a_citric.jpg',
    'berries': 'assets/visuales/Aromatizador/Por Aroma/a_berries.jpg',
    'coco-nut': 'assets/visuales/Aromatizador/Por Aroma/a_coco_nut.jpg',
    'sugar': 'assets/visuales/Aromatizador/Por Aroma/a_sugar.jpg',
    'chicle': 'assets/visuales/Aromatizador/Por Aroma/a_chicle.jpg',
    'manzana-canela': 'assets/visuales/Aromatizador/Por Aroma/a_manzana_canela.jpg',
    'coco-flower': 'assets/visuales/Aromatizador/Por Aroma/a_coco_flower.jpg',
    'mokka': 'assets/visuales/Aromatizador/Por Aroma/a_mokka.jpg',
    'limon': 'assets/visuales/Aromatizador/Por Aroma/a_limon.jpg',
    'pino': 'assets/visuales/Aromatizador/Por Aroma/a_pino.jpg',
    'lavanda': 'assets/visuales/Aromatizador/Por Aroma/a_lavanda.jpg',
    'frutal-mango': 'assets/visuales/Aromatizador/Por Aroma/a_frutal_mango.jpg'
  },
  'recarga-250': {
    'vainilla-coco': 'assets/visuales/Recarga 250/Por Aroma/r250_vainilla_coco.jpg',
    'citric': 'assets/visuales/Recarga 250/Por Aroma/r250_citric.jpg',
    'berries': 'assets/visuales/Recarga 250/Por Aroma/r250_berries.jpg',
    'coco-nut': 'assets/visuales/Recarga 250/Por Aroma/r250_coco_nut.jpg',
    'sugar': 'assets/visuales/Recarga 250/Por Aroma/r250_sugar.jpg',
    'chicle': 'assets/visuales/Recarga 250/Por Aroma/r250_chicle.jpg',
    'manzana-canela': 'assets/visuales/Recarga 250/Por Aroma/r250_manzana_canela.jpg',
    'coco-flower': 'assets/visuales/Recarga 250/Por Aroma/r250_coco_flower.jpg',
    'mokka': 'assets/visuales/Recarga 250/Por Aroma/r250_mokka.jpg',
    'limon': 'assets/visuales/Recarga 250/Por Aroma/r250_limon.jpg',
    'pino': 'assets/visuales/Recarga 250/Por Aroma/r250_pino.jpg',
    'lavanda': 'assets/visuales/Recarga 250/Por Aroma/r250_lavanda.jpg',
    'frutal-mango': 'assets/visuales/Recarga 250/Por Aroma/r250_frutal_mango.jpg'
  },
  'recarga-500': {
    'vainilla-coco': 'assets/visuales/Recarga 500/Por Aroma/r500_vainilla_coco.jpg',
    'citric': 'assets/visuales/Recarga 500/Por Aroma/r500_citric.jpg',
    'berries': 'assets/visuales/Recarga 500/Por Aroma/r500_berries.jpg',
    'coco-nut': 'assets/visuales/Recarga 500/Por Aroma/r500_coco_nut.jpg',
    'sugar': 'assets/visuales/Recarga 500/Por Aroma/r500_sugar.jpg',
    'chicle': 'assets/visuales/Recarga 500/Por Aroma/r500_chicle.jpg',
    'manzana-canela': 'assets/visuales/Recarga 500/Por Aroma/r500_manzana_canela.jpg',
    'coco-flower': 'assets/visuales/Recarga 500/Por Aroma/r500_coco_flower.jpg',
    'mokka': 'assets/visuales/Recarga 500/Por Aroma/r500_mokka.jpg',
    'limon': 'assets/visuales/Recarga 500/Por Aroma/r500_limon.jpg',
    'pino': 'assets/visuales/Recarga 500/Por Aroma/r500_pino.jpg',
    'lavanda': 'assets/visuales/Recarga 500/Por Aroma/r500_lavanda.jpg',
    'frutal-mango': 'assets/visuales/Recarga 500/Por Aroma/r500_frutal_mango.jpg'
  }
};

const PACKS = [
  {
    id: 'set-ritual-completo',
    name: 'Set Ritual Botánico Jeshia',
    price: 26000,
    badge: 'Set Exclusivo 🎁',
    image: 'assets/visuales/Familia.png',
    tagline: 'Home Spray 250ml + Mikado 50ml + Recarga 250ml en caja de regalo.',
    description: 'La experiencia completa para perfumar tu hogar con coherencia olfativa. Elige tu aroma favorito o combina fragancias complementarias.',
    includes: ['1x Home Spray 250ml', '1x Difusor Mikado 50ml', '1x Recarga Eco 250ml', 'Caja de presentación con lazo botánico']
  }
];

const REVIEWS = [
  {
    author: 'Camila Valenzuela',
    city: 'Las Condes, Santiago',
    aroma: 'Mokka',
    rating: 5,
    date: 'Hace 3 días',
    comment: 'El Home Spray de Mokka es de otro planeta. Entrar a mi departamento y que huela a cafetería de especialidad con notas tostadas es una delicia. La fijación dura horas.'
  },
  {
    author: 'Ignacio Morales',
    city: 'Viña del Mar',
    aroma: 'Pino',
    rating: 5,
    date: 'Hace 1 semana',
    comment: 'Buscaba un aroma que no fuera el típico pino químico, y este es literalmente como caminar por un bosque andino después de la lluvia. Muy elegante.'
  },
  {
    author: 'Francisca Soto',
    city: 'Providencia',
    aroma: 'Vainilla Coco & Berries',
    rating: 5,
    date: 'Hace 2 semanas',
    comment: 'Compré el Mikado de Berries y la Recarga de Vainilla Coco. El packaging en vidrio ámbar es precioso y los envíos por WhatsApp fueron súper rápidos y amables.'
  }
];

const MOOD_CATEGORIES = [
  {
    id: 'calm',
    title: 'Dormir & Desconectar',
    icon: '🌙',
    color: '#7B68EE',
    desc: 'Bajar los niveles de cortisol, apaciguar la mente e inducir un sueño profundo y reparador.',
    ritual: 'Rocía tus almohadas y sábanas con Home Spray 15 minutos antes de acostarte.',
    fragrances: ['lavanda', 'coco-flower', 'pino']
  },
  {
    id: 'focus',
    title: 'Foco & Productividad',
    icon: '⚡',
    color: '#E9C46A',
    desc: 'Estimular la lucidez mental, despejar el agotamiento y elevar la concentración en horas de trabajo.',
    ritual: 'Coloca un Mikado en tu escritorio o pulveriza el aire al iniciar tu jornada laboral.',
    fragrances: ['citric', 'limon', 'mokka']
  },
  {
    id: 'cozy',
    title: 'Calidez & Abrazo de Hogar',
    icon: '☕',
    color: '#BC6C25',
    desc: 'Sensación envolvente de confort, nostalgia dulce y hospitalidad para reuniones y tardes frías.',
    ritual: 'Aplica en cortinas y sofás para impregnar la tela de una estela dulce y duradera.',
    fragrances: ['vainilla-coco', 'manzana-canela', 'sugar', 'coco-nut']
  },
  {
    id: 'energy',
    title: 'Alegría & Optimismo',
    icon: '🍓',
    color: '#E76F51',
    desc: 'Vibraciones chispeantes que despiertan el buen humor, la creatividad y la vitalidad veraniega.',
    ritual: 'Ideal para pasillos, salas comunes y vestidores al comenzar el día.',
    fragrances: ['berries', 'frutal-mango', 'chicle']
  }
];

const ROOM_GUIDELINES = [
  {
    id: 'living',
    name: 'Living & Salón Principal',
    icon: '🛋️',
    size: '20 - 45 m²',
    recommendedFormat: 'Duo Home Spray 250ml + Mikado 50ml',
    recommendedAromas: ['mokka', 'vainilla-coco', 'berries', 'manzana-canela'],
    tip: 'Coloca el Mikado en un mueble central sin sol directo y usa el Home Spray en cojines y cortinas antes de recibir visitas.'
  },
  {
    id: 'bedroom',
    name: 'Dormitorio & Suite',
    icon: '🛏️',
    size: '12 - 20 m²',
    recommendedFormat: 'Home Spray Textil 250ml',
    recommendedAromas: ['lavanda', 'coco-flower', 'vainilla-coco'],
    tip: 'Vaporiza sobre el embozo de las sábanas a 30 cm de distancia. La fórmula botánica no mancha el lino ni el algodón.'
  },
  {
    id: 'office',
    name: 'Oficina & Home Office',
    icon: '💼',
    size: '8 - 15 m²',
    recommendedFormat: 'Difusor Mikado 50ml',
    recommendedAromas: ['citric', 'limon', 'mokka', 'pino'],
    tip: 'Las notas cítricas y resinosas purifican el aire cerrado y reducen la fatiga visual.'
  },
  {
    id: 'kitchen',
    name: 'Cocina & Comedor',
    icon: '🍋',
    size: '10 - 25 m²',
    recommendedFormat: 'Home Spray 250ml',
    recommendedAromas: ['limon', 'citric', 'manzana-canela'],
    tip: 'Neutraliza olores de cocción al instante aportando una atmósfera fresca y pulcra.'
  },
  {
    id: 'car',
    name: 'Vehículo & Vestidor',
    icon: '🚗',
    size: '2 - 6 m²',
    recommendedFormat: 'Aromatizador Compacto 15ml',
    recommendedAromas: ['lavanda', 'citric', 'coco-nut'],
    tip: 'Aplica 2 toques sobre las alfombrillas del auto para una fragancia constante sin saturar la cabina.'
  }
];

const WHOLESALE_TIERS = [
  {
    tier: 'Tier 1',
    qty: '20 a 49 unidades',
    discount: '15% Descuento',
    idealFor: 'Recuerdos de Matrimonio, Bautizos y Regalos Corporativos medianos'
  },
  {
    tier: 'Tier 2',
    qty: '50 a 99 unidades',
    discount: '25% Descuento',
    idealFor: 'Hoteles Boutique, Spas, Salones de Belleza y Regalos de Empresa'
  },
  {
    tier: 'Tier 3',
    qty: '100+ unidades',
    discount: '35% Descuento + Etiqueta Personalizada',
    idealFor: 'Marcas mayoristas, Cadenas y Eventos Masivos'
  }
];

// Helper para obtener aroma por ID
function getFragranceById(id) {
  return FRAGRANCES.find(f => f.id === id) || FRAGRANCES[0];
}

// Helper para obtener producto por ID
function getProductById(id) {
  return PRODUCTS.find(p => p.id === id) || PRODUCTS[0];
}

// Helper para obtener la fotografía real de un producto según su formato y fragancia
function getProductAromaImage(productId, fragranceId) {
  if (PRODUCT_AROMA_IMAGES[productId] && PRODUCT_AROMA_IMAGES[productId][fragranceId]) {
    return PRODUCT_AROMA_IMAGES[productId][fragranceId];
  }
  const prod = getProductById(productId);
  return prod ? prod.image : 'assets/visuales/Familia.png';
}

// Helper para obtener la fotografía real del aroma (por defecto en formato Home Spray o el solicitado)
function getFragranceVisualImage(fragranceId, formatId = 'home-spray-250') {
  return getProductAromaImage(formatId, fragranceId);
}

// Formateador de moneda chilena
function formatCLP(amount) {
  return '$' + amount.toLocaleString('es-CL');
}

