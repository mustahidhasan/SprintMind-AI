"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { logout } from "@/lib/auth";

type NavItem = {
  label: string;
  href?: string;
  icon: React.ReactNode;
  children?: Array<{ label: string; href: string }>;
};

const IconStroke = { fill: "none", stroke: "currentColor", strokeWidth: 2 } as const;

const icons = {
  dashboard: <svg className="h-4 w-4" viewBox="0 0 24 24" {...IconStroke}><path d="M3 13h8V3H3zM13 21h8V11h-8zM13 3h8v6h-8zM3 21h8v-6H3z" /></svg>,
  onboarding: <svg className="h-4 w-4" viewBox="0 0 24 24" {...IconStroke}><path d="M12 20h9" /><path d="M12 4h9" /><path d="M4 9h16" /><path d="M4 15h16" /></svg>,
  jira: <svg className="h-4 w-4" viewBox="0 0 24 24" {...IconStroke}><rect x="3" y="3" width="18" height="18" rx="2" /><path d="M7 12h10" /></svg>,
  issues: <svg className="h-4 w-4" viewBox="0 0 24 24" {...IconStroke}><rect x="4" y="3" width="16" height="18" rx="2" /><path d="M8 8h8M8 12h8M8 16h5" /></svg>,
  sprints: <svg className="h-4 w-4" viewBox="0 0 24 24" {...IconStroke}><path d="M4 6h16M4 12h16M4 18h10" /></svg>,
  approvals: <svg className="h-4 w-4" viewBox="0 0 24 24" {...IconStroke}><path d="M20 6L9 17l-5-5" /></svg>,
  recommendations: <svg className="h-4 w-4" viewBox="0 0 24 24" {...IconStroke}><path d="M12 2v4" /><path d="M12 18v4" /><path d="M4.9 4.9l2.8 2.8" /><path d="M16.3 16.3l2.8 2.8" /><circle cx="12" cy="12" r="4" /></svg>,
  reports: <svg className="h-4 w-4" viewBox="0 0 24 24" {...IconStroke}><path d="M4 19h16" /><path d="M7 15V9" /><path d="M12 15V5" /><path d="M17 15v-3" /></svg>,
  settings: <svg className="h-4 w-4" viewBox="0 0 24 24" {...IconStroke}><circle cx="12" cy="12" r="3" /><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 0 1-4 0v-.1a1.7 1.7 0 0 0-1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 0 1 0-4h.1a1.7 1.7 0 0 0 1.5-1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 0 1 4 0v.1a1.7 1.7 0 0 0 1 1.5h.1a1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 0 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z" /></svg>,
};

const navItems: NavItem[] = [
  { label: "Dashboard", href: "/dashboard", icon: icons.dashboard },
  { label: "Onboarding", icon: icons.onboarding, children: [{ label: "Start", href: "/onboarding" }, { label: "Connect Jira", href: "/onboarding/connect-jira" }, { label: "Select Project", href: "/onboarding/select-project" }] },
  { label: "Jira", icon: icons.jira, children: [{ label: "Connection", href: "/jira/connection" }, { label: "Projects", href: "/jira/projects" }, { label: "Boards", href: "/jira/boards" }, { label: "Sync", href: "/jira/sync" }] },
  { label: "Issues", icon: icons.issues, children: [{ label: "List", href: "/issues" }, { label: "Import", href: "/issues/import" }, { label: "Analyze", href: "/issues/analyze" }, { label: "Drafts", href: "/issues/drafts" }] },
  { label: "Sprints", href: "/sprints", icon: icons.sprints },
  { label: "Approvals", href: "/approvals", icon: icons.approvals },
  { label: "Recommendations", href: "/recommendations", icon: icons.recommendations },
  { label: "Reports", href: "/reports", icon: icons.reports },
  { label: "Settings", href: "/settings", icon: icons.settings },
];

function BrandMark({ collapsed }: { collapsed: boolean }) {
  return (
    <div className="mb-4 flex items-center gap-2 rounded-xl border border-line bg-white px-2 py-2">
      <div className="grid h-8 w-8 place-items-center rounded-lg bg-brand text-xs font-bold text-white">SM</div>
      <div className={`transition-all duration-200 ${collapsed ? "w-0 overflow-hidden opacity-0" : "opacity-100"}`}>
        <p className="text-[11px] font-medium uppercase tracking-[0.18em] text-muted">SprintMind</p>
        <p className="-mt-0.5 text-sm font-semibold text-slate-900">AI Workspace</p>
      </div>
    </div>
  );
}

function TopBrand() {
  return (
    <div className="pointer-events-none absolute left-1/2 -translate-x-1/2">
      <div className="rounded-full border border-line bg-white px-4 py-1.5 shadow-sm">
        <div className="leading-tight text-center">
          <p className="text-[10px] font-medium uppercase tracking-[0.2em] text-muted">SprintMind</p>
          <p className="text-xs font-semibold text-slate-900">AI Workspace</p>
        </div>
      </div>
    </div>
  );
}

