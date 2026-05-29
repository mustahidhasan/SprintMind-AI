import { PageHeader } from "@/components/PageHeader";

export default function IssueDetailPage({ params }: { params: { issueId: string } }) {
  return (
    <main>
      <PageHeader title={`Issue ${params.issueId}`} subtitle="Jira data, AI analysis, quality, risk, and approval history." />
      <div className="grid cols-2">
        <div className="card"><h3>Original Jira Data</h3><p className="muted">Status, assignee, priority, labels, sprint.</p></div>
        <div className="card"><h3>AI Analysis</h3><p className="muted">Quality breakdown, risk explanation, impact score.</p></div>
      </div>
      <div className="card" style={{ marginTop: 12 }}><h3>Automation Logs</h3><p className="muted">No recent automation logs.</p></div>
    </main>
  );
}
