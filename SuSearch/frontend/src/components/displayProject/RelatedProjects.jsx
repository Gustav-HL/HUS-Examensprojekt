
/**
 * Displays projects related to the selected project.
 * Allows users to open a related project.
 *
 * @param {Object} props - Component properties.
 * @param {Array} props.projects - List of related projects.
 * @param {Function} props.onSelectProject - Opens a related project.
 */
export default function RelatedProjects({
  projects = [],
  onSelectProject
}) {
  const relatedProjects = Array.isArray(projects)
    ? projects.filter((project) => project && typeof project === 'object')
    : [];

  return (
    <section
      className="related-projects"
      aria-label="Relaterade projekt"
    >
      <h2>Relaterade projekt</h2>

      {relatedProjects.length === 0 ? (
        <p>Inga relaterade projekt hittades.</p>
      ) : (
        <div className="related-project-list">
          {relatedProjects.map((project, index) => (
            <article
              className="related-project-card"
              key={project.id ?? index}
            >
              {project.area && (
                <p>{project.area}</p>
              )}

              <h3>{project.title || 'Namnlöst projekt'}</h3>

              <p>
                {project.description ||
                  'Ingen beskrivning tillgänglig.'}
              </p>

              <button
                type="button"
                onClick={() => onSelectProject?.(project)}
                disabled={!onSelectProject}
              >
                Visa projekt
              </button>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
