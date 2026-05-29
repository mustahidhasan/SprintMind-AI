import { PageHeader } from "@/components/PageHeader";

export default function JiraSyncPage() {
  return (
    <main>
      <PageHeader title="Jira Sync" subtitle="Sync projects, boards, sprints, and issue metadata." />
      <div className="card"><p className="muted">Last full sync completed successfully.</p><div className="actions"><button className="btn primary">Run Sync Now</button></div></div>
    </main>
  );
}
