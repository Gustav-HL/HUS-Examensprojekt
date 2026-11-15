/**
 * Displays the main information about a selected project.
 * Shows the project's area, title and description.
 * 
 * @param {Object} props - Component properties
 * @param {Object} props.object - The project to display.
 */

export default function ProjectInformation({ project }) {
    if (!project) {
        return null;
    }

    return (
        <section>
            {project.area && (
                <p>{project.area}</p>
            )}

            <h1>{project.title || 'Namnlöst projekt'}</h1>

            <div>
                <h2>Om projektet</h2>

                <p>
                    {project.description ||
                    'Ingen tillgänglig beskrivning'}
                </p>
            </div>
        </section>
    );
}