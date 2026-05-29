import Link from "next/link";
import { PageHeader } from "@/components/PageHeader";

export default function OnboardingPage() {
  return (
    <main>
      <PageHeader title="Onboarding" subtitle="Connect your Jira workspace and select your default project and board." />
      <div className="card">
        <h3>Welcome to SprintMind AI</h3>
        <p className="muted">Connect Jira to start analyzing ticket quality and sprint risk.</p>
        <div className="actions">
          <Link className="btn primary" href="/onboarding/connect-jira">Connect Jira</Link>
          <Link className="btn" href="/dashboard">Skip for Demo</Link>
        </div>
      </div>
    </main>
  );
}
