import { useState } from 'react';
import AreaFilter from './AreaFilter';
import MethodFilter from './MethodFilter';
import ActiveFilters from './ActiveFilters';
/**
 * Displays the filter panel and allows users to filter projects.
 * Handles opening and closing the panel and shows active filter count.
 *
 * @param {Object} props - Component properties.
 * @param {string} props.area - Currently selected area.
 * @param {Function} props.onAreaChange - Updates the selected area.
 * @param {Function} props.onClearFilters - Clears selected filters.
 * @param {string} props.method - Currently selected method.
 * @param {Function} props.onMethodChange - Updates the selected method.
 */

export default function FilterPanel({
  area,
  method,
  onAreaChange,
  onMethodChange,
  onClearFilters
}) {
  const [isOpen, setIsOpen] = useState(false);


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

        <ActiveFilters area={area} method={method} />
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

          <MethodFilter
            value={method}
            onChange={onMethodChange}
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
