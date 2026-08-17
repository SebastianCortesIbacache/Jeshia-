/**
 * Jeshia — Lógica Interactiva Principal
 * Control del Catálogo, Filtros de Fragancias, Carrito Drawer, WhatsApp Checkout
 * y Módulos Avanzados (Box Builder, Mood Wheel, Room Guide, B2B, Eco Calc y Dark Mode)
 */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initHeader();
  initTicker();
  initCatalog();
  initCatalogSearch();
  initUniverse();
  initComparator();
  initQuiz();
  initBoxBuilder();
  initMoodSection();
  initRoomSection();
  initB2BSection();
  initEcoCalc();
  initCart();
  initGiftDedication();
  initModals();
  initFloatingWhatsApp();
});

/* ==========================================================================
   1. THEME SWITCHER (MODO DÍA / NOCHE OBSIDIAN)
   ========================================================================== */
function initTheme() {
  const savedTheme = localStorage.getItem('jeshia_theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeBtn(savedTheme);

  const themeBtn = document.getElementById('themeToggleBtn');
  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme') || 'light';
      const next = current === 'light' ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('jeshia_theme', next);
      updateThemeBtn(next);
      showToast(`✦ Modo ${next === 'dark' ? 'Noche Obsidian 🌙' : 'Día Lino ☀️'} activado`);
    });
  }
}

function updateThemeBtn(theme) {
  const themeBtn = document.getElementById('themeToggleBtn');
  if (themeBtn) {
    themeBtn.innerHTML = theme === 'dark' ? '☀️' : '🌙';
    themeBtn.title = theme === 'dark' ? 'Cambiar a Modo Día' : 'Cambiar a Modo Noche';
  }
}

/* ==========================================================================
   2. HEADER & NAVEGACIÓN
   ========================================================================== */
function initHeader() {
  const header = document.querySelector('.site-header');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 40) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });

  const mobileBtn = document.querySelector('.mobile-menu-btn');
  const navMenu = document.querySelector('.nav-menu');
  if (mobileBtn && navMenu) {
    mobileBtn.addEventListener('click', () => {
      const isVisible = navMenu.style.display === 'flex';
      navMenu.style.display = isVisible ? 'none' : 'flex';
      if (!isVisible) {
        navMenu.style.flexDirection = 'column';
        navMenu.style.position = 'absolute';
        navMenu.style.top = '80px';
        navMenu.style.left = '0';
        navMenu.style.right = '0';
        navMenu.style.background = 'var(--bg-surface)';
        navMenu.style.zIndex = '999';
        navMenu.style.padding = '24px';
        navMenu.style.boxShadow = 'var(--shadow-lg)';
        navMenu.style.borderBottom = '1px solid var(--brand-line)';
      }
    });
  }
}

/* ==========================================================================
   3. AROMA TICKER TRACK
   ========================================================================== */
function initTicker() {
  const track = document.getElementById('tickerTrack');
  if (!track) return;

  const all = [...FRAGRANCES, ...FRAGRANCES];
  track.innerHTML = all.map(f => `
    <div class="ticker-item">
      <span>${f.icon}</span> ${f.name} · <em>${f.familyName}</em>
    </div>
  `).join('');
}

/* ==========================================================================
   4. CATÁLOGO DE PRODUCTOS INTERACTIVO & BÚSQUEDA EN TIEMPO REAL
   ========================================================================== */
let currentCategory = 'all';
let catalogSearchTerm = '';

function initCatalog() {
  const tabs = document.querySelectorAll('.cat-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      currentCategory = tab.dataset.category;
      renderProducts();
    });
  });

  renderProducts();
}

function initCatalogSearch() {
  const searchInput = document.getElementById('catalogSearchInput');
  const clearBtn = document.getElementById('clearSearchBtn');

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      catalogSearchTerm = e.target.value.trim().toLowerCase();
      if (clearBtn) {
        clearBtn.style.display = catalogSearchTerm.length > 0 ? 'flex' : 'none';
      }
      renderProducts();
    });
  }

  if (clearBtn) {
    clearBtn.addEventListener('click', clearCatalogSearch);
  }
}

function clearCatalogSearch() {
  const searchInput = document.getElementById('catalogSearchInput');
  const clearBtn = document.getElementById('clearSearchBtn');
  if (searchInput) searchInput.value = '';
  if (clearBtn) clearBtn.style.display = 'none';
  catalogSearchTerm = '';
  renderProducts();
}

