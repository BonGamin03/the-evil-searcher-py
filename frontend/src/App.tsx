import { ThemeProvider } from "./components/theme-provider"
import { ModeToggle } from "./components/mode-toggle"
import { Search } from "./components/search"
import { Footer } from "./components/footer" 
import { Header } from "./components/header"

function App() {
  return (
        <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <div className="relative flex flex-col min-h-svh w-full bg-background font-sans antialiased">
        
         
        <Header />
        <div className="fixed top-4 right-6 z-[60]">
             <ModeToggle />
        </div>

        <main className="flex-1 flex flex-col items-center pt-[25vh] px-4">
          <div className="w-full max-w-2xl">
             
            <div className="mb-8 text-center sm:hidden">
                 <h1 className="text-4xl font-black tracking-tighter">Evil Searcher</h1>
            </div>
            <Search />
          </div>
        </main>

        <Footer />
      </div>
    </ThemeProvider>
  )
}

export default App
