import Link from "next/link";
import { PageHeader } from "@/components/PageHeader";

export default function ConnectJiraPage() {
  return (
    <main>
      <PageHeader title="Connect Jira" subtitle="Provide Jira base URL, email, and API token." />
      <div className="card">
        <form className="form">
          <div><label className="label">Jira Base URL</label><input className="input" placeholder="https://yourcompany.atlassian.net" /></div>
          <div><label className="label">Email</label><input className="input" placeholder="user@company.com" /></div>
          <div><label className="label">API Token</label><input className="input" type="password" placeholder="********" /></div>
          <div><label className="label">Connection Name</label><input className="input" placeholder="Company Jira" /></div>
          <div className="actions">
            <button className="btn" type="button">Test Connection</button>
            <Link className="btn primary" href="/onboarding/select-project">Save Connection</Link>
          </div>
        </form>
      </div>
    </main>
  );
}