function renderProducts() {
  const grid = document.getElementById('productsGrid');
  const noResults = document.getElementById('noSearchResults');
  if (!grid) return;

  let filtered = currentCategory === 'all' 
    ? PRODUCTS 
    : PRODUCTS.filter(p => p.category === currentCategory);

  // Filtrado por término de búsqueda en tiempo real
  let matchedFragId = null;
  if (catalogSearchTerm) {
    // Buscar si alguna fragancia coincide con el término
    const matchingFrags = FRAGRANCES.filter(f => {
      const q = catalogSearchTerm;
      return f.name.toLowerCase().includes(q) ||
             f.subtitle.toLowerCase().includes(q) ||
             f.familyName.toLowerCase().includes(q) ||
             f.description.toLowerCase().includes(q) ||
             f.notes.top.toLowerCase().includes(q) ||
             f.notes.heart.toLowerCase().includes(q) ||
             f.notes.base.toLowerCase().includes(q) ||
             f.mood.toLowerCase().includes(q) ||
             f.space.toLowerCase().includes(q);
    });

    if (matchingFrags.length > 0) {
      matchedFragId = matchingFrags[0].id;
    }

    filtered = filtered.filter(prod => {
      const matchProd = prod.name.toLowerCase().includes(catalogSearchTerm) ||
                        prod.tagline.toLowerCase().includes(catalogSearchTerm) ||
                        prod.categoryName.toLowerCase().includes(catalogSearchTerm);
      return matchProd || matchingFrags.length > 0;
    });
  }

  if (filtered.length === 0) {
    grid.style.display = 'none';
    if (noResults) noResults.style.display = 'block';
    return;
  }

  grid.style.display = 'grid';
  if (noResults) noResults.style.display = 'none';

  grid.innerHTML = filtered.map(prod => {
    const selectedFrag = matchedFragId || prod.defaultFragrance;
    const initialImg = getProductAromaImage(prod.id, selectedFrag);
    const scentOptions = FRAGRANCES.map(f => `
      <option value="${f.id}" ${f.id === selectedFrag ? 'selected' : ''}>
        ${f.icon} ${f.name} (${f.subtitle})
      </option>
    `).join('');

    return `
      <article class="product-card" data-product-id="${prod.id}">
        <span class="card-badge">${prod.badge}</span>
        <div class="card-img-container">
          <img src="${initialImg}" alt="${prod.name}" id="img-${prod.id}" loading="lazy">
        </div>
        <div class="card-body">
          <span class="card-volume">${prod.volume} · ${prod.categoryName}</span>
          <h3 class="card-title">${prod.name}</h3>
          <p class="card-tagline">${prod.tagline}</p>
          
          <div class="scent-picker">
            <label for="select-${prod.id}">Seleccionar Fragancia:</label>
            <div class="scent-select-wrap">
              <select class="scent-select" id="select-${prod.id}" onchange="changeProductCardScent('${prod.id}', this.value)">
                ${scentOptions}
              </select>
            </div>
          </div>

          <div class="card-footer">
            <span class="card-price">${formatCLP(prod.price)}</span>
            <button class="btn-add-cart" onclick="addProductToCart('${prod.id}')">
              <span>🛒</span> Agregar
            </button>
          </div>
          <button class="btn-quick-view" onclick="openProductQuickView('${prod.id}')">
            ✦ Ver Ficha & Pirámide Olfativa
          </button>
        </div>
      </article>
    `;
  }).join('');
}

function changeProductCardScent(productId, fragranceId) {
  const img = document.getElementById(`img-${productId}`);
  if (img) {
    img.src = getProductAromaImage(productId, fragranceId);
  }
}

/* ==========================================================================
   5. UNIVERSO DE 13 FRAGANCIAS
   ========================================================================== */
let currentFragFamily = 'all';

function initUniverse() {
  const filterBtns = document.querySelectorAll('.frag-filter-btn');
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentFragFamily = btn.dataset.family;
      renderUniverse();
    });
  });

  renderUniverse();
}

function renderUniverse() {
  const grid = document.getElementById('fragranceGrid');
  if (!grid) return;

  const filtered = currentFragFamily === 'all'
    ? FRAGRANCES
    : FRAGRANCES.filter(f => f.family === currentFragFamily);

  grid.innerHTML = filtered.map(frag => {
    const fragVisual = getProductAromaImage('home-spray-250', frag.id);
    return `
      <div class="fragrance-card" style="--frag-accent: ${frag.color}" onclick="openFragranceModal('${frag.id}')">
        <div class="frag-art-wrap">
          <img src="${fragVisual}" alt="${frag.name}" loading="lazy">
        </div>
        <span class="frag-family-tag">${frag.icon} ${frag.familyName}</span>
        <h3 class="frag-name">${frag.name}</h3>
        <p class="frag-subtitle">${frag.subtitle}</p>
        <p class="frag-desc">${frag.description}</p>
        <div class="frag-notes-pill">
          <b>Pirámide Olfativa:</b>
          <span>Salida: ${frag.notes.top}</span>
        </div>
      </div>
    `;
  }).join('');
}

/* ==========================================================================
   5B. COMPARADOR INTERACTIVO DE AROMAS BOTÁNICOS (LADO A LADO)
   ========================================================================== */
function initComparator() {
  const selectA = document.getElementById('compareFragA');
  const selectB = document.getElementById('compareFragB');
  if (!selectA || !selectB) return;

  const optionsA = FRAGRANCES.map(f => `
    <option value="${f.id}" ${f.id === 'mokka' ? 'selected' : ''}>
      ${f.icon} ${f.name} (${f.familyName})
    </option>
  `).join('');

  const optionsB = FRAGRANCES.map(f => `
    <option value="${f.id}" ${f.id === 'vainilla-coco' ? 'selected' : ''}>
      ${f.icon} ${f.name} (${f.familyName})
    </option>
  `).join('');

  selectA.innerHTML = optionsA;
  selectB.innerHTML = optionsB;

  selectA.addEventListener('change', renderComparison);
  selectB.addEventListener('change', renderComparison);

  renderComparison();
}

function renderComparison() {
  const selectA = document.getElementById('compareFragA');
  const selectB = document.getElementById('compareFragB');
  const container = document.getElementById('compareCardsGrid');
  if (!selectA || !selectB || !container) return;

  const fragA = getFragranceById(selectA.value);
  const fragB = getFragranceById(selectB.value);

  container.innerHTML = `
    ${renderCompareCard(fragA)}
    ${renderCompareCard(fragB)}
  `;
}

function renderCompareCard(frag) {
  const homeSprayPrice = PRODUCTS.find(p => p.id === 'home-spray-250')?.price || 12990;
  const fragPhoto = getProductAromaImage('home-spray-250', frag.id);
  return `
    <div class="compare-card" style="--compare-color: ${frag.color}">
      <div class="compare-card-header">
        <div class="compare-art-wrap">
          <img src="${fragPhoto}" alt="${frag.name}" loading="lazy">
        </div>
        <div class="compare-title-area">
          <span class="frag-family-tag">${frag.icon} ${frag.familyName}</span>
          <h3>${frag.name}</h3>
          <span class="compare-sub">${frag.subtitle}</span>
        </div>
      </div>

      <div class="compare-notes-table">
        <div class="compare-note-row">
          <b>Salida:</b>
          <span>${frag.notes.top}</span>
        </div>
        <div class="compare-note-row">
          <b>Corazón:</b>
          <span>${frag.notes.heart}</span>
        </div>
        <div class="compare-note-row">
          <b>Fondo:</b>
          <span>${frag.notes.base}</span>
        </div>
      </div>

      <div class="compare-meta-pill">
        <p>✨ <b>Sensación:</b> ${frag.mood}</p>
        <p>🏠 <b>Espacio ideal:</b> ${frag.space}</p>
        <p style="margin-top: 6px; font-style: italic; font-size: 0.8rem;">"${frag.description}"</p>
      </div>

      <button class="btn-primary compare-add-btn" onclick="quickAddFragranceToCart('${frag.id}')">
        <span>🛒</span> Pedir Home Spray en ${frag.name} (${formatCLP(homeSprayPrice)})
      </button>
    </div>
  `;
}

