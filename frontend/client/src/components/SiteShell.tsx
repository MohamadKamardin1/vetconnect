/* Sunlit Credential navigation: a polished, high-contrast service rail gives every page a clear route into care or the secure workspace. */
import { Menu, Search, X } from "lucide-react";
import { useState } from "react";
import { Link, useLocation } from "wouter";
import { BrandMark } from "./BrandMark";

const links = [["Find care", "/find-care"], ["For professionals", "/professionals"], ["Marketplace", "/marketplace"], ["Community", "/community"], ["Care tools", "/tools"]] as const;

export function SiteShell({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(false); const [location] = useLocation();
  return <div className="min-h-screen overflow-x-clip bg-[#fcfaf6]">
    <div className="border-b border-[#eadfca] bg-[#244c3d] px-5 py-2.5 text-center text-[10px] font-bold tracking-[0.12em] text-[#fffaf0] sm:text-xs">CARE, CONNECTED — FOR TANZANIA & ZANZIBAR</div>
    <header className="sticky top-0 z-40 border-b border-[#eadfca]/80 bg-[#fcfaf6]/95 backdrop-blur-xl">
      <div className="container flex h-[76px] items-center justify-between gap-5">
        <BrandMark />
        <nav className="hidden items-center gap-6 lg:flex">{links.map(([label, href]) => <Link key={href} href={href} className={`text-sm font-bold transition hover:text-[#b78a38] ${location === href ? "text-[#b78a38]" : "text-[#365747]"}`}>{label}</Link>)}</nav>
        <div className="hidden items-center gap-3 sm:flex"><Link href="/login" className="text-sm font-bold text-[#244c3d]">Sign in</Link><Link href="/portal/overview" className="gold-button !px-4 !py-2.5">My care space</Link></div>
        <button className="grid h-11 w-11 place-items-center rounded-full border border-[#dfcfaa] text-[#244c3d] lg:hidden" onClick={() => setOpen(!open)} aria-label="Toggle navigation">{open ? <X size={20} /> : <Menu size={21} />}</button>
      </div>
      {open && <div className="container border-t border-[#eadfca] py-4 lg:hidden"><div className="grid gap-2">{links.map(([label, href]) => <Link key={href} href={href} onClick={() => setOpen(false)} className="rounded-xl px-3 py-3 font-bold text-[#244c3d] hover:bg-[#fff6e6]">{label}</Link>)}<Link href="/login" className="gold-button mt-2">Sign in to your care space</Link></div></div>}
    </header>
    {children}
    <footer className="border-t border-[#e7dcc7] bg-white"><div className="container grid gap-10 py-12 md:grid-cols-[1.25fr_.75fr_.75fr]">
      <div><BrandMark /><p className="mt-5 max-w-sm text-sm leading-7 text-[#617064]">A connected veterinary care network for animal owners, professionals, clinics, and accountable vendors across Tanzania and Zanzibar.</p></div>
      <div><p className="eyebrow !text-[9px]">Explore</p><div className="mt-4 grid gap-3 text-sm font-bold text-[#365747]"><Link href="/find-care">Find verified care</Link><Link href="/marketplace">Care marketplace</Link><Link href="/community">Community guidance</Link></div></div>
      <div><p className="eyebrow !text-[9px]">Safety</p><p className="mt-4 text-sm leading-7 text-[#617064]">Digital tools support care decisions but do not replace an in-person veterinary assessment when an animal may be ill or in danger.</p></div>
    </div><div className="border-t border-[#eee4d2]"><div className="container flex flex-col gap-2 py-4 text-xs font-medium text-[#788179] sm:flex-row sm:justify-between"><span>© 2026 VetKonnect Tanzania & Zanzibar</span><span>Privacy · Terms · Clinical safety</span></div></div></footer>
  </div>;
}

export function SearchStrip() { return <div className="relative"><Search className="absolute left-4 top-1/2 -translate-y-1/2 text-[#96763a]" size={18}/><input aria-label="Search care" placeholder="Search professional, clinic, or service" className="h-14 w-full rounded-2xl border border-[#e2d3b2] bg-white pl-12 pr-4 text-sm font-semibold text-[#244c3d] shadow-[0_16px_30px_-24px_rgba(44,76,61,.5)] outline-none transition focus:border-[#b78a38]" /></div>; }
