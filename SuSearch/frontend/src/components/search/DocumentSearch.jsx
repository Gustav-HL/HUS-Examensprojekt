import './DocumentSearch.css'
export default function DocumentSearch({ onFileChange }) {

    /** When the user selects a file, it will check that the file extension is PDF, TXT or DOCX.
    * If the extension is not supported, it'll display an error message and clear the file field. 
    * If the file extension is supported, it will send the file 
    * to the parent component through onFileChange. 
    */
    function handleDocumentSelection(event) {
        const selectedFile = event.target.files[0] ?? null;

        if (!selectedFile) {
            return;
        }
        // lista över tillåtna filändelser.
        const acceptedFileFormats = ['pdf', 'txt', 'docx'];

        // hämtar filändelsen från namnet
        const selectedFileExtension = selectedFile.name.split('.').pop().toLowerCase();

        if (!acceptedFileFormats.includes(selectedFileExtension)) {
            alert('OBS! Felaktigt filformat!\nVälj en fil i formatet PDF, TXT eller DOCX');
            event.target.value = '';
            return;
        }

        onFileChange(selectedFile);

    }

    return (
        <div className="document-search-control">
           <label htmlFor="documentFile" className="folder-icon-btn">
            <svg xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                className="lucide lucide-file-text preview-icon"
            >
                <path
                    d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"
                />
                <path d="M14 2v5a1 1 0 0 0 1 1h5"/>
                <path d="M10 9H8"/>
                <path d="M16 13H8"/>
                <path d="M16 17H8"/>
            </svg>

            <span>Dokument</span>
        </label>

            <input
                id="documentFile"
                type="file"
                accept=".pdf, .txt, .docx"
                onChange={handleDocumentSelection}
                className="visually-hidden-file-input"
            />
        </div>
    );
}