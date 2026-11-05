
import { useState } from 'react';
import AreaFilter from './AreaFilter';
/**
 * Displays the filter panel and allows users to filter projects.
 * Handles opening and closing the panel and shows active filter count.
 *
 * @param {Object} props - Component properties.
 * @param {string} props.area - Currently selected area.
 * @param {Function} props.onAreaChange - Updates the selected area.
 * @param {Function} props.onClearFilters - Clears selected filters.
 */

export default function FilterPanel({
  area,
  onAreaChange,
  onClearFilters
}) {
  const [isOpen, setIsOpen] = useState(false);

  const activeCount = area ? 1 : 0;

  return (
    <>
      <div className="filter-line">
        <button
          className="filter-button"
          type="button"
          aria-expanded={isOpen}
          aria-controls="filterPanel"
          onClick={() => setIsOpen(!isOpen)}
        >
          <img
            className="filter-icon"
            src="/images/filter.svg"
            alt=""
            aria-hidden="true"
          />

          <span>Filtrera</span>
        </button>

        <span className="active-filters">
          {activeCount === 0
            ? 'Inga filter valda'
            : '1 filter valt'}
        </span>
      </div>

      <div
        className={`filter-panel ${isOpen ? 'open' : ''}`}
        id="filterPanel"
      >
        <div className="filter-grid">
          <AreaFilter
            value={area}
            onChange={onAreaChange}
          />
        </div>

        <div className="filter-actions">
          <button
            className="clear-button"
            type="button"
            onClick={onClearFilters}
          >
            Nollställ
          </button>
        </div>
      </div>
    </>
  );
}
