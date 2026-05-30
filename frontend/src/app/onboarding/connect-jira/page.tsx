"use client";

import Link from "next/link";
import { useState } from "react";

import { PageHeader } from "@/components/PageHeader";
import { api } from "@/lib/axios";

export default function ConnectJiraPage() {
  const [form, setForm] = useState({
    connectionName: "My Jira Workspace",
    baseUrl: "",
    email: "",
    apiToken: "",
  });
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const onChange = (key: string, value: string) => setForm((prev) => ({ ...prev, [key]: value }));

  const testConnection = async () => {
    setMessage("");
    setError("");
    try {
      const { data } = await api.post("/jira/test-connection", form);
      setMessage(data?.message ?? "Connection test successful");
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Connection test failed");
    }
  };

  const saveConnection = async () => {
    setMessage("");
    setError("");
    try {
      const { data } = await api.post("/jira/connect", form);
      setMessage(data?.message ?? "Jira connected");
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Save failed");
    }
  };

  return (
    <main>
      <PageHeader title="Connect Jira" subtitle="Provide Jira base URL, email, and API token." />
      <div className="card">
        <form className="form" onSubmit={(e) => e.preventDefault()}>
          <div><label className="label">Jira Base URL</label><input className="input" placeholder="https://yourcompany.atlassian.net" value={form.baseUrl} onChange={(e) => onChange("baseUrl", e.target.value)} /></div>
          <div><label className="label">Email</label><input className="input" placeholder="user@company.com" value={form.email} onChange={(e) => onChange("email", e.target.value)} /></div>
          <div><label className="label">API Token</label><input className="input" type="password" placeholder="********" value={form.apiToken} onChange={(e) => onChange("apiToken", e.target.value)} /></div>
          <div><label className="label">Connection Name</label><input className="input" placeholder="Company Jira" value={form.connectionName} onChange={(e) => onChange("connectionName", e.target.value)} /></div>
          {message ? <p className="text-sm text-green-600">{message}</p> : null}
          {error ? <p className="text-sm text-red-600">{error}</p> : null}
          <div className="actions">
            <button className="btn" type="button" onClick={testConnection}>Test Connection</button>
            <button className="btn" type="button" onClick={saveConnection}>Save Connection</button>
            <Link className="btn primary" href="/onboarding/select-project">Continue</Link>
          </div>
        </form>
      </div>
    </main>
  );
}
