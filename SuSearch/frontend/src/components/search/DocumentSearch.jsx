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
            <label
                htmlFor="documentFile"
                className="folder-icon-btn"
            >

                <svg
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    aria-hidden="true"
                >
                    <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
                </svg>
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