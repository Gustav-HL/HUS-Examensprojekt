function ProjectCard({ project }) {
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
                        {/* Place ProjectTags component here */}
                    </div>
                )}

                {project.id != null && (
                    <a
                        href={`/projects/${project.id}`}
                        className="project-card-link"
                    >
                        Visa exempel
                    </a>
                )}
            </footer>
        </article>
    );
}

export default ProjectCard;