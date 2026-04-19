import { useState, useRef, useEffect } from "react";
import { ChevronDown, ChevronUp, Sparkles } from "lucide-react";
import { Button } from "./ui/button";

interface AIInformationProps {
  content: string;
}

export function AIInformation({ content }: AIInformationProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [shouldShowButton, setShouldShowButton] = useState(false);
  const contentRef = useRef<HTMLDivElement>(null);

  // Altura máxima antes de colapsar (ajusta según prefieras)
  const MAX_HEIGHT = 160; 

  useEffect(() => {
    if (contentRef.current) {
      setShouldShowButton(contentRef.current.scrollHeight > MAX_HEIGHT);
    }
  }, [content]);

  if (!content) return null;

  return (
    <div className="relative mb-10 p-6 rounded-2xl border bg-card/50 backdrop-blur-sm border-blue-500/20 shadow-lg shadow-blue-500/5">
      <div className="flex items-center gap-2 mb-4 text-blue-500 font-medium">
        <Sparkles className="h-4 w-4" />
        <span className="text-sm tracking-tight">AI Overview</span>
      </div>

      <div 
        ref={contentRef}
        className={`relative overflow-hidden transition-all duration-500 ease-in-out text-foreground/90 leading-relaxed`}
        style={{ 
          maxHeight: isExpanded ? `${contentRef.current?.scrollHeight}px` : `${MAX_HEIGHT}px` 
        }}
      >
        <p className="whitespace-pre-wrap">{content}</p>
        
        {/* Capa de difuminado (solo visible si no está expandido y el texto es largo) */}
        {!isExpanded && shouldShowButton && (
          <div className="absolute bottom-0 left-0 w-full h-24 bg-gradient-to-t from-background via-background/80 to-transparent pointer-events-none" />
        )}
      </div>

      {shouldShowButton && (
        <div className="mt-4 flex justify-start">
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={() => setIsExpanded(!isExpanded)}
            className="text-blue-500 hover:text-blue-600 hover:bg-blue-500/10 gap-1 pl-0"
          >
            {isExpanded ? (
              <>
                Show less <ChevronUp className="h-4 w-4" />
              </>
            ) : (
              <>
                Show more <ChevronDown className="h-4 w-4" />
              </>
            )}
          </Button>
        </div>
      )}
    </div>
  );
}