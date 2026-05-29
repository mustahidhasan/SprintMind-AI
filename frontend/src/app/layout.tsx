import type { Metadata } from "next";
import React from "react";

export const metadata: Metadata = {
  title: "SprintMind AI",
  description: "AI-assisted sprint planning and issue quality platform",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ fontFamily: "sans-serif", margin: 0, padding: "1.5rem" }}>{children}</body>
    </html>
  );
}
