import Link from "next/link";
import { PageHeader } from "@/components/PageHeader";

export default function HomePage() {
  return (
    <main>
      <PageHeader title="Welcome" subtitle="Start with onboarding or open the dashboard." />
      <div className="card">
        <h3>Quick start</h3>
        <div className="actions">
          <Link className="btn primary" href="/onboarding/connect-jira">Connect Jira</Link>
          <Link className="btn" href="/dashboard">Open Dashboard</Link>
          <Link className="btn" href="/issues/import">Import Tasks</Link>
        </div>
      </div>
    </main>
  );
}
