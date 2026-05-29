export default function IssueDetailPage({ params }: { params: { issueId: string } }) {
  return <main><h1>Issue {params.issueId}</h1><p>Issue details page.</p></main>;
}
