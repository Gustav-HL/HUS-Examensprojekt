import ProjectCard from './ProjectCard';
export default function SearchResults({ results = [] }) {
    
    if (results.length===0){
        return <p> Inga projekt hittades.</p>
    }
    
    return (
        <div>
            {/* map() goes through a list and creates an article element for each project. 
            key={currentProject.id} is used to identify each result. 
            project={currentProject} sends ddata to projectcard component */}
            <p> Resultat: {results.length}</p>

            {results.map((currentProject) => (
                <ProjectCard 
                    key={currentProject.id}
                    project={currentProject}
                />
            ))}
        </div>
    );
}