import './Header.css';

/**
 * Shared header for SuSearch.
 * Displays HUT branding, project breadcrumb navigation,
 * and the existing theme toggle.
 *
 * @param {Object} props - Component properties.
 * @param {'search'|'project'} [props.variant='search'] - Active page.
 * @param {string} [props.projectTitle] - Selected project title.
 * @param {Function} [props.onNavigate] - Navigates back to search.
 * @param {React.ReactNode} [props.themeToggle] - Existing theme toggle.
 */
export default function Header({
  variant = 'search',
  projectTitle = '',
  onNavigate,
  themeToggle
}) {
  const isProjectPage = variant === 'project';

  // Both images use the same silhouette and sizing, with colors
  // tailored for light and dark backgrounds.
  const brand = (
    <>
      <img
        className="app-header__logo app-header__logo--light"
        src="/images/hut-logo-light.png"
        alt=""
        aria-hidden="true"
      />
      <img
        className="app-header__logo app-header__logo--dark"
        src="/images/hut-logo-dark.png"
        alt=""
        aria-hidden="true"
      />
      <span className="sr-only">Hållbar Utveckling Skåne</span>
    </>
  );

  return (
    <header className="app-header">
      <div className="app-header__inner">
        <div className="app-header__identity">
          {isProjectPage ? (
            <button
              type="button"
              className="app-header__brand"
              onClick={() => onNavigate?.('search')}
              disabled={!onNavigate}
              title="Tillbaka till sökresultaten"
            >
              {brand}
            </button>
          ) : (
            <div className="app-header__brand">
              {brand}
            </div>
          )}
        </div>

        {isProjectPage && (
          <nav className="app-header__nav" aria-label="Brödsmulnavigering">
            <button
              type="button"
              className="app-header__nav-link"
              onClick={() => onNavigate?.('search')}
              disabled={!onNavigate}
            >
              Arkiv
            </button>
            <span className="app-header__separator" aria-hidden="true">/</span>
            <span
              className="app-header__project-title"
              aria-current="page"
              title={projectTitle || 'Projekt'}
            >
              {projectTitle || 'Projekt'}
            </span>
          </nav>
        )}

        <div className="app-header__actions">
          {themeToggle}
        </div>
      </div>
    </header>
  );
}
