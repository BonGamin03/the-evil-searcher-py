import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { ArrowLeft, ExternalLink, Copy, Check } from "lucide-react";
import { Button } from "@/components/ui/button";

interface Article {
  id: string;
  title: string;
  url: string;
  league: string;
  content: string[];
  full_text: string;
}

export function Article() {
  const params = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [article, setArticle] = useState<Article | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const fetchArticle = async () => {
      try {
        const docId = params.id;
        const response = await fetch(`http://localhost:8000/article/${docId}`);
        
        if (!response.ok) {
          throw new Error("Error al cargar el artículo");
        }
        
        const data = await response.json();
        setArticle(data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Error desconocido");
        setArticle(null);
      } finally {
        setLoading(false);
      }
    };

    if (params.id) {
      fetchArticle();
    }
  }, [params.id]);

  const handleCopyUrl = () => {
    if (article?.url) {
      navigator.clipboard.writeText(article.url);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-primary/10 mb-4">
            <div className="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin" />
          </div>
          <p className="text-muted-foreground">Cargando artículo...</p>
        </div>
      </div>
    );
  }

  if (error || !article) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen">
        <div className="text-center max-w-md">
          <h1 className="text-2xl font-bold mb-2">Error</h1>
          <p className="text-muted-foreground mb-6">{error || "No se pudo cargar el artículo"}</p>
          <Button onClick={() => navigate("/")} className="rounded-full">
            Volver a inicio
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header con botón de volver */}
      <div className="sticky top-0 z-40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 border-b">
        <div className="flex items-center justify-between max-w-3xl mx-auto px-4 py-4">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate("/")}
            className="rounded-full"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Volver
          </Button>
          
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={handleCopyUrl}
              className="rounded-full text-xs"
            >
              {copied ? (
                <>
                  <Check className="w-3 h-3 mr-1" />
                  Copiado
                </>
              ) : (
                <>
                  <Copy className="w-3 h-3 mr-1" />
                  Copiar URL
                </>
              )}
            </Button>
            
            <a
              href={article.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-muted-foreground hover:text-foreground transition-colors"
              title="Abrir en sitio original"
            >
              <ExternalLink className="w-4 h-4" />
            </a>
          </div>
        </div>
      </div>

      {/* Contenido principal */}
      <article className="max-w-3xl mx-auto px-4 py-12">
        {/* Metadatos */}
        <div className="mb-8 space-y-2">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <span className="inline-block px-3 py-1 rounded-full bg-primary/10 text-primary font-semibold">
              {article.league}
            </span>
            <span>•</span>
            <span>{new Date().toLocaleDateString("es-ES")}</span>
          </div>
        </div>

        {/* Separador visual */}
        <div className="h-px bg-gradient-to-r from-transparent via-border to-transparent mb-8" />

        {/* Título */}
        <h1 className="text-4xl md:text-5xl lg:text-6xl font-black tracking-tighter mb-8 leading-tight">
          {article.title}
        </h1>

        {/* Separador visual */}
        <div className="h-px bg-gradient-to-r from-transparent via-border to-transparent mb-12" />

        {/* Contenido */}
        <div className="prose prose-invert max-w-none space-y-6">
          {article.content && article.content.length > 0 ? (
            article.content.map((paragraph, index) => (
              <p
                key={index}
                className="text-base md:text-lg leading-relaxed text-foreground/90 first-letter:font-bold first-letter:text-lg"
              >
                {paragraph}
              </p>
            ))
          ) : (
            <p className="text-muted-foreground italic">No hay contenido disponible</p>
          )}
        </div>

        {/* Separador visual final */}
        <div className="h-px bg-gradient-to-r from-transparent via-border to-transparent my-12" />

        {/* Footer con información de la fuente */}
        <div className="bg-muted/30 rounded-lg p-6 border border-muted">
          <h3 className="font-semibold text-sm mb-2">Fuente</h3>
          <a
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-primary hover:underline break-all flex items-center gap-2"
          >
            {article.url}
            <ExternalLink className="w-3 h-3 flex-shrink-0" />
          </a>
        </div>

        {/* Botón flotante de volver */}
        <div className="flex justify-center mt-12">
          <Button
            onClick={() => navigate("/")}
            className="rounded-full px-8"
          >
            Volver a resultados
          </Button>
        </div>
      </article>
    </div>
  );
}
