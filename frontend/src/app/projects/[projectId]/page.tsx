import { PageHeader } from "@/components/PageHeader";

export default function ProjectDetailPage({ params }: { params: { projectId: string } }) {
  return (
    <main>
      <PageHeader title={`Project ${params.projectId}`} subtitle="Project summary, risks, and issue quality trends." />
      <div className="card"><p className="muted">Overview placeholder for project analytics and sprint mapping.</p></div>
    </main>
  );
}
