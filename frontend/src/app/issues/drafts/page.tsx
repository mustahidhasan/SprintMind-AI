import { PageHeader } from "@/components/PageHeader";

export default function IssueDraftsPage() {
  return (
    <main>
      <PageHeader title="Issue Drafts" subtitle="Generated drafts before creating Jira issues." />
      <div className="card table-wrap">
        <table>
          <thead><tr><th>Title</th><th>Type</th><th>Priority</th><th>Quality</th><th>Risk</th><th>Impact</th><th>Status</th><th>Actions</th></tr></thead>
          <tbody>
            <tr><td>Payment validation API</td><td>Story</td><td>High</td><td>82</td><td>Medium</td><td>High</td><td>Needs Review</td><td>View · Approve</td></tr>
            <tr><td>Export bug fix</td><td>Bug</td><td>Medium</td><td>69</td><td>High</td><td>Medium</td><td>Generated</td><td>Edit · Reject</td></tr>
          </tbody>
        </table>
      </div>
    </main>
  );
}
