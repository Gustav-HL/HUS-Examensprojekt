
import RelatedProjects from '../components/displayProject/RelatedProjects';
import ProjectFactCards from '../components/displayProject/ProjectFactCards';

/**
 * Displays information about the selected project
 * and its related projects.
 *
 * @param {Object} props - Component properties.
 * @param {Object} props.project - Selected project.
 * @param {Function} props.onBack - Returns to search results.
 * @param {Function} props.onSelectProject - Opens a related project.
 */
export default function ProjectPage({
    project,
    onBack,
    onSelectProject
}) {
    if (!project) {
        return (
            <main className="project-page">
                <p>Inget projekt har valts.</p>
            </main>
        );
    }

    // Get related projects from project data.
    const relatedProjects =
        project.related_projects ?? project.relatedProjects ?? [];

    return (
        <main className="project-page">
            <div className="project-page-container">

                <button
                    type="button"
                    className="project-back-button"
                    onClick={onBack}
                >
                    ← Tillbaka till sökresultat
                </button>

                <div className="project-page-layout">

                    <section className="project-main">
                        {project.area && (
                            <p className="project-category">
                                {project.area}
                            </p>
                        )}

                        <h1>{project.title}</h1>

                        <h2>Om projektet</h2>

                        <p>
                            {project.description ||
                            'Ingen beskrivning tillgänglig.'}
                        </p>
                    </section>

                    <aside className="project-facts">
                        <h2>Projektfakta</h2>

                        <p>
                            <strong>Organisation:</strong>{' '}
                            {project.organization || '-'}
                        </p>

                        <p>
                            <strong>Plats:</strong>{' '}
                            {project.location || '-'}
                        </p>

                        <p>
                            <strong>Status:</strong>{' '}
                            {project.status || '-'}
                        </p>

                        {/* Display additional project facts */}
                        <ProjectFactCards project={project} />

                    </aside>

                </div>

                {/* Display related projects */}
                <RelatedProjects
                    projects={relatedProjects}
                    onSelectProject={onSelectProject}
                />

            </div>
        </main>
    );
}
