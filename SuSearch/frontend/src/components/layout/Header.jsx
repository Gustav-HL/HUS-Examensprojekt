
import './Header.css';

/**
 * Header component for the SuSearch desktop application.
 * Displays the organization name, project navigation,
 * and theme toggle on both pages.
 *
 * @param {Object} props - Component properties.
 * @param {string} [props.variant] - Current page variant.
 * @param {string} [props.projectTitle] - Selected project title.
 * @param {Function} [props.onNavigate] - Handles page navigation.
 * @param {React.ReactNode} [props.themeToggle] - Theme toggle component.
 */
export default function Header({
  variant = 'search',
  projectTitle,
  onNavigate,
  themeToggle
}) {
  const isProjectPage = variant === 'project';

  return (
    <header className="app-header">
      <div className="app-header__inner">

        {/* Organization branding */}
        <div className="app-header__brand">
          <span className="app-header__mark">HUT</span>
          <span className="app-header__name">
            Hållbar Utveckling Skåne
          </span>
        </div>

        {/* Project navigation */}
        {isProjectPage && (
          <nav
            className="app-header__nav"
            aria-label="Brödsmulnavigering"
          >
            <button
              type="button"
              onClick={() => onNavigate?.('search')}
              disabled={!onNavigate}
            >
              Arkiv
            </button>

            <span> / {projectTitle || 'Projekt'}</span>
          </nav>
        )}

        {/* Shared theme toggle */}
        <div className="app-header__actions">
          {themeToggle}
        </div>

      </div>
    </header>
  );
}
