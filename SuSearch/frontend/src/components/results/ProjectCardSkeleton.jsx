
/**
 * Displays a placeholder project card while project
 * information is loading.
 *
 * @returns {JSX.Element} A project card skeleton.
 */
export default function ProjectCardSkeleton() {
  return (
    <article
      className="project-card-skeleton"
      aria-hidden="true"
    >
      {/* Project area placeholder */}
      <div className="skeleton-area" />

      {/* Project title placeholder */}
      <div className="skeleton-title" />

      {/* Project description placeholders */}
      <div className="skeleton-description">
        <div className="skeleton-line" />
        <div className="skeleton-line" />
        <div className="skeleton-line skeleton-line-short" />
      </div>

      {/* Project footer placeholder */}
      <div className="skeleton-footer">
        <div className="skeleton-tags" />
        <div className="skeleton-button" />
      </div>
    </article>
  );
}