/* ==========================================================================
   6. TEST INTERACTIVO "DESCUBRE TU AROMA"
   ========================================================================== */
let quizAnswers = { vibe: 'calm', space: 'living', intensity: 'medium' };

function initQuiz() {
  const optionBtns = document.querySelectorAll('.quiz-btn');
  optionBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      const step = this.closest('.quiz-step');
      const stepNum = parseInt(step.dataset.step, 10);
      const key = this.dataset.key;
      const value = this.dataset.val;

      quizAnswers[key] = value;

      step.querySelectorAll('.quiz-btn').forEach(b => b.classList.remove('selected'));
      this.classList.add('selected');

      setTimeout(() => {
        if (stepNum < 3) {
          showQuizStep(stepNum + 1);
        } else {
          calculateQuizResult();
        }
      }, 250);
    });
  });
}

function showQuizStep(stepNum) {
  document.querySelectorAll('.quiz-step').forEach(s => s.classList.remove('active'));
  const target = document.querySelector(`.quiz-step[data-step="${stepNum}"]`);
  if (target) target.classList.add('active');
}

function restartQuiz() {
  showQuizStep(1);
  document.querySelectorAll('.quiz-btn').forEach(b => b.classList.remove('selected'));
}

function calculateQuizResult() {
  let matchedId = 'vainilla-coco';

  if (quizAnswers.vibe === 'energy') {
    matchedId = quizAnswers.space === 'kitchen' ? 'citric' : 'limon';
  } else if (quizAnswers.vibe === 'cozy') {
    matchedId = quizAnswers.space === 'office' ? 'mokka' : 'manzana-canela';
  } else if (quizAnswers.vibe === 'calm') {
    matchedId = quizAnswers.space === 'bedroom' ? 'lavanda' : 'pino';
  } else if (quizAnswers.vibe === 'sweet') {
    matchedId = quizAnswers.space === 'living' ? 'berries' : 'sugar';
  }

  const frag = getFragranceById(matchedId);
  const quizPhoto = getProductAromaImage('home-spray-250', frag.id);
  const container = document.getElementById('quizResultBox');

  if (container) {
    container.innerHTML = `
      <div class="quiz-result-art">
        <img src="${quizPhoto}" alt="${frag.name}" style="max-width: 90%; max-height: 90%; object-fit: contain;">
      </div>
      <div>
        <span class="card-volume">${frag.icon} ${frag.familyName}</span>
        <h3 class="font-serif" style="font-size: 1.8rem; color: var(--brand-forest-dark); margin-bottom: 6px;">
          ${frag.name}
        </h3>
        <p style="font-size: 0.92rem; color: var(--text-muted); margin-bottom: 12px;">
          ${frag.description}
        </p>
        <p style="font-size: 0.85rem; font-weight: 600; color: var(--brand-terracotta); margin-bottom: 20px;">
          ✦ Ideal para: ${frag.space} · Estado: ${frag.mood}
        </p>
        <div style="display: flex; gap: 12px; flex-wrap: wrap;">
          <button class="btn-primary" onclick="quickAddFragranceToCart('${frag.id}')" style="padding: 12px 24px; font-size: 0.85rem;">
            🛒 Pedir Home Spray en ${frag.name}
          </button>
          <button class="btn-outline" onclick="restartQuiz()" style="padding: 11px 20px; font-size: 0.85rem;">
            ↻ Repetir Test
          </button>
        </div>
      </div>
    `;
  }

  showQuizStep(4);
}

function quickAddFragranceToCart(fragranceId) {
  const homeSpray = PRODUCTS.find(p => p.id === 'home-spray-250') || PRODUCTS[0];
  addToCart(homeSpray.id, fragranceId, 1);
  openCartDrawer();
}

/* ==========================================================================
   7. CREADOR DE SETS PERSONALIZADOS (CUSTOM GIFT BOX BUILDER)
   ========================================================================== */
let boxConfig = {
  format: 'duo-ritual', // duo-ritual, trio-full, solo-spray, solo-mikado
  fragrance1: 'mokka',
  fragrance2: 'berries',
  addon: 'none' // none, mini-auto, eco-250
};

const BOX_FORMATS = {
  'duo-ritual': {
    name: 'Dúo Ritual Botánico (Home Spray 250ml + Mikado 50ml)',
    originalPrice: 20500,
    discountPrice: 17400,
    discountBadge: '15% Descuento Set 🎁',
    slots: 2
  },
  'trio-full': {
    name: 'Trío Esencial (Home Spray + Mikado + Recarga 250ml)',
    originalPrice: 29500,
    discountPrice: 23600,
    discountBadge: '20% Descuento Set 🎁',
    slots: 2
  },
  'solo-spray': {
    name: 'Set Home Spray 250ml + Caja Regalo',
    originalPrice: 12000,
    discountPrice: 12000,
    discountBadge: 'Edición Regalo 🎀',
    slots: 1
  }
};

