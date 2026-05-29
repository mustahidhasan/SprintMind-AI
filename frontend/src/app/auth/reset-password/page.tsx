import Link from "next/link";

export default function ResetPasswordPage() {
  return (
    <div className="auth-wrap">
      <div className="auth-card">
        <h2>Reset Password</h2>
        <form className="form">
          <input className="input" type="password" placeholder="New Password" />
          <input className="input" type="password" placeholder="Confirm Password" />
          <button className="btn primary" type="button">Reset Password</button>
        </form>
        <div className="actions" style={{ marginTop: 10 }}><Link href="/auth/login" className="btn">Back to Login</Link></div>
      </div>
    </div>
  );
}
