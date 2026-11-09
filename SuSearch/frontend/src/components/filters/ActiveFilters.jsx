/**
 * Displays the number of currently active filters.
 * Counts selected area and method filters.
 *
 * @param {Object} props - Component properties.
 * @param {string} props.area - Currently selected area.
 * @param {string} props.method - Currently selected method.
 */
export default function ActiveFilters({ area, method }) {
  const activeCount = Number(Boolean(area)) + Number(Boolean(method));

  return (
    <span className="active-filters">
      {activeCount === 0
        ? 'Inga filter valda'
        : activeCount === 1
          ? '1 filter valt'
          : `${activeCount} filter valda`}
    </span>
  );
}
