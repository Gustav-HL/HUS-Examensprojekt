export default function SearchResults({ results = [] }) {
    
    if (results.length===0){
        return <p> Inga projekt hittades.</p>
    }
    
    return (
        <div>
            {/* map() goes through a list and creates an article element for each project. 
            key={project.id} is used to identify each result. 
            project.name displays the filename. */}
            <p> Resultat: {results.length}</p>

            {results.map((project) => (
                <article key={project.id}>
                    <h3>{project.name}</h3>
                </article>
            ))
            }
        </div>
    );
}