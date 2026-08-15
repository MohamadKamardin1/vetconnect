/* Sunlit Credential locale context: language is a user-controlled local preference, never a substitute for consent, role, or clinical controls. */
import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { getStoredLocale, localizeText, type Locale } from "@/lib/i18n";

type LanguageContextValue = { locale: Locale; setLocale: (locale: Locale) => void; t: (value: string) => string };
const LanguageContext = createContext<LanguageContextValue | null>(null);

function translateDom(root: HTMLElement, locale: Locale) {
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  const textNodes: Text[] = [];
  while (walker.nextNode()) textNodes.push(walker.currentNode as Text);
  textNodes.forEach((node) => { const localized = localizeText(node.nodeValue ?? "", locale); if (localized !== node.nodeValue) node.nodeValue = localized; });
  root.querySelectorAll<HTMLElement>("[placeholder], [aria-label], [title]").forEach((element) => {
    ["placeholder", "aria-label", "title"].forEach((attribute) => {
      const value = element.getAttribute(attribute); if (!value) return;
      const localized = localizeText(value, locale); if (localized !== value) element.setAttribute(attribute, localized);
    });
  });
}

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [locale, setLocaleState] = useState<Locale>(getStoredLocale);
  const setLocale = useCallback((nextLocale: Locale) => setLocaleState(nextLocale), []);
  const t = useCallback((value: string) => localizeText(value, locale), [locale]);
  useEffect(() => {
    document.documentElement.lang = locale === "sw" ? "sw" : "en";
    document.documentElement.dataset.locale = locale;
    document.title = locale === "sw" ? "VetKonnect | Kiunganishi cha Huduma za Wanyama" : "VetKonnect | Connected Veterinary Care";
    window.localStorage.setItem("vetkonnect_locale", locale);
    const root = document.getElementById("root"); if (!root) return;
    translateDom(root, locale);
    const observer = new MutationObserver((mutations) => mutations.forEach((mutation) => {
      if (mutation.type === "characterData") translateDom(root, locale);
      mutation.addedNodes.forEach((node) => { if (node.nodeType === Node.ELEMENT_NODE) translateDom(node as HTMLElement, locale); });
    }));
    observer.observe(root, { childList: true, subtree: true, characterData: true });
    return () => observer.disconnect();
  }, [locale]);
  const value = useMemo(() => ({ locale, setLocale, t }), [locale, setLocale, t]);
  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>;
}

export function useLanguage() { const context = useContext(LanguageContext); if (!context) throw new Error("useLanguage must be used inside LanguageProvider"); return context; }
