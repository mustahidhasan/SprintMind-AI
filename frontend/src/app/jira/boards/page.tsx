import { PageHeader } from "@/components/PageHeader";

export default function JiraBoardsPage() {
  return (
    <main>
      <PageHeader title="Jira Boards" subtitle="Board and sprint mapping." />
      <div className="card table-wrap"><table><thead><tr><th>Board</th><th>Project</th><th>Active Sprint</th></tr></thead><tbody><tr><td>Engineering</td><td>PAY</td><td>Sprint 24</td></tr><tr><td>Product</td><td>GRO</td><td>Sprint 11</td></tr></tbody></table></div>
    </main>
  );
}
