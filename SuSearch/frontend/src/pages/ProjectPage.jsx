export default function ProjectPage({ project, onBack }) {
    if (!project) {
        return (
            <main className="project-page">
                <p>Inget projekt har valts.</p>
            </main>
        );
    }

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
                            'Ingen beskrivning tillgänlig.'}
                        </p>
                    </section>

                    <aside className="project-facts">
                        <h2>Projektfakta</h2>

                        <p>
                            <strong>Organisation:</strong>{''}
                            {project.organization || '-'}
                        </p>

                        <p>
                            <strong>Plats:</strong>{''}
                            {project.location || '-'}
                        </p>

                        <p>Status:</p>{''}
                        {project.status || '-'}
                    </aside>

                </div>
            </div>
        </main>
    );
    
}