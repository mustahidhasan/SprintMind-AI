import { PageHeader } from "@/components/PageHeader";

export default function ApprovalsPage() {
  return (
    <main>
      <PageHeader title="Approvals" subtitle="Review AI actions before Jira updates." />
      <div className="grid">
        <div className="card">
          <h3>Create Story: Implement payment validation API</h3>
          <p className="muted">Quality: 82/100 · Risk: Medium · Reason: backend validation + checkout resilience.</p>
          <div className="actions"><button className="btn soft">Approve</button><button className="btn">Edit Before Approve</button><button className="btn">Reject</button></div>
        </div>
      </div>
    </main>
  );
}
