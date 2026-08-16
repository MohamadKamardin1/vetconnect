/* Sunlit Credential brand component: the gold seal stays distinct and legible across public and protected product contexts. */
import { Link } from "wouter";

export function BrandMark({ compact = false, tone = "light" }: { compact?: boolean; tone?: "light" | "dark" }) {
  return <Link href="/" className="flex items-center gap-3" aria-label="VetKonnect home">
    <span className="grid h-10 w-10 place-items-center overflow-hidden rounded-[1rem] bg-[#f7edd7] ring-1 ring-[#d6b775]/70 shadow-[0_8px_18px_-12px_rgba(183,138,56,.8)]">
      <img src="/manus-storage/vetkonnect-logo-seal_11196867.png" alt="" className="h-9 w-9 object-contain" />
    </span>
    {!compact && <span className="leading-none"><span className={`block text-lg font-extrabold tracking-[-0.075em] ${tone === "dark" ? "text-[#fffaf0]" : "text-[#244c3d]"}`}>VetKonnect</span><span className="mt-1 block text-[8px] font-extrabold uppercase tracking-[0.19em] text-[#cda95b]">Veterinary care network</span></span>}
  </Link>;
}