function initBoxBuilder() {
  const formatBtns = document.querySelectorAll('.box-format-btn');
  formatBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      formatBtns.forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      boxConfig.format = btn.dataset.format;
      updateBoxSummary();
    });
  });

  const fragSelect1 = document.getElementById('boxFrag1');
  const fragSelect2 = document.getElementById('boxFrag2');
  const addonSelect = document.getElementById('boxAddon');

  if (fragSelect1) {
    fragSelect1.innerHTML = FRAGRANCES.map(f => `<option value="${f.id}">${f.icon} ${f.name} (${f.subtitle})</option>`).join('');
    fragSelect1.value = boxConfig.fragrance1;
    fragSelect1.addEventListener('change', () => { boxConfig.fragrance1 = fragSelect1.value; updateBoxSummary(); });
  }

  if (fragSelect2) {
    fragSelect2.innerHTML = FRAGRANCES.map(f => `<option value="${f.id}">${f.icon} ${f.name} (${f.subtitle})</option>`).join('');
    fragSelect2.value = boxConfig.fragrance2;
    fragSelect2.addEventListener('change', () => { boxConfig.fragrance2 = fragSelect2.value; updateBoxSummary(); });
  }

  if (addonSelect) {
    addonSelect.addEventListener('change', () => { boxConfig.addon = addonSelect.value; updateBoxSummary(); });
  }

  updateBoxSummary();
}

function updateBoxSummary() {
  const formatData = BOX_FORMATS[boxConfig.format] || BOX_FORMATS['duo-ritual'];
  const frag1 = getFragranceById(boxConfig.fragrance1);
  const frag2 = getFragranceById(boxConfig.fragrance2);

  let addonPrice = 0;
  let addonName = '';
  if (boxConfig.addon === 'mini-auto') {
    addonPrice = 3500;
    addonName = ' + Aromatizador Auto 15ml';
  } else if (boxConfig.addon === 'eco-250') {
    addonPrice = 7500;
    addonName = ' + Recarga Eco 250ml';
  }

  const finalTotal = formatData.discountPrice + addonPrice;
  const originalTotal = formatData.originalPrice + (addonPrice > 0 ? addonPrice + 1000 : 0);

  const titleEl = document.getElementById('boxSummaryTitle');
  const itemsEl = document.getElementById('boxSummaryItems');
  const discountBadgeEl = document.getElementById('boxDiscountBadge');
  const origPriceEl = document.getElementById('boxOriginalPrice');
  const finalPriceEl = document.getElementById('boxFinalPrice');

  if (titleEl) titleEl.textContent = formatData.name;
  if (discountBadgeEl) discountBadgeEl.textContent = formatData.discountBadge;
  if (origPriceEl) origPriceEl.textContent = formatCLP(originalTotal);
  if (finalPriceEl) finalPriceEl.textContent = formatCLP(finalTotal);

  if (itemsEl) {
    itemsEl.innerHTML = `
      <p>• <b>Fragancia 1:</b> ${frag1.icon} ${frag1.name}</p>
      ${formatData.slots > 1 ? `<p>• <b>Fragancia 2:</b> ${frag2.icon} ${frag2.name}</p>` : ''}
      ${addonName ? `<p>• <b>Extra:</b> ${addonName}</p>` : ''}
      <p>• <b>Empaque:</b> Caja botánica con lazo de lino y viruta protectora ✨</p>
    `;
  }
}

function addCustomBoxToCart() {
  const formatData = BOX_FORMATS[boxConfig.format] || BOX_FORMATS['duo-ritual'];
  const frag1 = getFragranceById(boxConfig.fragrance1);
  const frag2 = getFragranceById(boxConfig.fragrance2);

  let addonPrice = 0;
  let addonTxt = '';
  if (boxConfig.addon === 'mini-auto') { addonPrice = 3500; addonTxt = ' + Aromatizador 15ml'; }
  else if (boxConfig.addon === 'eco-250') { addonPrice = 7500; addonTxt = ' + Recarga 250ml'; }

  const boxPrice = formatData.discountPrice + addonPrice;
  const customName = `Set Personalizado: ${formatData.name}${addonTxt}`;
  const customFragDesc = formatData.slots > 1 ? `${frag1.name} & ${frag2.name}` : frag1.name;

  cart.push({
    productId: 'custom-box-' + Date.now(),
    fragranceId: boxConfig.fragrance1,
    name: customName,
    volume: 'Set de Regalo',
    price: boxPrice,
    image: 'assets/visuales/Familia.png',
    fragranceName: customFragDesc,
    fragranceIcon: '🎁',
    qty: 1
  });

  saveCart();
  showToast(`🎁 ¡Set de Regalo personalizado añadido al carrito!`);
  openCartDrawer();
}

/* ==========================================================================
   8. NEURO-AROMATERAPIA (MOOD SCENT WHEEL)
   ========================================================================== */
function initMoodSection() {
  const tabsContainer = document.getElementById('moodTabsContainer');
  const showcaseContainer = document.getElementById('moodShowcaseContainer');
  if (!tabsContainer || !showcaseContainer) return;

  tabsContainer.innerHTML = MOOD_CATEGORIES.map((m, i) => `
    <button class="mood-tab ${i === 0 ? 'active' : ''}" data-mood-id="${m.id}" style="--mood-color: ${m.color}">
      <span>${m.icon}</span> ${m.title}
    </button>
  `).join('');

  const tabs = tabsContainer.querySelectorAll('.mood-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      renderMoodShowcase(tab.dataset.moodId);
    });
  });

  renderMoodShowcase(MOOD_CATEGORIES[0].id);
}

