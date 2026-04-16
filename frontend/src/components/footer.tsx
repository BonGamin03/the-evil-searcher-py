export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="w-full border-t bg-background py-6 md:py-0">
      <div className="container flex flex-col items-center justify-between gap-4 md:h-16 md:flex-row mx-auto px-4">
        <p className="text-center text-sm leading-loose text-muted-foreground md:text-left">
          © {currentYear} Evil Searcher, Inc. All rights reserved.
        </p>
        <div className="flex items-center gap-4 text-sm font-medium text-muted-foreground">
          <a href="" className="hover:underline underline-offset-4">Privacy</a>
          <a href="" className="hover:underline underline-offset-4">Terms</a>
        </div>
      </div>
    </footer>
  );
}