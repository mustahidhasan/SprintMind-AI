import { PageHeader } from "@/components/PageHeader";

export default function SprintsPage() {
  return (
    <main>
      <PageHeader title="Sprints" subtitle="Sprint-level risk and workload visibility." />
      <div className="card table-wrap">
        <table><thead><tr><th>Sprint</th><th>Total Issues</th><th>Blocked</th><th>Risk Score</th><th>Status</th></tr></thead><tbody><tr><td>Sprint 24</td><td>42</td><td>5</td><td>72</td><td><span className="badge warn">At Risk</span></td></tr><tr><td>Sprint 25</td><td>34</td><td>1</td><td>43</td><td><span className="badge success">Healthy</span></td></tr></tbody></table>
      </div>
    </main>
  );
}
