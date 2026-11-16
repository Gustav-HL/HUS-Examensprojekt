
import ProjectCard from './ProjectCard';

/**
 * Displays a list of projects returned by a search.
 *
 * @param {Object} props - Component properties.
 * @param {Array} props.results - List of matching projects.
 * @param {Function} props.onSelectProject - Opens a selected project.
 */
export default function SearchResults({
  results = [],
  onSelectProject
}) {
  if (results.length === 0) {
    return <p>Inga projekt hittades.</p>;
  }

  return (
    <div className="search-results">
      <div className="project-list">
        {results.map((project) => (
          <ProjectCard
            key={project.id}
            project={project}
            onSelectProject={onSelectProject}
          />
        ))}
      </div>
    </div>
  );
}
