import { PageHeader } from "@/components/PageHeader";

export default function SprintDetailPage({ params }: { params: { sprintId: string } }) {
  return (
    <main>
      <PageHeader title={`Sprint ${params.sprintId}`} subtitle="Capacity, delay, dependencies, reopen risk, and recommendations." />
      <div className="grid cols-2">
        <div className="card"><h3>Sprint Summary</h3><p className="muted">Total: 42 · Completed: 26 · Blocked: 5 · High Risk: 8 · Risk Score: 72/100</p></div>
        <div className="card"><h3>Team Workload</h3><p className="muted">2 engineers overloaded. Recommend moving low-priority tasks.</p></div>
      </div>
    </main>
  );
}
