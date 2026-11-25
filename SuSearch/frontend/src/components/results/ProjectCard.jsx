import ProjectTags from "./ProjectTags";
import './ProjectCard.css';
/**
 * Displays a project card with its title, description,
 * optional details, tags section, and navigation button.
 *
 * @param {Object} props - Component properties.
 * @param {Object} props.project - Project data to display.
 * @param {string[]} [props.project.tags] - Tags to display when the list isn't empty. 
 * @param {Function} props.onSelectProject - Opens the selected project.
 */

function LimitTextLength(text, maxLength = 500){
    if (!text || text.length <= maxLength) 
        return text;

    const shortText = text.split(". ").slice(3).join(". ").slice(0, maxLength);
    return shortText;
}
function LimitProjectTagLength(tags, maxLength = 100){
    if (!tags || tags.length <= maxLength) 
        return tags;

    const shortTagsLenght = tags.split(". ").slice(3).join(". ").slice(0, maxLength);
    return shortTagsLenght;
}

function ProjectCard({ project, onSelectProject }) {
    
    const tags = [
    ...(project.matched_keywords ?? []),
    ...(project.matched_ner ?? []), 
].map((match) => match.query_keyword);

    return (
        <article className="project-card">
            {project.area && (
                <p className="project-card-area">
                    {project.area}
                </p>
            )}

            <h3>{project.title}</h3>

            <p className="project-card-description">
                {LimitTextLength(project.preview_text, 500) || "Ingen beskrivning tillgänglig."}
            </p>

            <footer className="project-card-footer">
                {project.matched_ner?.length > 0 && (
                    <div className="project-card-tags">
                        <ProjectTags tags={tags.slice(0,4)} />
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
