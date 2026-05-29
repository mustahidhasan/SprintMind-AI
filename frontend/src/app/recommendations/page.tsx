import { PageHeader } from "@/components/PageHeader";

export default function RecommendationsPage() {
  return (
    <main>
      <PageHeader title="Recommendations" subtitle="Central place for AI suggestions." />
      <div className="card">
        <h3>Split "Build reporting module" into 3 tasks <span className="badge warn">New</span></h3>
        <p className="muted">Broad scope and high delay risk. Estimated sprint risk reduction: 18%.</p>
        <div className="actions"><button className="btn soft">Accept</button><button className="btn">Reject</button><button className="btn">Create Drafts</button></div>
      </div>
    </main>
  );
}
