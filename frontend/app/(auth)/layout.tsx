export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-950 dark:bg-neutral-950 dark:text-slate-50">
      {children}
    </div>
  );
}
