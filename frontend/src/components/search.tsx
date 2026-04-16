import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Search as SearchIcon } from "lucide-react"

interface SearchProps {
  onSearch: () => void;
}
export function Search({ onSearch }: SearchProps) {
  const handleSubmit = (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSearch();
  };

  return (
      <form onSubmit={handleSubmit} className="flex w-full items-center gap-3">
      <div className="flex flex-1 items-center rounded-full border bg-card px-4 py-1 shadow-sm transition-shadow focus-within:shadow-md">
        <SearchIcon className="ml-1 h-4 w-4 text-muted-foreground" />
        <Input 
          type="search" 
          placeholder="Search..." 
          className="border-none bg-transparent shadow-none focus-visible:ring-0 h-10 w-full" 
        />
      </div>

      <Button 
        type="submit"
        className="rounded-full px-6 h-12 font-medium transition-all duration-200
                   hover:shadow-[0_0_15px_rgba(0,0,0,0.1)] dark:hover:shadow-[0_0_15px_rgba(255,255,255,0.1)] 
                   hover:-translate-y-0.5
                   active:scale-95 active:bg-primary/80"
      >
        Search
      </Button>
    </form>
  )
}
