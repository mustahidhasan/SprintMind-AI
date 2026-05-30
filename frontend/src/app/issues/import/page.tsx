"use client";

import Link from "next/link";
import { useState } from "react";

import { PageHeader } from "@/components/PageHeader";
import { api } from "@/lib/axios";

export default function IssueImportPage() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState("MEDIUM");
  const [message, setMessage] = useState("");

  const createDraft = async () => {
    const { data } = await api.post("/issues/import", { title, description, sourceType: "MANUAL", priority });
    setMessage(data?.message ?? "Issue draft created");
    setTitle("");
    setDescription("");
  };

  return (
    <main>
      <PageHeader title="Import Tasks" subtitle="Manual issue input currently active." />
      <div className="grid cols-2">
        <div className="card">
          <h3>Manual Input</h3>
          <form className="form" onSubmit={(e) => e.preventDefault()}>
            <input className="input" placeholder="Raw task title" value={title} onChange={(e) => setTitle(e.target.value)} />
            <textarea className="textarea" placeholder="Raw description" value={description} onChange={(e) => setDescription(e.target.value)} />
            <select className="select" value={priority} onChange={(e) => setPriority(e.target.value)}><option>LOW</option><option>MEDIUM</option><option>HIGH</option></select>
            <div className="actions">
              <button className="btn primary" type="button" onClick={createDraft}>Save Draft</button>
              <Link className="btn" href="/issues/drafts">View Drafts</Link>
            </div>
            {message ? <p className="text-sm text-green-600">{message}</p> : null}
          </form>
        </div>
        <div className="card"><h3>AI Status</h3><p className="muted">AI operation: TBD</p></div>
      </div>
    </main>
  );
}
