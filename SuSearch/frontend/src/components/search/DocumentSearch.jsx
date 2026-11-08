export default function DocumentSearch({onFileChange}) {
    
    return (
        <div>
            <label htmlFor="documentFile">Välj ett dokument</label>
            <input id="documentFile" 
            type="file" 
            onChange={(event) => onFileChange(event.target.files[0] ?? null)}
            />
        </div>
    );
}