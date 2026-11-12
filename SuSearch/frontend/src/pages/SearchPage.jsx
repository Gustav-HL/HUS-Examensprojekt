
import { useState } from 'react';

import TextSearch from '../components/search/TextSearch';
import DocumentSearch from '../components/search/DocumentSearch';
import DisplaySelectedDocumentTitle from '../components/search/DisplaySelectedDocumentTitle';

import FilterPanel from '../components/filters/FilterPanel';

//import ResultCount from '../components/results/ResultCount';
import SearchResults from '../components/results/SearchResults';

/**
 * Main search page for SuSearch.
 * Connects text search, document search, filters and project results.
 *
 * @param {Object} props - Component properties.
 * @param {Array} props.results - Projects returned by the search.
 * @param {boolean} props.loading - Indicates if a search is loading.
 * @param {Function} props.onSearch - Starts a search.
 * @param {Function} props.onSelectProject - Opens the selected project.
 */
export default function SearchPage({
  results = [],
  loading = false,
  onSearch,
  onSelectProject
}) {
  const [searchTerm, setSearchTerm] = useState('');
  const [area, setArea] = useState('');
  const [method, setMethod] = useState('');
  const [selectedDocument, setSelectedDocument] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);

  /**
   * Sends the current search values to the parent component.
   */
  const handleSearch = (event) => {
    event?.preventDefault();

    if (!searchTerm.trim() && !selectedDocument) {
      alert('OBS! Ange sökord, mening eller välj ett dokument.');
      return;
    }

    setHasSearched(true);

    if (onSearch) {
      onSearch({
        query: searchTerm.trim(),
        area,
        method,
        document: selectedDocument
      });
    }
  };

  /**
   * Resets the selected filters.
   */
  const handleClearFilters = () => {
    setArea('');
    setMethod('');
  };

  /**
   * Removes the selected document.
   */
  const handleRemoveDocument = () => {
    setSelectedDocument(null);
  };

  return (
    <main className="search-page">
      <div className="wrap">

        <section
          className="search-section"
          aria-labelledby="search-heading"
        >
          <h1 id="search-heading">
            Sök efter projekt
          </h1>

          <p>
            Hitta information, metoder och erfarenheter
            från tidigare projekt.
          </p>

          <form onSubmit={handleSearch}>
            <DocumentSearch
              onFileChange={setSelectedDocument}
            />

            <TextSearch
              value={searchTerm}
              onChange={setSearchTerm}
            />
            <button type="submit" disabled={loading}>
              {loading ? 'Söker...' : 'Sök'}
            </button>
          </form>

          {selectedDocument && (
            <DisplaySelectedDocumentTitle
              file={selectedDocument}
              onRemove={handleRemoveDocument}
            />
          )}
        </section>

        <section
          className="filter-section"
          aria-label="Filtrera sökresultat"
        >
          <FilterPanel
            area={area}
            method={method}
            onAreaChange={setArea}
            onMethodChange={setMethod}
            onClearFilters={handleClearFilters}
          />
        </section>

        <section
          className="results-section"
          aria-labelledby="results-heading"
        >
          <h2 id="results-heading">
            Sökresultat
          </h2>
          {/*
          {!loading && hasSearched && (
            <ResultCount count={results.length} />
          )}
           */}

          {loading ? (
            <p role="status">
              Söker efter projekt...
            </p>
          ) : results.length > 0 ? (
            <SearchResults
              results={results}
              onSelectProject={onSelectProject}
            />
          ) : (
            <p role="status">
              {hasSearched
                ? 'Inga projekt hittades. Försök med andra sökord eller filter.'
                : 'Sök efter projekt för att se resultat.'}
            </p>
          )}
        </section>

      </div>
    </main>
  );
}
