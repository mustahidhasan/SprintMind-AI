"use client";

import { useEffect, useState } from "react";

import { PageHeader } from "@/components/PageHeader";
import { api } from "@/lib/axios";

export default function ApprovalsPage() {
  const [rows, setRows] = useState<any[]>([]);

  const load = async () => {
    const { data } = await api.get("/approvals");
    setRows(data?.data ?? []);
  };

  const approve = async (id: string) => {
    await api.post(`/approvals/${id}/approve`);
    await load();
  };

  const reject = async (id: string) => {
    await api.post(`/approvals/${id}/reject`);
    await load();
  };

  useEffect(() => {
    load().catch(() => undefined);
  }, []);

  return (
    <main>
      <PageHeader title="Approvals" subtitle="Approve or reject issue drafts." />
      <div className="card table-wrap">
        <table>
          <thead><tr><th>ID</th><th>Issue Draft</th><th>Type</th><th>Status</th><th>Actions</th></tr></thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.id}>
                <td>{r.id.slice(0, 8)}</td><td>{r.issueDraftId.slice(0, 8)}</td><td>{r.type}</td><td>{r.status}</td>
                <td className="actions"><button className="btn soft" onClick={() => approve(r.id)}>Approve</button><button className="btn" onClick={() => reject(r.id)}>Reject</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
