"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { me, register } from "@/lib/auth";

export default function RegisterPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await register(name, email, password);
      const token = res?.data?.accessToken;
      if (!token) throw new Error("No access token returned");
      localStorage.setItem("accessToken", token);
      document.cookie = `accessToken=${token}; path=/; max-age=900`;
      const meRes = await me();
      const hasJira = Boolean(meRes?.data?.hasJiraConnection);
      router.push(hasJira ? "/dashboard" : "/onboarding/connect-jira");
      router.refresh();
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-wrap">
      <div className="auth-card">
        <h2>Register</h2>
        <form className="form" onSubmit={onSubmit}>
          <input className="input" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
          <input className="input" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
          <input className="input" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
          {error ? <p className="text-sm text-red-600">{error}</p> : null}
          <button className="btn primary" type="submit" disabled={loading}>{loading ? "Creating..." : "Create Account"}</button>
        </form>
        <div className="actions" style={{ marginTop: 10 }}><Link href="/auth/login" className="btn">Back to Login</Link></div>
      </div>
    </div>
  );
}
