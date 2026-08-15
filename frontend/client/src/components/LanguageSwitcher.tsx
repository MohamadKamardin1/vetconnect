/* Sunlit Credential language control: compact, keyboard-operable proof that English and Kiswahili carry equal product meaning. */
import { Languages } from "lucide-react";
import { useLanguage } from "@/contexts/LanguageContext";
import type { Locale } from "@/lib/i18n";

export function LanguageSwitcher({ dark = false, compact = false }: { dark?: boolean; compact?: boolean }) {
  const { locale, setLocale, t } = useLanguage();
  const select = (next: Locale) => setLocale(next);
  const base = dark ? "border-white/20 bg-white/10 text-white" : "border-[#e2d3b2] bg-white text-[#244c3d]";
  const active = dark ? "bg-[#f2d48d] text-[#244c3d]" : "bg-[#244c3d] text-white";
  return <div className={`inline-flex items-center gap-1 rounded-full border p-1 ${base}`} role="group" aria-label={t("Choose language")}>
    {!compact && <Languages size={14} className="ml-1.5 opacity-70" aria-hidden="true"/>}
    {(["en", "sw"] as Locale[]).map((item) => <button key={item} type="button" onClick={() => select(item)} aria-pressed={locale === item} className={`rounded-full px-2.5 py-1.5 text-[10px] font-extrabold tracking-[.08em] transition ${locale === item ? active : "opacity-75 hover:opacity-100"}`}>{item === "en" ? "EN" : "SW"}</button>)}
  </div>;
}
