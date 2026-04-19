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