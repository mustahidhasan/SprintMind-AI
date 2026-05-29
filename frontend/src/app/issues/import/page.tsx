import Link from "next/link";
import { PageHeader } from "@/components/PageHeader";

export default function IssueImportPage() {
  return (
    <main>
      <PageHeader title="Import Tasks" subtitle="Manual entry, CSV upload, and requirement paste." />
      <div className="grid cols-2">
        <div className="card">
          <h3>Manual Input</h3>
          <form className="form">
            <input className="input" placeholder="Raw task title" />
            <textarea className="textarea" placeholder="Raw description" />
            <input className="input" placeholder="Business goal" />
            <input className="input" placeholder="Priority" />
            <input className="input" placeholder="Expected deadline" />
          </form>
        </div>
        <div className="card">
          <h3>CSV / Document</h3>
          <p className="muted">Use columns: title, description, priority, component, assignee, deadline, business_value, notes.</p>
          <input className="input" type="file" />
          <textarea className="textarea" placeholder="Paste meeting notes or requirement document" style={{ marginTop: 10 }} />
        </div>
      </div>
      <div className="actions" style={{ marginTop: 12 }}><Link className="btn primary" href="/issues/analyze">Analyze with AI</Link></div>
    </main>
  );
}