function IconChevron({ open }: { open: boolean }) { return <svg className={`h-4 w-4 transition-transform duration-200 ${open ? "rotate-90" : ""}`} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M9 6l6 6-6 6" /></svg>; }
function IconMenu() { return <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 6h16M4 12h16M4 18h16" /></svg>; }
function IconPanelCollapse() { return <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="4" width="18" height="16" rx="2" /><path d="M9 4v16M13 9l-3 3 3 3" /></svg>; }
function IconPanelExpand() { return <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="4" width="18" height="16" rx="2" /><path d="M9 4v16M11 9l3 3-3 3" /></svg>; }
function IconLogout() { return <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" /><path d="M16 17l5-5-5-5" /><path d="M21 12H9" /></svg>; }

export function AppShell({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname() ?? "";
  const isPublicBarePage =
    pathname === "/" ||
    pathname.startsWith("/auth/login") ||
    pathname.startsWith("/auth/register") ||
    pathname.startsWith("/auth/forgot-password") ||
    pathname.startsWith("/auth/reset-password");
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [expanded, setExpanded] = useState<Record<string, boolean>>({ Onboarding: true, Jira: true, Issues: true });

  const onLogout = async () => {
    try {
      await logout();
    } catch {
      // noop
    }
    if (typeof window !== "undefined") {
      localStorage.removeItem("accessToken");
      document.cookie = "accessToken=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
    }
    router.push("/auth/login");
    router.refresh();
  };

  if (isPublicBarePage) {
    return <div className="min-h-screen">{children}</div>;
  }

  const sidebarWidth = sidebarCollapsed ? "lg:w-[84px]" : "lg:w-[280px]";
  const contentOffset = sidebarCollapsed ? "lg:pl-[100px]" : "lg:pl-[296px]";

  const renderNav = () => (
    <nav className="space-y-1">
      {navItems.map((item) => {
        const activeMain = item.href ? pathname === item.href || pathname.startsWith(`${item.href}/`) : item.children?.some((c) => pathname === c.href || pathname.startsWith(`${c.href}/`));

        if (item.children?.length) {
          const isOpen = expanded[item.label] ?? false;
          return (
            <div key={item.label} className="rounded-xl border border-line bg-white transition-colors duration-200">
              <button type="button" onClick={() => setExpanded((prev) => ({ ...prev, [item.label]: !isOpen }))} className={`flex w-full items-center justify-between px-3 py-2 text-left text-sm ${activeMain ? "text-brand" : "text-slate-700"}`}>
                <span className="flex items-center gap-2 font-medium"><span className="shrink-0">{item.icon}</span><span className={`transition-all duration-200 ${sidebarCollapsed ? "w-0 overflow-hidden opacity-0" : "opacity-100"}`}>{item.label}</span></span>
                {!sidebarCollapsed ? <IconChevron open={isOpen} /> : null}
              </button>
              <div className={`grid transition-all duration-200 ${isOpen && !sidebarCollapsed ? "grid-rows-[1fr]" : "grid-rows-[0fr]"}`}>
                <div className="overflow-hidden border-t border-line"><div className="p-1">{item.children.map((child) => {
                  const active = pathname === child.href || pathname.startsWith(`${child.href}/`);
                  return <Link key={child.href} href={child.href} className={`block rounded-lg px-2 py-2 text-sm ${active ? "bg-blue-50 text-brand" : "text-slate-600 hover:bg-slate-50"}`} onClick={() => setMobileOpen(false)}>{child.label}</Link>;
                })}</div></div>
              </div>
            </div>
          );
        }

        return (
          <Link key={item.label} href={item.href ?? "#"} className={`block rounded-xl border border-line bg-white px-3 py-2 text-sm font-medium ${activeMain ? "text-brand" : "text-slate-700 hover:bg-slate-50"}`} onClick={() => setMobileOpen(false)}>
            <span className="flex items-center gap-2"><span className="shrink-0">{item.icon}</span><span className={`transition-all duration-200 ${sidebarCollapsed ? "w-0 overflow-hidden opacity-0" : "opacity-100"}`}>{item.label}</span></span>
          </Link>
        );
      })}
    </nav>
  );

  return (
    <div className="min-h-screen">
      <aside className={`fixed left-0 top-0 z-30 hidden h-screen overflow-y-auto border-r border-line bg-base p-3 transition-all duration-300 ${sidebarWidth} lg:block`}>
        <div className="mb-3 grid h-8 w-8 place-items-center rounded-lg bg-brand text-xs font-bold text-white">SM</div>
        {renderNav()}
      </aside>

      <header className={`sticky top-0 z-20 border-b border-line bg-white/90 backdrop-blur transition-all duration-300 ${contentOffset}`}>
        <div className="relative flex h-16 items-center justify-between gap-3 px-4 sm:px-6">
          <TopBrand />
          <div className="flex items-center gap-2">
            <button className="btn !px-3 !py-2 lg:hidden" onClick={() => setMobileOpen((v) => !v)} type="button" aria-label="Open menu"><IconMenu /></button>
            <button className="btn !px-3 !py-2 hidden lg:inline-flex" onClick={() => setSidebarCollapsed((v) => !v)} type="button" aria-label="Toggle sidebar">{sidebarCollapsed ? <IconPanelExpand /> : <IconPanelCollapse />}</button>
            <div className="hidden text-sm text-muted md:block">Workspace</div>
          </div>
          <div className="flex items-center gap-2">
            <div className="hidden rounded-full border border-line bg-slate-50 px-3 py-1 text-sm text-slate-700 sm:block">Mustahid Hasan</div>
            <Link href="/settings" className="btn !py-2" aria-label="Settings">{icons.settings}</Link>
            <button className="btn !py-2" type="button" aria-label="Logout" onClick={onLogout}><IconLogout /></button>
          </div>
        </div>
      </header>

      <div className={`px-4 py-4 transition-all duration-300 sm:px-6 ${contentOffset}`}>
        {mobileOpen ? (
          <div className="fixed inset-0 z-40 bg-slate-900/30 lg:hidden" onClick={() => setMobileOpen(false)}>
            <aside className="h-full w-[280px] overflow-y-auto border-r border-line bg-base p-3" onClick={(e) => e.stopPropagation()}>
              <BrandMark collapsed={false} />
              {renderNav()}
            </aside>
          </div>
        ) : null}
        <main className="min-w-0">{children}</main>
      </div>
    </div>
  );
}