function renderMoodShowcase(moodId) {
  const mood = MOOD_CATEGORIES.find(m => m.id === moodId) || MOOD_CATEGORIES[0];
  const container = document.getElementById('moodShowcaseContainer');
  if (!container) return;

  const matchedFrags = mood.fragrances.map(id => getFragranceById(id));

  container.innerHTML = `
    <div class="mood-showcase-card">
      <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
        <span style="font-size: 2.2rem;">${mood.icon}</span>
        <div>
          <h3 class="font-serif" style="font-size: 1.8rem; color: #fff;">${mood.title}</h3>
          <p style="font-size: 0.95rem; color: var(--text-light);">${mood.desc}</p>
        </div>
      </div>

      <div class="mood-ritual-box" style="border-left-color: ${mood.color};">
        <h4 style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.1em; color: ${mood.color}; margin-bottom: 6px;">
          ✦ Ritual Recomendado de Aromaterapia
        </h4>
        <p style="font-size: 0.92rem; color: #FAF8F5;">${mood.ritual}</p>
      </div>

      <h4 style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-light); margin-top: 24px;">
        Fragancias con este efecto:
      </h4>

      <div class="mood-frag-cards">
        ${matchedFrags.map(f => {
          const fragImg = getProductAromaImage('home-spray-250', f.id);
          return `
            <div class="mood-frag-item" onclick="openFragranceModal('${f.id}')">
              <img src="${fragImg}" alt="${f.name}" style="height: 75px; margin: 0 auto 10px; object-fit: contain;">
              <h5 style="font-size: 1.1rem; color: #fff; margin-bottom: 4px;">${f.name}</h5>
              <p style="font-size: 0.78rem; color: var(--text-light); margin-bottom: 12px;">${f.subtitle}</p>
              <button class="btn-primary" style="padding: 8px 16px; font-size: 0.75rem; width: 100%;">
                Ver Ficha
              </button>
            </div>
          `;
        }).join('')}
      </div>
    </div>
  `;
}

/* ==========================================================================
   9. GUÍA DE AMBIENTES & COBERTURA
   ========================================================================== */
function initRoomSection() {
  const btnsContainer = document.getElementById('roomBtnsContainer');
  if (!btnsContainer) return;

  btnsContainer.innerHTML = ROOM_GUIDELINES.map((r, i) => `
    <button class="room-btn ${i === 0 ? 'active' : ''}" data-room-id="${r.id}">
      <span>${r.icon}</span> ${r.name}
    </button>
  `).join('');

  const btns = btnsContainer.querySelectorAll('.room-btn');
  btns.forEach(btn => {
    btn.addEventListener('click', () => {
      btns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderRoomDetail(btn.dataset.roomId);
    });
  });

  renderRoomDetail(ROOM_GUIDELINES[0].id);
}

function renderRoomDetail(roomId) {
  const room = ROOM_GUIDELINES.find(r => r.id === roomId) || ROOM_GUIDELINES[0];
  const container = document.getElementById('roomDetailContainer');
  if (!container) return;

  const fragObjects = room.recommendedAromas.map(id => getFragranceById(id));

  container.innerHTML = `
    <div class="room-detail-card">
      <div>
        <span class="room-badge-pill">${room.icon} Cobertura: ${room.size}</span>
        <h3 class="font-serif" style="font-size: 1.8rem; color: var(--brand-forest-dark); margin-bottom: 10px;">
          ${room.name}
        </h3>
        <p style="font-size: 1rem; color: var(--brand-terracotta); font-weight: 700; margin-bottom: 14px;">
          Formato Óptimo: ${room.recommendedFormat}
        </p>
        <p style="font-size: 0.92rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 20px;">
          💡 <b>Consejo de uso:</b> ${room.tip}
        </p>
      </div>

      <div style="background: var(--bg-warm-light); padding: 24px; border-radius: var(--radius-md); border: 1px solid var(--brand-line);">
        <h4 style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--brand-forest-dark); margin-bottom: 12px;">
          ✦ Aromas Más Recomendados para este Espacio:
        </h4>
        <div style="display: flex; flex-wrap: wrap; gap: 8px;">
          ${fragObjects.map(f => `
            <button class="btn-outline" onclick="openFragranceModal('${f.id}')" style="padding: 8px 14px; font-size: 0.8rem; background: var(--bg-surface);">
              ${f.icon} ${f.name}
            </button>
          `).join('')}
        </div>
      </div>
    </div>
  `;
}

/* ==========================================================================
   10. B2B & REGALOS CORPORATIVOS
   ========================================================================== */
function initB2BSection() {
  const slider = document.getElementById('b2bSlider');
  const qtyLabel = document.getElementById('b2bQtyLabel');
  const priceUnitEl = document.getElementById('b2bPriceUnit');
  const discountLabelEl = document.getElementById('b2bDiscountLabel');
  const totalEstEl = document.getElementById('b2bTotalEst');

  if (!slider) return;

  const basePrice = 12000; // precio base Home Spray

  function updateB2BCalc() {
    const qty = parseInt(slider.value, 10);
    if (qtyLabel) qtyLabel.textContent = `${qty} unidades`;

    let discountPct = 0.15;
    let tierText = '15% OFF';
    if (qty >= 100) {
      discountPct = 0.35;
      tierText = '35% OFF + Etiqueta Personalizada';
    } else if (qty >= 50) {
      discountPct = 0.25;
      tierText = '25% OFF';
    }

    const discountedUnit = Math.round(basePrice * (1 - discountPct));
    const totalEst = discountedUnit * qty;

    if (discountLabelEl) discountLabelEl.textContent = tierText;
    if (priceUnitEl) priceUnitEl.textContent = formatCLP(discountedUnit) + ' / un.';
    if (totalEstEl) totalEstEl.textContent = formatCLP(totalEst);
  }

  slider.addEventListener('input', updateB2BCalc);
  updateB2BCalc();
}

function requestB2BQuote() {
  const slider = document.getElementById('b2bSlider');
  const qty = slider ? slider.value : '50';
  const message = `🏢 *¡Hola Jeshia! Quisiera solicitar una cotización mayorista/corporativa:*\n\n• *Cantidad estimada:* ${qty} unidades\n• *Uso previsto:* (Regalos corporativos / Hotel / Matrimonio / Tienda)\n\n¿Me podrían indicar los tiempos de entrega y catálogo corporativo? ✨`;
  window.open(`https://wa.me/56912345678?text=${encodeURIComponent(message)}`, '_blank');
}

