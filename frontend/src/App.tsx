import { ThemeProvider } from "./components/theme-provider"
import { ModeToggle } from "./components/mode-toggle"
import { Search } from "./components/search"
import { Footer } from "./components/footer" 
import { Header } from "./components/header"
import { useState } from "react"
import { Results } from "./components/results"
import { useSearch } from "./lib/use-search"

function App() {
   const { results, isLoading, hasSearched, error, performSearch } = useSearch();

  
   
  
return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <div className="relative flex flex-col min-h-svh w-full bg-background font-sans antialiased">
        <Header />
        
        <div className="fixed top-4 right-6 z-[60]">
          <ModeToggle />
        </div>

        {/* El padding superior cambia dinámicamente */}
        <main className={`flex-1 flex flex-col items-center transition-all duration-500 ease-in-out px-4 
          ${hasSearched ? 'pt-24' : 'pt-[25vh]'}`}>
          
          <div className="w-full max-w-2xl">
            {/* Ocultar el título grande cuando hay resultados */}
            {!hasSearched && (
              <div className="mb-8 text-center">
                <h1 className="text-6xl font-black tracking-tighter">Evil Searcher</h1>
              </div>
            )}
            
            {/* Pasamos la función de búsqueda al componente Search */}
            <div className={`w-full transition-all duration-300 ${hasSearched ? 'mb-8 max-w-3xl' : 'mb-8'}`}>
              <Search onSearch={performSearch} isLoading={isLoading} />
            </div>
              {error && (
              <div className="p-4 mb-6 text-sm text-destructive bg-destructive/10 rounded-lg border border-destructive/20">
                {error}
              </div>
            )}
              {hasSearched && !isLoading && !error && (
              <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                <Results data={results} />
              </div>
            )}

            {isLoading && (
              <div className="flex flex-col items-center justify-center mt-20 gap-4 text-muted-foreground animate-pulse">
                <div className="h-8 w-8 border-4 border-primary border-t-transparent rounded-full animate-spin" />
                <p>Summoning results...</p>
              </div>
            )}
          </div>
        </main>

        <Footer />
      </div>
    </ThemeProvider>
  )
}

export default App
