import { PageHeader } from "@/components/PageHeader";

export default function SettingsPage() {
  return (
    <main>
      <PageHeader title="Settings" subtitle="Profile, Jira, AI model settings, and privacy controls." />
      <div className="grid cols-2">
        <div className="card">
          <h3>AI Settings</h3>
          <form className="form">
            <select className="select"><option>openai</option><option>anthropic</option><option>gemini</option></select>
            <input className="input" placeholder="Model name" defaultValue="gpt-4o-mini" />
            <input className="input" placeholder="Temperature" defaultValue="0.2" />
            <button className="btn primary" type="button">Save</button>
          </form>
        </div>
        <div className="card"><h3>Privacy & Security</h3><p className="muted">No secrets are displayed in UI. Tokens are intended to be encrypted at backend layer.</p></div>
      </div>
    </main>
  );
}
