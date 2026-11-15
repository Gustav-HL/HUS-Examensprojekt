
/**
 * Visar hur många projekt som hittades vid en sökning.
 *
 * @param {Object} props - Komponentens egenskaper.
 * @param {number} props.count - Antal hittade projekt.
 */
export default function ResultCount({ count = 0 }) {
  return (
    <p className="result-count" role="status">
      {count === 1
        ? '1 projekt hittades'
        : `${count} projekt hittades`}
    </p>
  );
}
