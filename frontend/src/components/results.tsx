import { ExternalLink } from "lucide-react";

interface SearchResult {
  id: string;
  title: string;
  url: string;
  displayUrl: string;
  description: string;
  date?: string;
}
interface ResultsProps {
  data: SearchResult[];
}

const data: SearchResult[] = [
  {
    id: "1",
    title: "How to survive the Evil Searcher - Tutorial",
    url: "https://example.com/survive-evil",
    displayUrl: "https://example.com › survive-evil",
    description: "Learn the basic steps to navigate through the dark web of the Evil Searcher. Don't let the algorithms catch you off guard.",
    date: "2 hours ago"
  },
  {
    id: "2",
    title: "The dark arts of SEO in 2024",
    url: "https://evil-seo.org/blog",
    displayUrl: "https://evil-seo.org › blog",
    description: "Mastering the search results requires more than just keywords. Discover the hidden patterns used by the Evil Searcher to rank content.",
    date: "May 12, 2024"
  },
  {
    id: "3",
    title: "GitHub - the-evil-searcher-py: A python based engine",
    url: "https://github.com/daniel/the-evil-searcher-py",
    displayUrl: "https://github.com › daniel › the-evil-searcher-py",
    description: "Official repository for the Evil Searcher project. Built with Python and React for maximum efficiency and speed.",
  }
];

export function Results({data}: ResultsProps) {
  return (
    <div className="w-full max-w-3xl flex flex-col gap-8 pb-20">
      {/* Resumen de resultados */}
      <p className="text-sm text-muted-foreground px-1">
        About {data.length} results (0.42 seconds)
      </p>

      {/* Lista de resultados */}
      <div className="flex flex-col gap-10">
        {data.map((result) => (
          <div key={result.id} className="group flex flex-col gap-1">
            {/* Meta info / URL */}
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <span className="truncate">{result.displayUrl}</span>
              <ExternalLink className="h-3 w-3 opacity-0 group-hover:opacity-100 transition-opacity" />
            </div>

            {/* Título */}
            <a 
              href={result.url} 
              className="text-xl font-medium text-blue-600 dark:text-blue-400 hover:underline decoration-blue-600 underline-offset-2"
            >
              <h3>{result.title}</h3>
            </a>

            {/* Descripción */}
            <div className="text-sm text-foreground/80 leading-relaxed max-w-prose">
              {result.date && (
                <span className="text-muted-foreground mr-2">{result.date} —</span>
              )}
              {result.description}
            </div>
          </div>
        ))}
      </div>

      {/* Ejemplo de Paginación Simple */}
      <div className="flex items-center justify-center gap-4 mt-10">
        <button className="px-4 py-2 text-sm font-medium rounded-md border hover:bg-accent disabled:opacity-50" disabled>
          Previous
        </button>
        <div className="flex gap-2">
          {[1, 2, 3].map((n) => (
            <button key={n} className={`w-10 h-10 rounded-md text-sm ${n === 1 ? 'bg-primary text-primary-foreground' : 'hover:bg-accent'}`}>
              {n}
            </button>
          ))}
        </div>
        <button className="px-4 py-2 text-sm font-medium rounded-md border hover:bg-accent">
          Next
        </button>
      </div>
    </div>
  );
}