/* ==========================================================================
   11. CALCULADORA ECO-REFILL
   ========================================================================== */
function initEcoCalc() {
  const slider = document.getElementById('ecoSlider');
  const bottlesLabel = document.getElementById('ecoBottlesLabel');
  const savedMoneyEl = document.getElementById('ecoSavedMoney');
  const savedBottlesEl = document.getElementById('ecoSavedBottles');

  if (!slider) return;

  function updateEco() {
    const bottlesPerMonth = parseInt(slider.value, 10);
    if (bottlesLabel) bottlesLabel.textContent = `${bottlesPerMonth} frasco${bottlesPerMonth > 1 ? 's' : ''} al mes`;

    // Ahorro anual estimado comprando recargas de 500ml frente a frascos nuevos
    const yearlyBottles = bottlesPerMonth * 12;
    const moneySaved = yearlyBottles * 4500; // ~$4.500 de ahorro por recarga
    const plasticDiverted = yearlyBottles;

    if (savedMoneyEl) savedMoneyEl.textContent = formatCLP(moneySaved);
    if (savedBottlesEl) savedBottlesEl.textContent = `${plasticDiverted} envases`;
  }

  slider.addEventListener('input', updateEco);
  updateEco();
}

/* ==========================================================================
   12. CARRITO DE COMPRAS DRAWER & DEDICATORIA DE REGALO
   ========================================================================== */
let cart = [];

function initCart() {
  const saved = localStorage.getItem('jeshia_cart');
  if (saved) {
    try { cart = JSON.parse(saved); } catch (e) { cart = []; }
  }
  updateCartUI();

  const openBtn = document.getElementById('cartOpenBtn');
  const closeBtn = document.getElementById('cartCloseBtn');
  const overlay = document.getElementById('cartOverlay');

  if (openBtn) openBtn.addEventListener('click', openCartDrawer);
  if (closeBtn) closeBtn.addEventListener('click', closeCartDrawer);
  if (overlay) {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) closeCartDrawer();
    });
  }
}

function initGiftDedication() {
  const check = document.getElementById('isGiftCheck');
  const panel = document.getElementById('giftDesignerPanel');
  const toInput = document.getElementById('giftTo');
  const fromInput = document.getElementById('giftFrom');
  const msgInput = document.getElementById('giftMsg');

  const previewTo = document.getElementById('previewCardTo');
  const previewMsg = document.getElementById('previewCardMsg');
  const previewFrom = document.getElementById('previewCardFrom');

  if (check && panel) {
    check.addEventListener('change', () => {
      if (check.checked) {
        panel.classList.add('active');
      } else {
        panel.classList.remove('active');
      }
    });
  }

  function syncCard() {
    if (previewTo) previewTo.textContent = toInput?.value.trim() ? `Para: ${toInput.value}` : 'Para: Alguien Especial';
    if (previewMsg) previewMsg.textContent = msgInput?.value.trim() ? `"${msgInput.value}"` : '"Que estos aromas llenen tu hogar de paz y bienestar."';
    if (previewFrom) previewFrom.textContent = fromInput?.value.trim() ? `De: ${fromInput.value}` : 'Con cariño, Jeshia';
  }

  if (toInput) toInput.addEventListener('input', syncCard);
  if (fromInput) fromInput.addEventListener('input', syncCard);
  if (msgInput) msgInput.addEventListener('input', syncCard);
}

