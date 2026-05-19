import { ThemeProvider } from "./components/theme-provider"
import { ModeToggle } from "./components/mode-toggle"
import { Search } from "./components/search"
import { Footer } from "./components/footer" 
import { Header } from "./components/header"
import { Results } from "./components/results"
import { Article } from "./components/article"
import { useSearch } from "./lib/use-search"
import { Loading } from "./components/loading"
import { AIInformation } from "./components/ai-information"
import { Routes, Route } from "react-router-dom"

function HomePage() {
   const { results, isLoading, hasSearched, error, performSearch } = useSearch();

  
   
  
return (
    <div className="relative flex flex-col min-h-svh w-full bg-background font-sans antialiased">
      <Header />
      
      <div className="fixed top-4 right-6 z-[60]">
        <ModeToggle />
      </div>

      
      <main className={`flex-1 flex flex-col items-center transition-all duration-500 ease-in-out px-4 
        ${hasSearched ? 'pt-24' : 'pt-[25vh]'}`}>
        
        <div className="w-full max-w-2xl">
          
          {!hasSearched && (
            <div className="mb-8 text-center">
              <h1 className="text-6xl font-black tracking-tighter">Evil Searcher</h1>
            </div>
          )}
          
           
          <div className={`w-full transition-all duration-300 ${hasSearched ? 'mb-8 max-w-3xl' : 'mb-8'}`}>
            <Search onSearch={performSearch} isLoading={isLoading} />
          </div>
            {error && (
            <div className="p-4 mb-6 text-sm text-destructive bg-destructive/10 rounded-lg border border-destructive/20">
              {error}
            </div>
          )}
             

           {isLoading ? (
            <Loading /> 
          ) : (
            hasSearched && !error && (
              <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                {results.rag && <AIInformation content={results.rag} />}
                <Results data={results.results} />
              </div>
            )
          )}
        </div>
      </main>

      <Footer />
    </div>
  )
}

function App() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/article/:id" element={<Article />} />
      </Routes>
    </ThemeProvider>
  )
}

export default App
