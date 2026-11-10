/**
 * Displays the selected folder and allows users
 * to choose or change the folder for scanning.
 * 
 * @param {Object} props - Component properties.
 * @param {string} props.selectedFolder - Currently selected folder path.
 * @param {Function} props.onSelectFolder - Handles folder selection.
 */
export default function FolderSelector({selectedFolder, onSelectFolder}) {
    return (
        <section>
            <h2>Projektmapp</h2>

            <p>
                {selectedFolder || "Ingen mapp vald."}
            </p>

            <button type="button" onClick={onSelectFolder}>
                {selectedFolder ? "Ändra mapp" : "Välj mapp"} 
            </button>
        </section>
    );
}