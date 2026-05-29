import { PageHeader } from "@/components/PageHeader";

export default function ReportsPage() {
  return (
    <main>
      <PageHeader title="Reports" subtitle="Generate sprint, quality, risk, and business impact reports." />
      <div className="grid cols-2">
        <div className="card"><h3>Report Types</h3><p className="muted">Sprint Health, Issue Quality, Business Impact, Delay Risk, AI Recommendation, Research Experiment.</p></div>
        <div className="card"><h3>Export</h3><div className="actions"><button className="btn">PDF</button><button className="btn">CSV</button><button className="btn">JSON</button></div></div>
      </div>
    </main>
  );
}
