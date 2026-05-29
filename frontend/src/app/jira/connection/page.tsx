import { PageHeader } from "@/components/PageHeader";

export default function JiraConnectionPage() {
  return (
    <main>
      <PageHeader title="Jira Connection" subtitle="Manage and verify Jira integration." />
      <div className="card">
        <h3>Connection Status <span className="badge success">Connected</span></h3>
        <p className="muted">URL: https://company.atlassian.net · Email: pm@company.com · Last sync: 10m ago</p>
        <div className="actions">
          <button className="btn">Test Connection</button>
          <button className="btn">Reconnect</button>
          <button className="btn">Sync Jira Metadata</button>
          <button className="btn">Remove Connection</button>
        </div>
      </div>
    </main>
  );
}
