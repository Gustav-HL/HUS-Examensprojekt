
import RelatedProjects from '../components/displayProject/RelatedProjects';

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
        
import ProjectFactCards from '../components/displayProject/ProjectFactCards';
import RelatedProjects from '../components/displayProject/RelatedProjects';

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
            <main className="mx-auto w-full max-w-6xl px-4 py-8">
                <p className="font-body text-navy">
                    Inget projekt har valts.
                </p>
            </main>
        );
    }

    // Get related projects from project data.
    const relatedProjects =
        project.related_projects ?? project.relatedProjects ?? [];

    return (
        <main className="min-h-screen bg-background px-4 py-8 md:px-6">
            <div className="mx-auto w-full max-w-6xl space-y-10">

                {/* Back navigation */}
                <button type="button" className="font-ui text-sm font-medium text-primary hover:text-secondary" onClick={onBack}>
                    ← Tillbaka till sökresultat
                </button>

                {/* Responsive layout for project information and facts */}
                <div className="grid grid-cols-1 items-start gap-8 lg:grid-cols-3">

                    {/* Main project information */}
                    <section className="min-w-0 space-y-6 lg:col-span-2">
                        {project.area && (
                            <p className="font-ui text-sm font-semibold text-secondary">
                                {project.area}
                            </p>
                        )}

                        <h1 className="font-heading text-4xl font-bold leading-tight text-primary md:text-5xl">
                            {project.title}
                        </h1>

                        <div className="space-y-3">
                            <h2 className="font-heading text-2xl font-semibold text-primary">
                                Om projektet
                            </h2>

                            <p className="max-w-3xl font-body text-base leading-relaxed text-navy">
                                {project.description ||
                                    'Ingen beskrivning tillgänglig.'}
                            </p>
                        </div>
                    </section>

                    {/* Project facts sidebar */}
                    <aside className="space-y-5 rounded-xl border border-lightgray bg-white p-6">
                        <h2 className="font-heading text-2xl font-semibold text-primary">
                            Projektfakta
                        </h2>

                        <div className="space-y-3 font-body text-sm text-navy">
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
                        </div>

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
