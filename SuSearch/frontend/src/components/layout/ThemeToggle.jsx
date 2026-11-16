import './ThemeToggle.css';
/**
 * Toggles between light and dark themes.
 *
 * @param {string} theme - Current theme.
 * @param {Function} onToggleTheme - Function to change the theme.
 */

function ThemeToggle({ theme, onToggleTheme }) {
  const isDark = theme === "dark";

  return (
    <button
      type="button"
      className="theme-toggle"
      onClick={onToggleTheme}
      aria-label={isDark ? "Byt till ljust tema" : "Byt till mörkt tema"}
      title={isDark ? "Ljust tema" : "Mörkt tema"}
    >
      <span aria-hidden="true">
        {isDark ? "☀️" : "🌙"}
      </span>
    </button>
  );
}

export default ThemeToggle;
