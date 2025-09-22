export default function Home() {
  return (
    <main style={{padding: 24}}>
      <h1>DinoDrop MVP</h1>
      <p>Frontend is up. API: <code>{process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8080'}</code></p>
    </main>
  );
}

