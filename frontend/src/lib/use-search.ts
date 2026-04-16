import { useState } from "react";
import axios from "axios";

export interface SearchResult {
  id: string;
  title: string;
  url: string;
  displayUrl: string;
  description: string;
  date?: string;
}

export function useSearch() {
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const performSearch = async (query: string) => {
    if (!query.trim()) return;

    setIsLoading(true);
    setError(null);
    setHasSearched(true);

    try {
      console.log("Performing search for query:", query);
      const response = await axios.get(`http://localhost:8000/search?q=${encodeURIComponent(query)}`);
      setResults(response.data);
    } catch (err) {
      console.error("Search error:", err);
      setError("Failed to fetch results. Please try again.");
      setResults([]); // Limpiar resultados previos en caso de error
    } finally {
      setIsLoading(false);
    }
  };

  const resetSearch = () => {
    setHasSearched(false);
    setResults([]);
    setError(null);
  };

  return { results, isLoading, hasSearched, error, performSearch, resetSearch };
}