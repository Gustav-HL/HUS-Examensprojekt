export default function TextSearch({value, onChange, onSearch}) {
    
    /**
     * When the user clicks on the Search button 
     * or presses Enter in the searchfield. The page gets prevented from reloading.
     * If the textfield is empty, a message is displayed and stops the search.
     * If the search is valid the function continues the search.
     */
    function handleSubmit(event){
        event.preventDefault();

        if (!value.trim()){
            alert('OBS! Ange sökord eller mening.');
            return;
        }
        onSearch(event);
    }


    return (
        <form onSubmit={handleSubmit}>
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



