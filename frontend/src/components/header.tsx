export function Header() {
  return (
    <header className="fixed top-0 left-0 w-full flex items-center justify-between px-6 py-4 z-50 bg-background/80 backdrop-blur-md border-b border-border/40">
      {/* Logo Innovador y Divertido */}
      <div className="flex items-center gap-1 group cursor-pointer select-none">
        <span className="text-2xl font-black tracking-tighter transition-all duration-300 group-hover:scale-110">
          <span className="text-primary">E</span>
          <span className="text-destructive inline-block hover:-rotate-12 transition-transform">v</span>
          <span className="text-primary">i</span>
          <span className="text-primary">l</span>
        </span>
        <span className="ml-1 text-xl font-bold bg-gradient-to-r from-primary via-destructive to-primary bg-[length:200%_auto] animate-gradient-x bg-clip-text text-transparent">
          Searcher
        </span>
      </div>

      {/* Aquí es donde iría el ModeToggle o perfiles si quieres */}
      <div id="header-actions">
        {/* El ModeToggle lo moveremos aquí desde el App.tsx */}
      </div>
    </header>
  );
}