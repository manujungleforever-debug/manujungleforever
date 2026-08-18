/**
 * Manu Jungle Forever - Global Auto-Correction & Orthography Engine
 * Automatically formats names, titles, and descriptions across the Admin panel.
 */

(function () {
  'use strict';

  // ── 1. DICTIONARY OF PROPER NOUNS & KEYWORDS ──
  const DICTIONARY = [
    { regex: /\bmanu\b/gi, replacement: 'Manu' },
    { regex: /\b(cusco|cuzco)\b/gi, replacement: 'Cusco' },
    { regex: /\b(machu wasi|machuwasi)\b/gi, replacement: 'Machu Wasi' },
    { regex: /\bblanquillo\b/gi, replacement: 'Blanquillo' },
    { regex: /\batalaya\b/gi, replacement: 'Atalaya' },
    { regex: /\bpaucartambo\b/gi, replacement: 'Paucartambo' },
    { regex: /\bpilcopata\b/gi, replacement: 'Pilcopata' },
    { regex: /\bnuevo eden\b/gi, replacement: 'Nuevo Edén' },
    { regex: /\b(amazonia|amazonica|amazonico)\b/gi, replacement: 'Amazonía' },
    { regex: /\bamazonas\b/gi, replacement: 'Amazonas' },
    { regex: /\bamazon\b/gi, replacement: 'Amazon' },
    { regex: /\bperu\b/gi, replacement: 'Perú' },
    { regex: /\b(cocha blanco|cochablanco)\b/gi, replacement: 'Cocha Blanco' },
    { regex: /\bcocha salvador\b/gi, replacement: 'Cocha Salvador' },
    { regex: /\bmadre de dios\b/gi, replacement: 'Madre de Dios' },
    { regex: /\bandes\b/gi, replacement: 'Andes' }
  ];

  // ── 2. PROPER NAME FORMATTER (TITLE CASE) ──
  // Example: "idel everardo maza maza" -> "Idel Everardo Maza Maza"
  function formatProperName(str) {
    if (!str || typeof str !== 'string') return '';
    // Normalize spaces
    const clean = str.trim().replace(/\s+/g, ' ');
    if (!clean) return '';

    return clean.split(' ').map(word => {
      if (!word) return '';
      // Lowercase prepositions in spanish/portuguese if not at the start
      const lower = word.toLowerCase();
      return lower.charAt(0).toUpperCase() + lower.slice(1);
    }).join(' ');
  }

  // ── 3. TITLE / HEADING FORMATTER ──
  // Example: "tour 4 dias reserva de biosfera manu" -> "Tour 4 Días Reserva de Biósfera Manu"
  function formatTitle(str) {
    if (!str || typeof str !== 'string') return '';
    let clean = str.trim().replace(/\s+/g, ' ');
    if (!clean) return '';

    // Split and capitalize
    clean = clean.split(' ').map((word, idx) => {
      const lower = word.toLowerCase();
      // Keep minor words lowercase if not first word
      const minorWords = ['de', 'del', 'la', 'las', 'el', 'los', 'en', 'y', 'a', 'to', 'in', 'of', 'and', 'the', '–', '-'];
      if (idx > 0 && minorWords.includes(lower)) {
        return lower;
      }
      return lower.charAt(0).toUpperCase() + lower.slice(1);
    }).join(' ');

    // Apply dictionary
    DICTIONARY.forEach(({ regex, replacement }) => {
      clean = clean.replace(regex, replacement);
    });

    return clean;
  }

  // ── 4. SENTENCE / DESCRIPTION FORMATTER ──
  // Capitalizes first letter of sentences, cleans punctuation spacing, applies dictionary
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
    if (id.includes('pass') || id.includes('email') || id.includes('token') || id.includes('url') || id.includes('slug')) return 'none';

    // Person Names
    if (id === 'p-n' || id.includes('nombre') || id.includes('pasajero') || id.includes('pax') || id.includes('autor') || id.includes('guia') || label.includes('nombre completo') || label.includes('autor') || label.includes('cliente')) {
      return 'name';
    }

    // Titles
    if (id === 'p-tour' || id.includes('titulo') || id.includes('tour_nombre') || id.includes('tour-nombre') || label.includes('título') || label.includes('nombre del tour')) {
      return 'title';
    }

    // Sentences / Descriptions
    if (el.tagName === 'TEXTAREA' || id.includes('desc') || id.includes('contenido') || id.includes('comentario') || id.includes('itinerario') || label.includes('descripción') || label.includes('comentario') || label.includes('detalle')) {
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
      // Trigger input event to update previews or reactivity if needed
      el.dispatchEvent(new Event('input', { bubbles: true }));
    }
  }

  // ── 7. GLOBAL EVENT LISTENERS ──
  document.addEventListener('blur', function (e) {
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
