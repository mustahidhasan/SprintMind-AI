export default function ProjectDetailPage({ params }: { params: { projectId: string } }) {
  return <main><h1>Project {params.projectId}</h1><p>Project details page.</p></main>;
}
