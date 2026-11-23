
/**
 * Displays reusable fact cards with key project information.
 * Handles missing information and supports multiple values.
 *
 * @param {Object} props - Component properties.
 * @param {Object} props.project - Project data to display.
 */

export default function ProjectFactCards({ project = {} }) {

  /**
   * Formats project information for display.
   * Returns a fallback when information is missing.
   */
  const formatValue = (value) => {
    if (Array.isArray(value)) {
      const items = value.filter(
        (item) => item != null && String(item).trim() !== ''
      );

      return items.length > 0
        ? items.join(', ')
        : 'Information saknas';
    }

    if (value === null || value === undefined || value === '') {
      return 'Information saknas';
    }

    return String(value);
  };

  // Project facts to display.
  const facts = [
    {
      label: 'Tidsperiod',
      value: project.period ?? project.duration
    },
    {
      label: 'Område',
      value: project.area ?? project.areas
    },
    {
      label: 'Samarbetspartners',
      value: project.partners ?? project.collaborationPartners
    }
  ];

  return (
    <section
      className="project-fact-cards"
      aria-label="Projektfakta"
    >
      {facts.map((fact) => (
        <div
          className="project-fact-card"
          key={fact.label}
        >
          <h3 className="project-fact-label">
            {fact.label}
          </h3>

          <p className="project-fact-value">
            {formatValue(fact.value)}
          </p>
        </div>
      ))}
    </section>
  );
}
