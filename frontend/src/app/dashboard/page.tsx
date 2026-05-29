import { PageHeader } from "@/components/PageHeader";
import { kpis } from "@/lib/mock-data";

export default function DashboardPage() {
  return (
    <main>
      <PageHeader title="Dashboard" subtitle="Project health, risk, quality, and approvals at a glance." />
      <section className="grid cols-3">
        {kpis.map(([label, value]) => (
          <div className="card" key={label}><div className="muted">{label}</div><div className="kpi">{value}</div></div>
        ))}
      </section>
      <section className="grid cols-2" style={{ marginTop: 14 }}>
        <div className="card"><h3>Sprint Health</h3><p className="muted">Sprint overload: 86% · Blocked issues: 5 · Delay risk: High</p></div>
        <div className="card"><h3>AI Recommendations</h3><p className="muted">Split 3 large tasks, improve acceptance criteria on 8 issues, move 2 low-priority tickets.</p></div>
      </section>
    </main>
  );
}
