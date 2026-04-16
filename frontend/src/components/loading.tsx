import { Loader2 } from "lucide-react";

interface LoadingProps {
  message?: string;
}

export function Loading({ message = "Summoning results..." }: LoadingProps) {
  return (
    <div className="flex flex-col items-center justify-center mt-20 gap-4 text-muted-foreground animate-in fade-in duration-500">
      <div className="relative flex items-center justify-center">
         
        <Loader2 className="h-10 w-10 text-primary animate-spin" />
         
        <div className="absolute h-10 w-10 bg-primary/20 blur-xl rounded-full animate-pulse" />
      </div>
      <p className="text-sm font-medium tracking-wide animate-pulse">
        {message}
      </p>
    </div>
  );
}