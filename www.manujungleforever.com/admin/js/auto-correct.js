/**
 * Manu Jungle Forever - Global Auto-Correction & Orthography Engine
 * Automatically formats and fixes typos in names, titles, and descriptions across the Admin panel.
 */

(function () {
  'use strict';

  // ── 1. DICTIONARY OF TYPOS, PROPER NOUNS & TOURISM TERMS ──
  const DICTIONARY = [
    // Manu & Variations / Typos (e.g. 'maniu', 'manui', 'manú', 'manio')
    { regex: /\b(manu|maniu|manui|manuu|manú|mano|manio|mani)\b/gi, replacement: 'Manu' },
    
    // Cusco
    { regex: /\b(cusco|cuzco|cusko|cuzco)\b/gi, replacement: 'Cusco' },
    
    // Machu Wasi & Machu Picchu
    { regex: /\b(machu wasi|machuwasi|machu huasi|machuhuasi)\b/gi, replacement: 'Machu Wasi' },
    { regex: /\b(machu picchu|machupicchu|machupichu)\b/gi, replacement: 'Machu Picchu' },
    
    // Amazon Locations
    { regex: /\b(blanquillo|blanquio|blanqillo)\b/gi, replacement: 'Blanquillo' },
    { regex: /\b(atalaya|atalalla)\b/gi, replacement: 'Atalaya' },
    { regex: /\b(paucartambo|paucartanbo)\b/gi, replacement: 'Paucartambo' },
    { regex: /\b(pilcopata|pilcopata)\b/gi, replacement: 'Pilcopata' },
    { regex: /\b(nuevo eden|nuevoeden)\b/gi, replacement: 'Nuevo Edén' },
    { regex: /\b(madre de dios|madrededios)\b/gi, replacement: 'Madre de Dios' },
    { regex: /\b(cocha blanco|cochablanco)\b/gi, replacement: 'Cocha Blanco' },
    { regex: /\b(cocha salvador|cochasalvador)\b/gi, replacement: 'Cocha Salvador' },
    { regex: /\b(andes)\b/gi, replacement: 'Andes' },
    { regex: /\b(peru|perú)\b/gi, replacement: 'Perú' },

    // Common Tourism & Spanish Accents
    { regex: /\b(dias)\b/gi, replacement: 'Días' },
    { regex: /\b(dia)\b/gi, replacement: 'Día' },
    { regex: /\b(expedicion|expedición)\b/gi, replacement: 'Expedición' },
    { regex: /\b(biosfera|biósfera)\b/gi, replacement: 'Biósfera' },
    { regex: /\b(fotografia|fotografía)\b/gi, replacement: 'Fotografía' },
    { regex: /\b(observacion|observación)\b/gi, replacement: 'Observación' },
    { regex: /\b(introduccion|introducción)\b/gi, replacement: 'Introducción' },
    { regex: /\b(corazon|corazón)\b/gi, replacement: 'Corazón' },
    { regex: /\b(guia|guía)\b/gi, replacement: 'Guía' },
    { regex: /\b(guias|guías)\b/gi, replacement: 'Guías' },
    { regex: /\b(rio|río)\b/gi, replacement: 'Río' },
    { regex: /\b(rios|ríos)\b/gi, replacement: 'Ríos' },
    { regex: /\b(parque nacional)\b/gi, replacement: 'Parque Nacional' },
    { regex: /\b(reserva)\b/gi, replacement: 'Reserva' },
    { regex: /\b(selva)\b/gi, replacement: 'Selva' },
    { regex: /\b(amazonia|amazonica|amazonico|amasonia)\b/gi, replacement: 'Amazonía' },
    { regex: /\b(amazonas|amasonas)\b/gi, replacement: 'Amazonas' }
  ];

  // ── 2. PROPER NAME FORMATTER (TITLE CASE) ──
  // Example: "idel everardo maza maza" -> "Idel Everardo Maza Maza"
  function formatProperName(str) {
    if (!str || typeof str !== 'string') return '';
    const clean = str.trim().replace(/\s+/g, ' ');
    if (!clean) return '';

    return clean.split(' ').map(word => {
      if (!word) return '';
      const lower = word.toLowerCase();
      return lower.charAt(0).toUpperCase() + lower.slice(1);
    }).join(' ');
  }

  // ── 3. TITLE / TOUR NAME FORMATTER ──
  // Example: "6 dias en el maniu" -> "6 Días en el Manu"
  function formatTitle(str) {
    if (!str || typeof str !== 'string') return '';
    let clean = str.trim().replace(/\s+/g, ' ');
    if (!clean) return '';

    // Step 1: Apply Dictionary replacements first
    DICTIONARY.forEach(({ regex, replacement }) => {
      clean = clean.replace(regex, replacement);
    });

    // Step 2: Capitalize each word, keeping minor prepositions in lowercase unless at start
    const minorWords = ['de', 'del', 'la', 'las', 'el', 'los', 'en', 'y', 'a', 'to', 'in', 'of', 'and', 'the', '–', '-', 'al', 'con', 'por', 'para', 'o'];
    
    clean = clean.split(' ').map((word, idx) => {
      if (!word) return '';
      // If already corrected by dictionary, keep it
      const isDict = DICTIONARY.some(d => d.replacement.toLowerCase() === word.toLowerCase() && d.replacement === word);
      if (isDict) return word;

      const lower = word.toLowerCase();
      if (idx > 0 && minorWords.includes(lower)) {
        return lower;
      }
      return lower.charAt(0).toUpperCase() + lower.slice(1);
    }).join(' ');

    return clean;
  }

  // ── 4. SENTENCE / DESCRIPTION FORMATTER ──
  function formatSentence(str) {
    if (!str || typeof str !== 'string') return '';
    let clean = str.trim().replace(/[ \t]+/g, ' ');
    if (!clean) return '';

    // Fix spacing before punctuation: "hola , como estas ." -> "hola, como estas."
    clean = clean.replace(/\s+([.,;:!?])/g, '$1');
    // Ensure space after punctuation: "hola,como" -> "hola, como"
    clean = clean.replace(/([.,;:!?])([A-Za-z0-9áéíóúÁÉÍÓÚñÑ])/g, '$1 $2');

    // Capitalize start of string and after sentence delimiters (., !, ?, \n)
    clean = clean.replace(/(^\s*|[.!?\n]\s+)([a-záéíóúñ])/g, (match, prefix, char) => {
      return prefix + char.toUpperCase();
    });

    // Apply dictionary terms
    DICTIONARY.forEach(({ regex, replacement }) => {
      clean = clean.replace(regex, replacement);
    });

    return clean;
  }

  // ── 5. INTELLIGENT FIELD INFERENCE ──
  function inferFieldType(el) {
    if (!el) return null;
    const explicit = el.getAttribute('data-case');
    if (explicit) return explicit; // 'name', 'title', 'sentence', 'none'

    const id = (el.id || '').toLowerCase();
    const name = (el.name || '').toLowerCase();
    const placeholder = (el.placeholder || '').toLowerCase();
    const label = el.closest('.ff') ? (el.closest('.ff').querySelector('label')?.textContent || '').toLowerCase() : '';

    // Passwords, emails, URLs, dates, numbers must NEVER be transformed
    const type = (el.type || '').toLowerCase();
    if (['password', 'email', 'url', 'number', 'date', 'datetime-local', 'file', 'hidden'].includes(type)) return 'none';
    if (id.includes('pass') || id.includes('email') || id.includes('token') || id.includes('url') || id.includes('slug') || id === 't-slug' || id === 'b-slug') return 'none';

    // Tour / Blog / Departure Titles
    if (
      id === 't-n' || 
      id === 'd-n' || 
      id === 'b-t' || 
      id === 'tm-t' || 
      id === 'p-tour' || 
      id.includes('titulo') || 
      id.includes('tour_nombre') || 
      id.includes('tour-nombre') || 
      label.includes('nombre del tour') || 
      label.includes('título') ||
      placeholder.includes('nombre del tour') ||
      placeholder.includes('título')
    ) {
      return 'title';
    }

    // Person Names
    if (
      id === 'p-n' || 
      id === 'tm-n' || 
      id === 'b-a' || 
      id.includes('nombre') || 
      id.includes('pasajero') || 
      id.includes('pax') || 
      id.includes('autor') || 
      id.includes('guia') || 
      label.includes('nombre completo') || 
      label.includes('autor') || 
      label.includes('cliente') || 
      label.includes('guía')
    ) {
      return 'name';
    }

    // Sentences / Descriptions / Content
    if (
      el.tagName === 'TEXTAREA' || 
      id === 't-dc' || 
      id === 't-dl' || 
      id === 'b-c' || 
      id === 'b-e' || 
      id === 'tm-c' || 
      id.includes('desc') || 
      id.includes('contenido') || 
      id.includes('comentario') || 
      id.includes('itinerario') || 
      label.includes('descripción') || 
      label.includes('comentario') || 
      label.includes('detalle') ||
      label.includes('itinerario')
    ) {
      return 'sentence';
    }

    return null;
  }

  // ── 6. AUTO-CORRECT HANDLER ──
  function handleAutoCorrect(el) {
    if (!el || !el.value) return;
    const type = inferFieldType(el);
    if (!type || type === 'none') return;

    const original = el.value;
    let corrected = original;

    if (type === 'name') {
      corrected = formatProperName(original);
    } else if (type === 'title') {
      corrected = formatTitle(original);
    } else if (type === 'sentence') {
      corrected = formatSentence(original);
    }

    if (corrected !== original) {
      el.value = corrected;
      // Trigger input & change events for reactive bindings
      el.dispatchEvent(new Event('input', { bubbles: true }));
      el.dispatchEvent(new Event('change', { bubbles: true }));
    }
  }

  // ── 7. GLOBAL EVENT LISTENERS ──
  document.addEventListener('blur', function (e) {
    if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) {
      handleAutoCorrect(e.target);
    }
  }, true);

  document.addEventListener('focusout', function (e) {
    if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) {
      handleAutoCorrect(e.target);
    }
  }, true);

  document.addEventListener('change', function (e) {
    if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) {
      handleAutoCorrect(e.target);
    }
  }, true);

  // Expose helpers globally
  window.MJF_CORRECT = {
    formatProperName,
    formatTitle,
    formatSentence,
    handleAutoCorrect
  };

})();
