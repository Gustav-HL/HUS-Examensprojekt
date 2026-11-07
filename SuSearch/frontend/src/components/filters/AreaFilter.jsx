/**
 * Displays a dropdown for filtering projects by area.
 * Allows users to select an area or show all areas.
 *
 * @param {Object} props - Component properties.
 * @param {string} props.value - Currently selected area.
 * @param {Function} props.onChange - Updates the selected area.
 */

export default function AreaFilter({ value, onChange }) {
  return (
    <div className="filter-field">
      <label htmlFor="themeFilter">Område</label>

      <select
        id="themeFilter"
        value={value}
        onChange={(event) => onChange(event.target.value)}
      >
        <option value="">Alla områden</option>
        <option value="Cirkulär ekonomi">Cirkulär ekonomi</option>
        <option value="Klimatanpassning">Klimatanpassning</option>
        <option value="Transporter">Transporter</option>
        <option value="Energi">Energi</option>
        <option value="Mat och konsumtion">Mat och konsumtion</option>
        <option value="Biodiversitet">Biodiversitet</option>
      </select>
    </div>
  );
}
