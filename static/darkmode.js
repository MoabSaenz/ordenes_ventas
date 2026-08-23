/**
 * ============================================
 * SISTEMA DE MODO OSCURO
 * ============================================
 *
 * Script que maneja:
 * - Activación/desactivación del modo oscuro
 * - Persistencia en localStorage
 * - Detección de preferencia del sistema operativo
 * - Sincronización entre pestañas
 */

class DarkModeManager {
  constructor() {
    this.THEME_KEY = 'theme-preference';
    this.DARK_THEME = 'dark';
    this.LIGHT_THEME = 'light';
    this.toggleButton = null;
    this.init();
  }

  /**
   * Inicializa el sistema de modo oscuro
   */
  init() {
    console.log('[DarkMode] Inicializando...');

    // Obtener tema guardado o preferencia del sistema
    const savedTheme = this.getSavedTheme();
    const preferredTheme = savedTheme || this.getSystemPreference();

    // Aplicar tema ANTES de cualquier cosa
    this.setTheme(preferredTheme);

    // Esperamos al DOM si aún está cargando
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => {
        this.setupToggleButton();
      });
    } else {
      this.setupToggleButton();
    }

    // Escuchar cambios en el sistema operativo
    this.watchSystemPreference();

    // Sincronizar entre pestañas
    this.watchStorageChanges();
  }

  /**
   * Obtiene el tema guardado en localStorage
   * @returns {string|null} 'dark', 'light' o null si no hay guardado
   */
  getSavedTheme() {
    if (typeof localStorage !== 'undefined') {
      return localStorage.getItem(this.THEME_KEY);
    }
    return null;
  }

  /**
   * Obtiene la preferencia del sistema operativo
   * @returns {string} 'dark' o 'light'
   */
  getSystemPreference() {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return this.DARK_THEME;
    }
    return this.LIGHT_THEME;
  }

  /**
   * Aplica el tema al documento
   * @param {string} theme - 'dark' o 'light'
   */
  setTheme(theme) {
    const htmlElement = document.documentElement;
    const resolvedTheme = theme === this.DARK_THEME ? this.DARK_THEME : this.LIGHT_THEME;

    console.log('[DarkMode] Aplicando tema:', resolvedTheme);

    if (resolvedTheme === this.DARK_THEME) {
      htmlElement.setAttribute('data-theme', this.DARK_THEME);
      document.body.classList.add('dark-mode-enabled');
      document.body.classList.remove('light-mode-enabled');
    } else {
      htmlElement.removeAttribute('data-theme');
      document.body.classList.add('light-mode-enabled');
      document.body.classList.remove('dark-mode-enabled');
    }

    if (typeof localStorage !== 'undefined') {
      localStorage.setItem(this.THEME_KEY, resolvedTheme);
    }

    this.updateToggleButtonState(resolvedTheme);

    window.dispatchEvent(new CustomEvent('themechange', {
      detail: { theme: resolvedTheme }
    }));
  }

  /**
   * Alterna entre modo oscuro y claro
   */
  toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === this.DARK_THEME ? this.LIGHT_THEME : this.DARK_THEME;
    console.log('[DarkMode] Toggle:', 'de', currentTheme || 'light', 'a', newTheme);
    this.setTheme(newTheme);
  }

  /**
   * Configura el botón toggle
   */
  setupToggleButton() {
    this.toggleButton = document.getElementById('dark-mode-toggle');

    if (!this.toggleButton) {
      console.warn('[DarkMode] No se encontró el botón dark-mode-toggle');
      return;
    }

    console.log('[DarkMode] Botón encontrado, añadiendo listener');
    this.toggleButton.addEventListener('click', () => {
      console.log('[DarkMode] Click en botón detectado');
      this.toggleTheme();
    });

    // Actualizar el estado visual
    const currentTheme = this.getCurrentTheme();
    this.updateToggleButtonState(currentTheme);
  }

  /**
   * Actualiza el estado visual del botón toggle
   * @param {string} theme - tema actual
   */
  updateToggleButtonState(theme) {
    const toggleButton = document.getElementById('dark-mode-toggle');
    if (!toggleButton) return;

    const isDark = theme === this.DARK_THEME;

    // Actualizar atributos ARIA
    toggleButton.setAttribute('aria-pressed', isDark ? 'true' : 'false');
    toggleButton.setAttribute('title', isDark ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro');

    console.log('[DarkMode] Botón actualizado a:', isDark ? 'dark' : 'light');
    // Nota: El efecto visual del toggle (slider y colores) se maneja completamente con CSS
    // usando html[data-theme="dark"] selector, no se necesita actualizar clases ni contenido
  }

  /**
   * Observa cambios en las preferencias del sistema operativo
   */
  watchSystemPreference() {
    if (!window.matchMedia) return;

    const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');

    // Para navegadores modernos
    if (darkModeQuery.addEventListener) {
      darkModeQuery.addEventListener('change', (e) => {
        // Solo cambiar si no hay tema guardado
        if (!this.getSavedTheme()) {
          const newTheme = e.matches ? this.DARK_THEME : this.LIGHT_THEME;
          this.setTheme(newTheme);
        }
      });
    }
  }

  /**
   * Sincroniza el tema entre pestañas/ventanas del mismo origen
   */
  watchStorageChanges() {
    window.addEventListener('storage', (e) => {
      if (e.key === this.THEME_KEY && e.newValue) {
        this.setTheme(e.newValue);
      }
    });
  }

  /**
   * Obtiene el tema actual
   * @returns {string} 'dark' o 'light'
   */
  getCurrentTheme() {
    return document.documentElement.getAttribute('data-theme') || this.LIGHT_THEME;
  }

  /**
   * Verifica si el modo oscuro está activado
   * @returns {boolean}
   */
  isDarkMode() {
    return this.getCurrentTheme() === this.DARK_THEME;
  }
}

// Inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    window.darkModeManager = new DarkModeManager();
  });
} else {
  window.darkModeManager = new DarkModeManager();
}

// Exportar para uso en módulos si es necesario
if (typeof module !== 'undefined' && module.exports) {
  module.exports = DarkModeManager;
}