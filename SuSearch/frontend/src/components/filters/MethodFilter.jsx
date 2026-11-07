/**
 * Displays a dropdown for filtering projects by working method.
 * Allows users to select a method or show all methods.
 *
 * @param {Object} props - Component properties.
 * @param {string} props.value - Currently selected method.
 * @param {Function} props.onChange - Updates the selected method.
 */
export default function MethodFilter({ value, onChange }) {
  return (
    <div className="filter-field">
      <label htmlFor="methodFilter">Arbetssätt</label>

      <select
        id="methodFilter"
        value={value}
        onChange={(event) => onChange(event.target.value)}
      >
        <option value="">Alla arbetssätt</option>
        <option value="Workshop">Workshop</option>
        <option value="Co-design">Co-design</option>
        <option value="Dialogmöten">Dialogmöten</option>
        <option value="Pilotstudie">Pilotstudie</option>
        <option value="Utbildning">Utbildning</option>
      </select>
    </div>
  );
}
