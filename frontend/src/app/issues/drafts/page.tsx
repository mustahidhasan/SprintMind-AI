"use client";

import { useEffect, useState } from "react";

import { PageHeader } from "@/components/PageHeader";
import { api } from "@/lib/axios";

export default function IssueDraftsPage() {
  const [rows, setRows] = useState<any[]>([]);

  const load = async () => {
    const { data } = await api.get("/issues/drafts");
    setRows(data?.data ?? []);
  };

  const sendToApproval = async (id: string) => {
    await api.post(`/issues/${id}/send-to-approval`);
    await load();
  };

  useEffect(() => {
    load().catch(() => undefined);
  }, []);

  return (
    <main>
      <PageHeader title="Issue Drafts" subtitle="Drafts saved in backend DB." />
      <div className="card table-wrap">
        <table>
          <thead><tr><th>Title</th><th>Priority</th><th>Status</th><th>AI</th><th>Action</th></tr></thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.id}><td>{r.title}</td><td>{r.priority}</td><td>{r.status}</td><td>{r.aiStatus}</td><td><button className="btn" onClick={() => sendToApproval(r.id)}>Send to Approval</button></td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