function openCartDrawer() {
  const overlay = document.getElementById('cartOverlay');
  if (overlay) overlay.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeCartDrawer() {
  const overlay = document.getElementById('cartOverlay');
  if (overlay) overlay.classList.remove('open');
  document.body.style.overflow = '';
}

function saveCart() {
  localStorage.setItem('jeshia_cart', JSON.stringify(cart));
  updateCartUI();
}

function addProductToCart(productId) {
  const select = document.getElementById(`select-${productId}`);
  const fragranceId = select ? select.value : 'vainilla-coco';
  addToCart(productId, fragranceId, 1);
}

function addToCart(productId, fragranceId, qty = 1) {
  const product = getProductById(productId);
  const fragrance = getFragranceById(fragranceId);

  const existingIndex = cart.findIndex(item => item.productId === productId && item.fragranceId === fragranceId);

  if (existingIndex > -1) {
    cart[existingIndex].qty += qty;
  } else {
    cart.push({
      productId,
      fragranceId,
      name: product.name,
      volume: product.volume,
      price: product.price,
      image: getProductAromaImage(productId, fragranceId),
      fragranceName: fragrance.name,
      fragranceIcon: fragrance.icon,
      qty: qty
    });
  }

  saveCart();
  showToast(`✦ Agregado: ${product.name} (${fragrance.name})`);
  openCartDrawer();
}

function updateCartItemQty(index, delta) {
  if (!cart[index]) return;
  cart[index].qty += delta;
  if (cart[index].qty <= 0) {
    cart.splice(index, 1);
  }
  saveCart();
}

function removeCartItem(index) {
  if (!cart[index]) return;
  cart.splice(index, 1);
  saveCart();
}

function updateCartUI() {
  const countEl = document.getElementById('cartCount');
  const itemsContainer = document.getElementById('cartItems');
  const subtotalEl = document.getElementById('cartSubtotal');
  const totalCount = cart.reduce((sum, item) => sum + item.qty, 0);

  if (countEl) countEl.textContent = totalCount;

  if (!itemsContainer) return;

  if (cart.length === 0) {
    itemsContainer.innerHTML = `
      <div class="empty-cart-msg">
        <div class="icon">🌿</div>
        <h4>Tu carrito está vacío</h4>
        <p>Explora nuestras fragancias y añade tus productos favoritos.</p>
      </div>
    `;
    if (subtotalEl) subtotalEl.textContent = '$0';
    return;
  }

  let subtotal = 0;
  itemsContainer.innerHTML = cart.map((item, index) => {
    const itemTotal = item.price * item.qty;
    subtotal += itemTotal;
    return `
      <div class="cart-item">
        <button class="remove-item-btn" onclick="removeCartItem(${index})" title="Eliminar">✕</button>
        <div class="cart-item-img">
          <img src="${item.image}" alt="${item.name}">
        </div>
        <div class="cart-item-info">
          <h4 class="cart-item-title">${item.name} (${item.volume})</h4>
          <p class="cart-item-frag">${item.fragranceIcon} Aroma: ${item.fragranceName}</p>
          <span class="cart-item-price">${formatCLP(item.price)} c/u</span>
          <div class="cart-item-qty">
            <button class="qty-btn" onclick="updateCartItemQty(${index}, -1)">-</button>
            <span style="font-weight: 700; font-size: 0.88rem;">${item.qty}</span>
            <button class="qty-btn" onclick="updateCartItemQty(${index}, 1)">+</button>
            <span style="margin-left: auto; font-weight: 800; color: var(--brand-forest-dark); font-size: 0.95rem;">
              ${formatCLP(itemTotal)}
            </span>
          </div>
        </div>
      </div>
    `;
  }).join('');

  if (subtotalEl) subtotalEl.textContent = formatCLP(subtotal);
}

function checkoutWhatsApp() {
  if (cart.length === 0) {
    alert('Tu carrito está vacío. Añade algún producto antes de enviar tu pedido.');
    return;
  }

  const phone = '56912345678';
  const notes = document.getElementById('cartNotes')?.value || '';
  const isGift = document.getElementById('isGiftCheck')?.checked || false;
  const giftTo = document.getElementById('giftTo')?.value || '';
  const giftFrom = document.getElementById('giftFrom')?.value || '';
  const giftMsg = document.getElementById('giftMsg')?.value || '';

  let message = `🌿 *¡Hola Jeshia! Deseo realizar el siguiente pedido:*\n\n`;

  let total = 0;
  cart.forEach((item, i) => {
    const itemTotal = item.price * item.qty;
    total += itemTotal;
    message += `*${i + 1}. ${item.name} (${item.volume})*\n`;
    message += `   • Fragancia: ${item.fragranceName}\n`;
    message += `   • Cantidad: ${item.qty} un.\n`;
    message += `   • Subtotal: ${formatCLP(itemTotal)}\n\n`;
  });

  message += `💰 *TOTAL PEDIDO: ${formatCLP(total)}*\n`;

  if (isGift && (giftTo || giftMsg)) {
    message += `\n🎁 *TARJETA DE REGALO INCLUIDA:*\n`;
    if (giftTo) message += `   • Para: ${giftTo}\n`;
    if (giftFrom) message += `   • De: ${giftFrom}\n`;
    if (giftMsg) message += `   • Dedicatoria: "${giftMsg}"\n`;
  }

  if (notes.trim()) {
    message += `\n📝 *Notas de envío:* ${notes.trim()}\n`;
  }

  message += `\n¿Me podrían indicar los datos de transferencia y coordinar el envío? ¡Muchas gracias! ✨`;

  const whatsappUrl = `https://wa.me/${phone}?text=${encodeURIComponent(message)}`;
  window.open(whatsappUrl, '_blank');
}

/* ==========================================================================
   13. MODALES Y QUICK VIEW
   ========================================================================== */
function initModals() {
  const overlay = document.getElementById('modalOverlay');
  const closeBtn = document.getElementById('modalCloseBtn');

  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  if (overlay) {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) closeModal();
    });
  }
}

function closeModal() {
  const overlay = document.getElementById('modalOverlay');
  if (overlay) overlay.classList.remove('open');
  document.body.style.overflow = '';
}

let selectedFragranceFormat = 'home-spray-250';

