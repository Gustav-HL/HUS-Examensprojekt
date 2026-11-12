
/**
 * Displays a message when no content or results are available.
 *
 * @param {Object} props - Component properties.
 * @param {string} props.title - Title of the empty state.
 * @param {string} props.message - Description of the situation.
 * @param {string} props.hint - Optional guidance for the user.
 * @param {string} props.actionLabel - Optional button text.
 * @param {Function} props.onAction - Function called when the button is clicked.
 */
export default function EmptyState({
  title = 'Inget att visa',
  message = 'Det finns inget innehåll att visa just nu.',
  hint,
  actionLabel,
  onAction
}) {
  return (
    <div className="empty-state" role="status">
      <h3 className="empty-state-title">{title}</h3>

      <p className="empty-state-message">{message}</p>

      {hint && (
        <p className="empty-state-hint">{hint}</p>
      )}

      {actionLabel && onAction && (
        <button
          type="button"
          className="empty-state-button"
          onClick={onAction}
        >
          {actionLabel}
        </button>
      )}
    </div>
  );
}
