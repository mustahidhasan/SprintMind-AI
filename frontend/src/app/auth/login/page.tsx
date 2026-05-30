"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { login, me } from "@/lib/auth";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await login(email, password);
      const token = res?.data?.accessToken;
      if (!token) throw new Error("No access token returned");
      localStorage.setItem("accessToken", token);
      document.cookie = `accessToken=${token}; path=/; max-age=900`;
      const meRes = await me();
      const hasJira = Boolean(meRes?.data?.hasJiraConnection);
      router.push(hasJira ? "/dashboard" : "/onboarding/connect-jira");
      router.refresh();
    } catch (err: any) {
      const status = err?.response?.status;
      const detail = err?.response?.data?.detail;
      const message = err?.response?.data?.message;
      if (status === 401) {
        setError("Invalid email or password");
      } else {
        setError(detail || message || "Login failed");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-wrap">
      <div className="auth-card">
        <h2>Login</h2>
        <p className="muted">Sign in to SprintMind AI.</p>
        <form className="form" onSubmit={onSubmit}>
          <input className="input" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
          <input className="input" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
          {error ? <p className="text-sm text-red-600">{error}</p> : null}
          <button className="btn primary" type="submit" disabled={loading}>{loading ? "Signing in..." : "Login"}</button>
        </form>
        <div className="actions" style={{ marginTop: 10 }}>
          <Link href="/auth/register" className="btn">Register</Link>
          <Link href="/auth/forgot-password" className="btn">Forgot Password</Link>
        </div>
      </div>
    </div>
  );
}
