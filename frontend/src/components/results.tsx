import { ExternalLink } from "lucide-react";
import { Link } from "react-router-dom";

interface SearchResult {
  id: string;
  title: string;
  url: string;
  displayUrl?: string;
  content: string | string[];
  league?: string;
  relevance_score?: number;
  authority_score?: number;
  freshness_score?: number;
  final_score?: number;
  ranking_type?: string;
  content_type?: string;
  featured_snippet?: string;
  snippet_confidence?: number;
}

interface ResultsProps {
  data: SearchResult[];
}

function getContentPreview(content: string | string[]): string {
  if (Array.isArray(content)) {
    return content[0] || "Sin descripción disponible";
  }
  return content;
}

 export function Results({data}: ResultsProps) {
  return (
    <div className="w-full max-w-3xl flex flex-col gap-8 pb-20">
      {/* Resumen de resultados */}
      <p className="text-sm text-muted-foreground px-1">
        About {data.length} results (0.42 seconds)
      </p>

      {/* Lista de resultados */}
      <div className="flex flex-col gap-10">
        {data.map((items) => (
          <div key={items.id} className="group flex flex-col gap-2">
            {/* Meta info / URL */}
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <span className="truncate">{items.displayUrl || items.url}</span>
              <ExternalLink className="h-3 w-3 opacity-0 group-hover:opacity-100 transition-opacity" />
            </div>

            {/* Título - Link interno */}
            <Link
              to={`/article/${items.id}`}
              className="text-xl font-medium text-blue-600 dark:text-blue-400 hover:underline decoration-blue-600 underline-offset-2 cursor-pointer"
            >
              <h3>{items.title}</h3>
            </Link>

            {/* Badges de ranking */}
            <div className="flex flex-wrap gap-2">
              {items.content_type && (
                <span className="text-xs px-2 py-1 bg-primary/10 text-primary rounded-full font-medium">
                  {items.content_type.toUpperCase()}
                </span>
              )}
              
              {items.freshness_score !== undefined && items.freshness_score >= 80 && (
                <span className="text-xs px-2 py-1 bg-green-100 dark:bg-green-950 text-green-800 dark:text-green-100 rounded-full font-medium">
                  📰 Reciente
                </span>
              )}
              
              {items.authority_score !== undefined && items.authority_score >= 85 && (
                <span className="text-xs px-2 py-1 bg-blue-100 dark:bg-blue-950 text-blue-800 dark:text-blue-100 rounded-full font-medium">
                  ✓ Confiable
                </span>
              )}
            </div>

            {/* Descripción */}
            <div className="text-sm text-foreground/80 leading-relaxed max-w-prose">
              {items.league && (
                <span className="text-muted-foreground mr-2">{items.league} —</span>
              )}
              {items.featured_snippet || getContentPreview(items.content)}...
            </div>

            {/* Score info pequeño */}
            {items.final_score !== undefined && (
              <div className="text-xs text-muted-foreground pt-1">
                <span>Score: {items.final_score.toFixed(1)}</span>
                {items.authority_score !== undefined && (
                  <span> • Autoridad: {items.authority_score.toFixed(0)}%</span>
                )}
              </div>
            )}
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