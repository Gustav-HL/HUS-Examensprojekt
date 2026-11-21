import ProjectTags from "./ProjectTags";
/**
 * Displays a project card with its title, description,
 * optional details, tags section, and navigation button.
 *
 * @param {Object} props - Component properties.
 * @param {Object} props.project - Project data to display.
 * @param {string[]} [props.project.tags] - Tags to display when the list isn't empty. 
 * @param {Function} props.onSelectProject - Opens the selected project.
 */
function ProjectCard({ project, onSelectProject }) {
    return (
        <article>
            {project.area && <p>{project.area}</p>}

            <h3>{project.title}</h3>

            <p>
                {project.description || "Ingen beskrivning tillgänglig."}
            </p>

            <footer>
                {project.tags?.length > 0 && (
                    <div className="project-card-tags">
                        <ProjectTags tags={project.tags} />
              </div>
                )}

                {project.id != null && (
                    <button
                        type="button"
                        className="project-card-link"
                        onClick={() => onSelectProject?.(project)}
                    >
                        Visa projekt
                    </button>
                )}
            </footer>
        </article>
    );
}

export default ProjectCard;