function openFragranceModal(fragranceId, preselectedFormatId = 'home-spray-250') {
  selectedFragranceFormat = preselectedFormatId;
  const frag = getFragranceById(fragranceId);
  const modalContent = document.getElementById('modalBody');
  const overlay = document.getElementById('modalOverlay');

  if (!modalContent || !overlay) return;

  const currentProd = getProductById(selectedFragranceFormat) || PRODUCTS[0];
  const fragModalImg = getProductAromaImage(selectedFragranceFormat, frag.id);

  const formatButtons = PRODUCTS.map(p => `
    <button class="format-option-btn ${p.id === selectedFragranceFormat ? 'active' : ''}" 
            onclick="updateFragModalFormat('${frag.id}', '${p.id}')">
      <span class="format-opt-title">${p.categoryName} (${p.volume})</span>
      <span class="format-opt-price">${formatCLP(p.price)}</span>
    </button>
  `).join('');

  modalContent.innerHTML = `
    <div class="modal-grid">
      <div class="modal-img-wrap" style="position: relative;">
        <img src="${fragModalImg}" alt="${frag.name}" style="max-width: 85%; max-height: 85%; object-fit: contain;">
        <div style="position: absolute; bottom: 16px; left: 16px; background: rgba(255,255,255,0.95); padding: 6px 12px; border-radius: var(--radius-full); font-size: 0.75rem; font-weight: 700; color: var(--brand-forest-dark); box-shadow: var(--shadow-sm);">
          ${frag.icon} ${frag.name} · ${currentProd.categoryName}
        </div>
      </div>
      <div class="modal-content">
        <span class="card-volume">${frag.icon} ${frag.familyName}</span>
        <h2 class="font-serif" style="font-size: 2rem; color: var(--brand-forest-dark); margin-bottom: 4px;">
          ${frag.name}
        </h2>
        <p style="font-size: 0.92rem; color: var(--brand-terracotta); font-weight: 600; margin-bottom: 12px;">
          ${frag.subtitle}
        </p>
        <p style="font-size: 0.9rem; color: var(--text-muted); line-height: 1.5; margin-bottom: 18px;">
          ${frag.description}
        </p>

        <!-- Selector de Formato de Producto -->
        <div class="modal-format-picker">
          <label class="modal-format-label">1. Elige tu Formato de Envase:</label>
          <div class="modal-formats-grid">
            ${formatButtons}
          </div>
        </div>

        <div style="background: var(--bg-main); padding: 14px; border-radius: var(--radius-md); border: 1px solid var(--brand-line); margin-bottom: 20px;">
          <h4 style="font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--brand-forest-dark); margin-bottom: 8px;">
            ✦ Pirámide Olfativa
          </h4>
          <p style="font-size: 0.82rem; margin-bottom: 3px;"><b>Salida:</b> ${frag.notes.top}</p>
          <p style="font-size: 0.82rem; margin-bottom: 3px;"><b>Corazón:</b> ${frag.notes.heart}</p>
          <p style="font-size: 0.82rem;"><b>Fondo:</b> ${frag.notes.base}</p>
        </div>

        <p style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 20px;">
          🏠 <b>Espacio ideal:</b> ${frag.space} · ✨ <b>Sensación:</b> ${frag.mood}
        </p>

        <button class="btn-primary" onclick="addToCart('${currentProd.id}', '${frag.id}', 1); closeModal();" style="width: 100%;">
          🛒 Añadir ${currentProd.categoryName} en ${frag.name} (${formatCLP(currentProd.price)})
        </button>
      </div>
    </div>
  `;

  overlay.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function updateFragModalFormat(fragranceId, formatId) {
  openFragranceModal(fragranceId, formatId);
}

function openProductQuickView(productId, specificFragranceId = null) {
  const prod = getProductById(productId);
  const select = document.getElementById(`select-${productId}`);
  const currentFragId = specificFragranceId || (select ? select.value : prod.defaultFragrance);
  const frag = getFragranceById(currentFragId);
  const quickViewImg = getProductAromaImage(prod.id, currentFragId);

  const modalContent = document.getElementById('modalBody');
  const overlay = document.getElementById('modalOverlay');

  if (!modalContent || !overlay) return;

  const scentOptions = FRAGRANCES.map(f => `
    <option value="${f.id}" ${f.id === frag.id ? 'selected' : ''}>
      ${f.icon} ${f.name} (${f.subtitle})
    </option>
  `).join('');

  modalContent.innerHTML = `
    <div class="modal-grid">
      <div class="modal-img-wrap" style="position: relative;">
        <img src="${quickViewImg}" alt="${prod.name}" style="max-width: 85%; max-height: 85%; object-fit: contain;">
        <div style="position: absolute; bottom: 16px; left: 16px; background: rgba(255,255,255,0.92); padding: 6px 12px; border-radius: var(--radius-full); font-size: 0.75rem; font-weight: 700; color: var(--brand-forest-dark); box-shadow: var(--shadow-sm);">
          ${frag.icon} Aroma: ${frag.name}
        </div>
      </div>
      <div class="modal-content">
        <span class="card-volume">${prod.volume} · ${prod.categoryName}</span>
        <h2 class="font-serif" style="font-size: 1.8rem; color: var(--brand-forest-dark); margin-bottom: 4px;">
          ${prod.name}
        </h2>
        <p style="font-size: 1.35rem; font-weight: 700; color: var(--brand-terracotta); margin-bottom: 14px;">
          ${formatCLP(prod.price)}
        </p>
        <p style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.5; margin-bottom: 18px;">
          ${prod.description}
        </p>

        <div style="margin-bottom: 18px;">
          <label style="display: block; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; color: var(--brand-forest-dark); margin-bottom: 6px;">
            Aroma Seleccionado:
          </label>
          <select id="modalFragSelect" class="scent-select" onchange="openProductQuickView('${prod.id}', this.value)">
            ${scentOptions}
          </select>
        </div>

        <div style="background: var(--bg-main); padding: 14px; border-radius: var(--radius-md); border: 1px solid var(--brand-line); margin-bottom: 20px;">
          <h4 style="font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--brand-forest-dark); margin-bottom: 8px;">
            ✦ Pirámide Olfativa · ${frag.name}
          </h4>
          <p style="font-size: 0.8rem; margin-bottom: 3px;"><b>Salida:</b> ${frag.notes.top}</p>
          <p style="font-size: 0.8rem; margin-bottom: 3px;"><b>Corazón:</b> ${frag.notes.heart}</p>
          <p style="font-size: 0.8rem;"><b>Fondo:</b> ${frag.notes.base}</p>
        </div>

        <button class="btn-primary" onclick="addToCart('${prod.id}', '${frag.id}', 1); closeModal();" style="width: 100%;">
          🛒 Añadir al Carrito con ${frag.name} (${formatCLP(prod.price)})
        </button>
      </div>
    </div>
  `;

  overlay.classList.add('open');
  document.body.style.overflow = 'hidden';
}

/* ==========================================================================
   14. WIDGET FLOTANTE DE ASESORÍA BOTÁNICA WHATSAPP
   ========================================================================== */
function initFloatingWhatsApp() {
  const tooltip = document.getElementById('whatsappTooltip');
  const closeBtn = document.getElementById('closeWhatsappTooltip');

  // Mostrar tooltip tras 3.5 segundos de navegación
  setTimeout(() => {
    const isDismissed = sessionStorage.getItem('jeshia_wa_tooltip_dismissed');
    if (!isDismissed && tooltip) {
      tooltip.classList.add('show');
    }
  }, 3500);

  if (closeBtn && tooltip) {
    closeBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      tooltip.classList.remove('show');
      sessionStorage.setItem('jeshia_wa_tooltip_dismissed', 'true');
    });
  }
}

/* ==========================================================================
   15. NOTIFICACIONES TOAST
   ========================================================================== */
function showToast(message) {
  let toast = document.getElementById('siteToast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'siteToast';
    toast.className = 'toast';
    document.body.appendChild(toast);
  }

  toast.innerHTML = `<span>🌿</span> ${message}`;
  toast.classList.add('show');

  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => {
    toast.classList.remove('show');
  }, 2800);
}
