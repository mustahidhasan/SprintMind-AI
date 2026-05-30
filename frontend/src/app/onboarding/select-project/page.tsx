"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { PageHeader } from "@/components/PageHeader";
import { api } from "@/lib/axios";

export default function SelectProjectPage() {
  const [projects, setProjects] = useState<any[]>([]);
  const [boards, setBoards] = useState<any[]>([]);

  useEffect(() => {
    const load = async () => {
      const [p, b] = await Promise.all([api.get("/jira/projects"), api.get("/jira/boards")]);
      setProjects(p.data?.data ?? []);
      setBoards(b.data?.data ?? []);
    };
    load().catch(() => undefined);
  }, []);

  return (
    <main>
      <PageHeader title="Select Project" subtitle="Choose project and board." />
      <div className="card">
        <form className="form">
          <div><label className="label">Project</label><select className="select">{projects.map((p) => <option key={p.id} value={p.id}>{p.name}</option>)}</select></div>
          <div><label className="label">Board</label><select className="select">{boards.map((b) => <option key={b.id} value={b.id}>{b.name}</option>)}</select></div>
          <div className="actions"><Link className="btn primary" href="/dashboard">Finish Setup</Link></div>
        </form>
      </div>
    </main>
  );
}
