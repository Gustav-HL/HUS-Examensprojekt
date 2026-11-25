
import './TextSearch.css';

export default function TextSearch({ value, onChange, loading = false }) {
    return (
        <div className="text-search">
            <input
                id="searchText"
                className="text-search-input"
                type="search"
                placeholder="Skriv din sökning här ..."
                aria-label="Sök efter projekt"
                value={value}
                onChange={(event) => onChange(event.target.value)}
            />
        </div>
    );
}