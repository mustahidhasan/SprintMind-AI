import Link from "next/link";

export default function LoginPage() {
  return (
    <div className="auth-wrap">
      <div className="auth-card">
        <h2>Login</h2>
        <p className="muted">Sign in to SprintMind AI.</p>
        <form className="form">
          <input className="input" placeholder="Email" />
          <input className="input" type="password" placeholder="Password" />
          <button className="btn primary" type="button">Login</button>
        </form>
        <div className="actions" style={{ marginTop: 10 }}>
          <Link href="/auth/register" className="btn">Register</Link>
          <Link href="/auth/forgot-password" className="btn">Forgot Password</Link>
        </div>
      </div>
    </div>
  );
}
