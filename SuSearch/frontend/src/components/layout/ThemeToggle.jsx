import './ThemeToggle.css';

/**
 * Switches between light and dark themes.
 * The icons are local files in public/images.
 *
 * @param {Object} props - Component properties.
 * @param {'light'|'dark'} props.theme - Current theme.
 * @param {Function} props.onToggleTheme - Toggles the theme.
 */
export default function ThemeToggle({ theme, onToggleTheme }) {
  const isDark = theme === 'dark';

  return (
    <button
      type="button"
      className="theme-toggle"
      onClick={onToggleTheme}
      aria-label={isDark ? 'Byt till ljust tema' : 'Byt till mörkt tema'}
      title={isDark ? 'Ljust tema' : 'Mörkt tema'}
    >
      <img
        className="theme-toggle__icon"
        src={isDark ? '/images/sun-accent.svg' : '/images/moon-navy.svg'}
        alt=""
        aria-hidden="true"
      />
    </button>
  );
}
