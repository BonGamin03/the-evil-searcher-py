import { createContext, useContext, useState, type ReactNode } from 'react';

interface SearchResult {
  id: string;
  title: string;
  url: string;
  content: string | string[];
  league?: string;
  relevance_score?: number;
  authority_score?: number;
  freshness_score?: number;
  final_score?: number;
  content_type?: string;
  featured_snippet?: string;
}

interface SearchResponse {
  rag: string;
  results: SearchResult[];
}

interface SearchContextType {
  results: SearchResponse | undefined;
  setResults: (results: SearchResponse | undefined) => void;
  lastQuery: string;
  setLastQuery: (query: string) => void;
  hasSearched: boolean;
  setHasSearched: (value: boolean) => void;
}

const SearchContext = createContext<SearchContextType | undefined>(undefined);

export function SearchProvider({ children }: { children: ReactNode }) {
  const [results, setResults] = useState<SearchResponse | undefined>();
  const [lastQuery, setLastQuery] = useState('');
  const [hasSearched, setHasSearched] = useState(false);

  return (
    <SearchContext.Provider value={{ results, setResults, lastQuery, setLastQuery, hasSearched, setHasSearched }}>
      {children}
    </SearchContext.Provider>
  );
}

export function useSearchContext() {
  const context = useContext(SearchContext);
  if (!context) {
    throw new Error('useSearchContext must be used within a SearchProvider');
  }
  return context;
}
