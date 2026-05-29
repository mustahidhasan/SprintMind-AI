import { PageHeader } from "@/components/PageHeader";

export default function IssueAnalyzePage() {
  return (
    <main>
      <PageHeader title="AI Analysis" subtitle="Review generated drafts, quality scores, risk, and actions." />
      <div className="card">
        <h3>Raw Input</h3>
        <p className="muted">Implement payment validation and graceful checkout failure handling.</p>
      </div>
      <div className="grid cols-2" style={{ marginTop: 12 }}>
        <div className="card"><h3>AI Draft</h3><p>Title: Implement payment validation API</p><p className="muted">Acceptance Criteria: error mapping, retry path, test coverage.</p></div>
        <div className="card"><h3>Scores</h3><p>Quality: 71/100</p><p>Delay Risk: Medium</p><p>Business Impact: High</p></div>
      </div>
      <div className="card" style={{ marginTop: 12 }}>
        <h3>Recommended Actions</h3>
        <p className="muted">Add missing criteria, split into subtasks, confirm API dependency.</p>
        <div className="actions">
          <button className="btn">Edit Draft</button><button className="btn">Regenerate</button><button className="btn soft">Accept Suggestion</button><button className="btn primary">Send to Approval</button>
        </div>
      </div>
    </main>
  );
}
