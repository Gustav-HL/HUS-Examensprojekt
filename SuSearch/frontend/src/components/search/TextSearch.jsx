export default function TextSearch({value, onChange, onSearch}) {
    
    return (
        <form onSubmit={onSearch}>
            <label htmlFor="searchText"> Sök efter projekt </label>

            <input
                id="searchText"
                type="search"
                placeholder="Skriv din sökning här ..."
                value={value}
                onChange={(event) => onChange(event.target.value)}
            />

            <button type="submit">Sök</button>
        </form>
    );
}



