export default function DisplaySelectedDocumentTitle({ file, onRemove }) {
    if (!file) return null;

    return (
        <div>
            <p> Valt Dokument: {file.name} </p>
            <button type="button" onClick={onRemove}> Ta bort </button>
        </div>
    );
}