import Link from "next/link";

export default function ForgotPasswordPage() {
  return (
    <div className="auth-wrap">
      <div className="auth-card">
        <h2>Forgot Password</h2>
        <form className="form">
          <input className="input" placeholder="Email" />
          <button className="btn primary" type="button">Send Reset Link</button>
        </form>
        <div className="actions" style={{ marginTop: 10 }}><Link href="/auth/reset-password" className="btn">Reset Form</Link></div>
      </div>
    </div>
  );
}
