export default function DocumentSearch({onFileChange}) {
    
    /** When the user selects a file, it will check that the file extension is PDF, TXT or DOCX.
    * If the extension is not supported, it'll display an error message and clear the file field. 
    * If the file extension is supported, it will send the file 
    * to the parent component through onFileChange. 
    */
    function handleDocumentSelection(event){
        const selectedFile = event.target.files[0] ?? null;

        if(!selectedFile){
            return;
        }
        // lista över tillåtna filändelser.
        const acceptedFileFormats =['pdf', 'txt', 'docx'];
        
        // hämtar filändelsen från namnet
        const selectedFileExtension = selectedFile.name.split('.').pop().toLowerCase();

        if(!acceptedFileFormats.includes(selectedFileExtension)){
            alert('OBS! Felaktigt filformat!\nVälj en fil i formatet PDF, TXT eller DOCX');
            event.target.value = '';
            return;
        }

        onFileChange(selectedFile);

    }
   
    return (
        <div>
            <label htmlFor="documentFile">Välj ett dokument</label>
            <input id="documentFile" 
            type="file" 
            accept=".pdf, .txt, .docx"
            onChange={handleDocumentSelection}
            />
        </div>
    );
}