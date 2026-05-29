import Link from "next/link";
import { PageHeader } from "@/components/PageHeader";

export default function SelectProjectPage() {
  return (
    <main>
      <PageHeader title="Select Project" subtitle="Choose project, board, default issue type, and sprint." />
      <div className="card">
        <form className="form">
          <div><label className="label">Project</label><select className="select"><option>Payments Platform</option><option>Growth App</option></select></div>
          <div><label className="label">Board</label><select className="select"><option>Engineering Board</option><option>Product Board</option></select></div>
          <div><label className="label">Default Issue Type</label><select className="select"><option>Story</option><option>Task</option><option>Bug</option></select></div>
          <div><label className="label">Default Sprint</label><select className="select"><option>Sprint 24</option><option>Sprint 25</option></select></div>
          <div className="actions"><Link className="btn primary" href="/dashboard">Finish Setup</Link></div>
        </form>
      </div>
    </main>
  );
}
