import { PageHeader } from "@/components/PageHeader";

export default function JiraProjectsPage() {
  return (
    <main>
      <PageHeader title="Jira Projects" subtitle="Available projects from connected workspace." />
      <div className="card table-wrap"><table><thead><tr><th>Key</th><th>Name</th><th>Type</th></tr></thead><tbody><tr><td>PAY</td><td>Payments Platform</td><td>Software</td></tr><tr><td>GRO</td><td>Growth App</td><td>Software</td></tr></tbody></table></div>
    </main>
  );
}
