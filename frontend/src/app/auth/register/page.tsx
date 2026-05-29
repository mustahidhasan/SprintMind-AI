import Link from "next/link";

export default function RegisterPage() {
  return (
    <div className="auth-wrap">
      <div className="auth-card">
        <h2>Register</h2>
        <form className="form">
          <input className="input" placeholder="Name" />
          <input className="input" placeholder="Email" />
          <input className="input" type="password" placeholder="Password" />
          <button className="btn primary" type="button">Create Account</button>
        </form>
        <div className="actions" style={{ marginTop: 10 }}><Link href="/auth/login" className="btn">Back to Login</Link></div>
      </div>
    </div>
  );
}
