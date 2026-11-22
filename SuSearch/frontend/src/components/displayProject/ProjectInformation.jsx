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
         // tailwind spacing 
        <section className="min-w-0 space-y-6">
            {/* Project area/theme */}
            {project.area && ( <p className="font-ui text-xs font-bold uppercase tracking-wider text-secondary"> {project.area} 
            </p>
            )}

             {/*Responsive project title*/}
             <h1 className="font-heading text-4xl font-bold leading-tight text-primary md:text-5xl"> {project.title || 'Namnlöst projekt'}
             </h1>

            <div className="space-y-3">
                {/* project description/extract */}
                <h2 className="font-heading text-2xl font-bold text-primary">Om projektet</h2>
                <p className="max-w-3xl font-body text-base leading-relaxed text-navy"> {project.description || 'Ingen tillgänglig beskrivning'}
                </p>
            </div>
        </section>
    );
}