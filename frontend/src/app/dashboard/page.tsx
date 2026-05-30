"use client";

import { useEffect, useState } from "react";

import { PageHeader } from "@/components/PageHeader";
import { api } from "@/lib/axios";

export default function DashboardPage() {
  const [summary, setSummary] = useState<any>(null);

  useEffect(() => {
    api.get("/dashboard/summary").then((r) => setSummary(r.data?.data)).catch(() => undefined);
  }, []);

  const cards = [
    ["Total Issues Synced", summary?.totalIssues ?? "-"],
    ["High Risk Issues", summary?.highRiskIssues ?? "-"],
    ["Sprint Risk", summary?.sprintRisk ?? "TBD"],
    ["Average Quality", summary?.averageQualityScore ?? "-"],
    ["Pending Approvals", summary?.pendingApprovals ?? "-"],
    ["Business Impact", summary?.businessImpact ?? "TBD"],
  ];

  return (
    <main>
      <PageHeader title="Dashboard" subtitle="Project health overview." />
      <section className="grid cols-3">
        {cards.map(([label, value]) => (
          <div className="card" key={String(label)}><div className="muted">{label}</div><div className="kpi">{value}</div></div>
        ))}
      </section>
    </main>
  );
}
