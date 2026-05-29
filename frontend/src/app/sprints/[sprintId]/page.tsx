export default function SprintDetailPage({ params }: { params: { sprintId: string } }) {
  return <main><h1>Sprint {params.sprintId}</h1><p>Sprint detail page.</p></main>;
}
