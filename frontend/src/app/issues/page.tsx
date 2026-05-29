import Link from "next/link";
import { PageHeader } from "@/components/PageHeader";

export default function IssuesPage() {
  return (
    <main>
      <PageHeader title="Issues" subtitle="Synced and AI-generated Jira issue workspace." />
      <div className="actions" style={{ marginBottom: 12 }}>
        <Link className="btn" href="/issues/import">Import</Link>
        <Link className="btn" href="/issues/analyze">Analyze</Link>
        <Link className="btn" href="/issues/drafts">Drafts</Link>
      </div>
      <div className="card table-wrap">
        <table>
          <thead><tr><th>Jira Key</th><th>Title</th><th>Status</th><th>Priority</th><th>Quality</th><th>Risk</th><th>Impact</th></tr></thead>
          <tbody>
            <tr><td>PAY-219</td><td>Payment validation API</td><td>In Progress</td><td>High</td><td>82</td><td>Medium</td><td>High</td></tr>
            <tr><td>PAY-227</td><td>Export report bug</td><td>Todo</td><td>Medium</td><td>68</td><td>High</td><td>Medium</td></tr>
          </tbody>
        </table>
      </div>
    </main>
  );
}
