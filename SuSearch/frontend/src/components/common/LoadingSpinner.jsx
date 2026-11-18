/**
 * Reusable loading indicator component.
 * Displays an animated spinner and a customizable loading message.
 * 
 * @param {Object} props - Component properties.
 * @param {string} [props.message='Laddar...'] - Message displayed during loading.
 */
export default function LoadingSpinner({ message = 'Laddar...'}) {
    return (
        <div className="loading-container" role="status" aria-live="polite">
            <span className="loading-spinner" aria-hidden="true"></span>
            <span>{message}</span>
        </div>
    );
}