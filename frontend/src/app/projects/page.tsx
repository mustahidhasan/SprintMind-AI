import { PageHeader } from "@/components/PageHeader";

export default function ProjectsPage() {
  return (
    <main>
      <PageHeader title="Projects" subtitle="Project-level overview and selection." />
      <div className="card table-wrap"><table><thead><tr><th>Project</th><th>Board</th><th>Active Sprint</th><th>Risk</th></tr></thead><tbody><tr><td>Payments Platform</td><td>Engineering</td><td>Sprint 24</td><td>High</td></tr><tr><td>Growth App</td><td>Product</td><td>Sprint 11</td><td>Medium</td></tr></tbody></table></div>
    </main>
  );
}
