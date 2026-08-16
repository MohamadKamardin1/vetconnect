/* Sunlit Credential verification: a short, deliberate proof step before private account access. */
import { ArrowLeft, ArrowRight, CheckCircle2, MailCheck, RefreshCw, ShieldCheck } from "lucide-react";
import { ClipboardEvent, KeyboardEvent, useEffect, useRef, useState } from "react";
import { Link, useLocation } from "wouter";
import { BrandMark } from "@/components/BrandMark";
import { useLanguage } from "@/contexts/LanguageContext";
import { api } from "@/lib/api";

const CODE_LENGTH = 6;

export function VerifyEmailPage() {
  const [, navigate] = useLocation();
  const { t } = useLanguage();
  const [email] = useState(() => new URLSearchParams(window.location.search).get("email")?.trim() ?? "");
  const [digits, setDigits] = useState<string[]>(Array(CODE_LENGTH).fill(""));
  const [state, setState] = useState<"idle" | "verifying" | "error">("idle");
  const [message, setMessage] = useState("");
  const [resending, setResending] = useState(false);
  const [countdown, setCountdown] = useState(60);
  const inputs = useRef<Array<HTMLInputElement | null>>([]);
  const code = digits.join("");

  useEffect(() => {
    if (countdown <= 0) return;
    const timer = window.setInterval(() => setCountdown((seconds) => Math.max(0, seconds - 1)), 1000);
    return () => window.clearInterval(timer);
  }, [countdown]);

  const submit = async (nextCode = code) => {
    if (!email || nextCode.length !== CODE_LENGTH || state === "verifying") return;
    setState("verifying");
    setMessage("");
    const result = await api.verifyEmail(email, nextCode);
    if (!result.data) {
      setState("error");
      setMessage(t(result.error ?? "That code is invalid or has expired. Request a new code and try again."));
      setDigits(Array(CODE_LENGTH).fill(""));
      inputs.current[0]?.focus();
      return;
    }
    localStorage.setItem("vetkonnect_access_token", result.data.access);
    localStorage.setItem("vetkonnect_refresh_token", result.data.refresh);
    navigate("/onboarding");
  };

  const setDigit = (index: number, value: string) => {
    const digit = value.replace(/\D/g, "").slice(-1);
    const next = [...digits];
    next[index] = digit;
    setDigits(next);
    setState("idle");
    setMessage("");
    if (digit && index < CODE_LENGTH - 1) inputs.current[index + 1]?.focus();
    const nextCode = next.join("");
    if (nextCode.length === CODE_LENGTH && !next.includes("")) void submit(nextCode);
  };

  const handlePaste = (event: ClipboardEvent<HTMLInputElement>) => {
    const pasted = event.clipboardData.getData("text").replace(/\D/g, "").slice(0, CODE_LENGTH);
    if (!pasted) return;
    event.preventDefault();
    const next = Array.from({ length: CODE_LENGTH }, (_, index) => pasted[index] ?? "");
    setDigits(next);
    setState("idle");
    setMessage("");
    const finalIndex = Math.min(pasted.length, CODE_LENGTH) - 1;
    inputs.current[finalIndex]?.focus();
    if (pasted.length === CODE_LENGTH) void submit(pasted);
  };

  const handleKeyDown = (index: number, event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Backspace" && !digits[index] && index > 0) inputs.current[index - 1]?.focus();
    if (event.key === "ArrowLeft" && index > 0) inputs.current[index - 1]?.focus();
    if (event.key === "ArrowRight" && index < CODE_LENGTH - 1) inputs.current[index + 1]?.focus();
  };

  const resend = async () => {
    if (!email || countdown > 0 || resending) return;
    setResending(true);
    setMessage("");
    const result = await api.resendEmailVerification(email);
    setResending(false);
    if (!result.data) {
      setState("error");
      setMessage(t(result.error ?? "We could not send a new code just yet. Please try again shortly."));
      return;
    }
    setDigits(Array(CODE_LENGTH).fill(""));
    setCountdown(result.data.retry_after_seconds ?? 60);
    setState("idle");
    setMessage(t("A new code is on its way to your email."));
    inputs.current[0]?.focus();
  };

  if (!email) {
    return <main className="flex min-h-dvh items-center justify-center bg-[#f8f2e6] p-5"><div className="w-full max-w-md rounded-3xl bg-white p-8 shadow-[0_22px_60px_rgba(46,67,53,.12)]"><BrandMark /><h1 className="display mt-10 text-4xl text-[#244c3d]">{t("Start your verification")}</h1><p className="mt-4 leading-6 text-[#68776e]">{t("Create your account first, then we will send your six-digit code.")}</p><Link href="/register" className="ink-button mt-8">{t("Create an account")}<ArrowRight size={16} /></Link></div></main>;
  }

  return <main className="grid min-h-dvh bg-[#f8f2e6] lg:h-dvh lg:min-h-0 lg:grid-cols-[.9fr_1.1fr] lg:overflow-hidden">
    <section className="relative hidden overflow-hidden bg-[#244c3d] p-12 text-[#fffaf0] lg:block lg:p-9 xl:p-12"><div className="absolute inset-0 contour opacity-20" /><div className="relative flex h-full max-w-md flex-col"><BrandMark /><div className="my-auto"><p className="eyebrow !text-[#e5c66f]">{t("One small security step")}</p><h1 className="display mt-5 text-6xl leading-[.92]">{t("Your care space starts with a verified email.")}</h1><p className="mt-6 leading-7 text-[#d9e2d8]">{t("This protects your private account before you add animal records, choose a profile, or connect with care.")}</p></div><div className="flex items-center gap-3 text-xs font-bold text-[#d9e2d8]"><ShieldCheck size={18} className="text-[#e7c56d]" />{t("Your code is private. VetKonnect staff will never ask for it.")}</div></div></section>
    <section className="flex items-center justify-center p-5 sm:p-10 lg:min-h-0 lg:p-6 xl:p-8"><div className="w-full max-w-md lg:max-w-[29rem]"><div className="lg:hidden"><BrandMark /></div><div className="mt-12 lg:mt-0"><span className="inline-flex size-12 items-center justify-center rounded-2xl bg-[#fff1cf] text-[#a87822]"><MailCheck size={24} /></span><p className="eyebrow mt-6">{t("Email verification")}</p><h2 className="display mt-3 text-5xl leading-[.95] text-[#244c3d] lg:text-[2.7rem]">{t("Check your inbox.")}</h2><p className="mt-4 text-sm leading-6 text-[#68776e]">{t("We sent a six-digit code to")} <strong className="font-extrabold text-[#244c3d]">{email}</strong>. {t("Enter it below to finish creating your account.")}</p></div>
      <div className="mt-8"><p className="text-xs font-extrabold text-[#405b4c]">{t("Six-digit code")}</p><div className="mt-3 flex gap-2 sm:gap-3" role="group" aria-label={t("Six-digit verification code")}>{digits.map((digit, index) => <input key={index} ref={(node) => { inputs.current[index] = node; }} value={digit} onChange={(event) => setDigit(index, event.target.value)} onPaste={handlePaste} onKeyDown={(event) => handleKeyDown(index, event)} inputMode="numeric" autoComplete={index === 0 ? "one-time-code" : "off"} aria-label={`${t("Digit")} ${index + 1} ${t("of")} ${CODE_LENGTH}`} className="h-14 min-w-0 flex-1 rounded-xl border border-[#dfcfaa] bg-white text-center text-xl font-extrabold tracking-[.05em] text-[#244c3d] outline-none focus:border-[#b78a38] focus:ring-2 focus:ring-[#e7c56d]/40" maxLength={1} />)}</div></div>
      <p className={`mt-4 min-h-5 text-xs font-bold ${state === "error" ? "text-[#a04d33]" : "text-[#68776e]"}`} aria-live="polite">{message}</p>
      <button onClick={() => void submit()} disabled={state === "verifying" || code.length !== CODE_LENGTH} className="ink-button mt-4 w-full disabled:opacity-60">{state === "verifying" ? t("Verifying your code…") : t("Verify and continue")}<CheckCircle2 size={16} /></button>
      <div className="mt-5 flex items-center justify-between gap-3 text-xs font-bold text-[#68776e]"><Link href="/register" className="inline-flex items-center gap-1 hover:text-[#244c3d]"><ArrowLeft size={14} />{t("Use another email")}</Link><button onClick={() => void resend()} disabled={countdown > 0 || resending} className="inline-flex items-center gap-1 text-[#9e752a] disabled:text-[#9a9d98]"><RefreshCw size={14} className={resending ? "animate-spin" : ""} />{resending ? t("Sending…") : countdown > 0 ? `${t("Resend code in")} ${countdown}s` : t("Resend code")}</button></div>
      <p className="mt-8 flex items-center justify-center gap-2 text-center text-[11px] leading-5 text-[#889187]"><ShieldCheck size={13} />{t("The code expires in 10 minutes and has limited attempts for your safety.")}</p>
    </div></section>
  </main>;
}
