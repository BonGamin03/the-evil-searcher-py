import { useState } from "react";
import axios from "axios";
import { useSearchContext } from "@/context/SearchContext";

interface SearchResult {
  id: string;
  title: string;
  url: string;
  displayUrl?: string;
  content: string;
  league?: string;
}

export interface SearchResponse {
  rag: string;       // El texto generado por el LLM/RAG
  results: SearchResult[];    // Los resultados de búsqueda tradicionales
}
const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
// const data: SearchResult[] = [
//   {
//     id: "1",
//     title: "How to survive the Evil Searcher - Tutorial",
//     url: "https://example.com/survive-evil",
//     displayUrl: "https://example.com › survive-evil",
//     description: "Learn the basic steps to navigate through the dark web of the Evil Searcher. Don't let the algorithms catch you off guard.",
//     date: "2 hours ago"
//   },
//   {
//     id: "2",
//     title: "The dark arts of SEO in 2024",
//     url: "https://evil-seo.org/blog",
//     displayUrl: "https://evil-seo.org › blog",
//     description: "Mastering the search results requires more than just keywords. Discover the hidden patterns used by the Evil Searcher to rank content.",
//     date: "May 12, 2024"
//   },
//   {
//     id: "3",
//     title: "GitHub - the-evil-searcher-py: A python based engine",
//     url: "https://github.com/daniel/the-evil-searcher-py",
//     displayUrl: "https://github.com › daniel › the-evil-searcher-py",
//     description: "Official repository for the Evil Searcher project. Built with Python and React for maximum efficiency and speed.",
//   }
// ];

// const textRag = `The Evil Searcher uses a sophisticated Retrieval-Augmented Generation (RAG) system to process your queries. 
// By combining vector embeddings with a private LLM, it scans through indexed dark web archives to find precisely what you need.

// Key features of this architecture:
// 1. **Contextual Awareness**: The system doesn't just look for keywords; it understands the intent behind your search.
// 2. **Deep Indexing**: Every result is processed through a multi-stage reranker before being presented.
// 3. **Data Privacy**: All computations happen locally using the Python backend, ensuring your search history remains yours.
// 4. **Real-time Synthesis**: The information you are reading right now is being synthesized on-the-fly from the top 5 most relevant sources found in the database.

// It is important to remember that the Evil Searcher is still in its experimental phase. 
// Always verify the source links provided below for maximum accuracy. 
// The gradient effect you see at the bottom of this box should disappear once you click the 'Show more' button, expanding the container to its full height and revealing the rest of the documentation about the indexing process and safety protocols implemented in the version 1.0.4.`;
export function useSearch() {
  const { setResults: setContextResults, setLastQuery, hasSearched: contextHasSearched, setHasSearched: setContextHasSearched, results: contextResults } = useSearchContext();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const performSearch = async (query: string) => {
    if (!query.trim()) return;

    setIsLoading(true);
    setError(null);
    setContextHasSearched(true);
    setLastQuery(query);

    try {
      const userEmail = localStorage.getItem("userEmail");
      const response = await axios.get(`${API_URL}/search?query=${encodeURIComponent(query)}`,{ params: { userEmail } });
      console.log("API Response:", response.data);
      setContextResults(response.data); // Guardar globalmente para que persista
    } catch (err) {
      console.error("Search error:", err);
      setError("Failed to fetch results. Please try again.");
      setContextResults(undefined);  
    } finally {
      setIsLoading(false);
    }
  };

  const resetSearch = () => {
    setContextHasSearched(false);
    setContextResults(undefined);
    setError(null);
  };

  return { results: contextResults, isLoading, hasSearched: contextHasSearched, error, performSearch, resetSearch };
}