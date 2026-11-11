/**
 * Header component for the SuSearch desktop application.
 * Displays the application name and prepares navigation
 * and theme toggle integration.
 * 
 * @param {Object} props - Component properties.
 * @param {Function} [props.onNavigate] - Handles navigation between pages.
 * @param {React.ReactNode} [props.ThemeToggle] - Optional theme toggle component.
 * @returns {JSX.Element} The header element.
 */
export default function Header({
    variant = 'search',
    projectTitle,
    onNavigate,
    themeToggle
}) {
    const isProjectPage = variant === 'project';

    return (
        <header>
            <div>
                {isProjectPage ? (
                    <div>
                        {/* Organization logo will go here */}
                    </div>
                ) : (
                    <div>
                        <span>HUT</span>
                        <span>Hållbar Utveckling Skåne</span>
                    </div>
                )}
            </div>

            {isProjectPage && (
                <nav aria-label="Brödsmulnavigering">
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

            <div>
                {themeToggle}
            </div>
        </header>
    );
}