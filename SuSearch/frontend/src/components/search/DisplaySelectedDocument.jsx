export default function DisplaySelectedDocument({ file, onRemove }) {
    if (!file) return null;

    return (
        <div>
            <p> Valt Dokument: {file.name} </p>
            <button type="button" onClick={onRemove}> Ta bort </button>
        </div>
    );
}