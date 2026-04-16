import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Loader2, Search as SearchIcon } from "lucide-react"
import { useState } from "react";

interface SearchProps {
  onSearch: (query:string) => void;
  isLoading:boolean
}
export function Search({ onSearch, isLoading }: SearchProps) {
   const [query, setQuery] = useState("");
  const handleSubmit = (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
      <form onSubmit={handleSubmit} className="flex w-full items-center gap-3">
      <div className="flex flex-1 items-center rounded-full border bg-card px-4 py-1 shadow-sm transition-shadow focus-within:shadow-md">
        <SearchIcon className="ml-1 h-4 w-4 text-muted-foreground" />
        <Input 
          type="search" 
          value={query}
          onChange={(e)=>setQuery(e.target.value)}
          placeholder="Search..." 
          className="border-none bg-transparent shadow-none focus-visible:ring-0 h-10 w-full" 
          disabled={isLoading}
        />
      </div>

      <Button 
        type="submit"
        disabled={isLoading || !query.trim()}
        className="rounded-full px-6 h-12 font-medium transition-all duration-200
                   hover:shadow-[0_0_15px_rgba(0,0,0,0.1)] dark:hover:shadow-[0_0_15px_rgba(255,255,255,0.1)] 
                   hover:-translate-y-0.5
                   active:scale-95 active:bg-primary/80"
      >
       
       {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : "Search"}
      </Button>
    </form>
  )
}
