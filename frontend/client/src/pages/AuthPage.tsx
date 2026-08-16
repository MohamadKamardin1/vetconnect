/* Sunlit Credential authentication: private access is framed as a calm, explicit handoff into a protected care space. All care and safety language resolves through the shared locale context. */
import { ArrowRight, LockKeyhole, ShieldCheck, Sparkles } from "lucide-react";
import { FormEvent, useState } from "react";
import { Link, useLocation } from "wouter";
import { BrandMark } from "@/components/BrandMark";
import { useLanguage } from "@/contexts/LanguageContext";
import { api } from "@/lib/api";

export function AuthPage({ mode }: { mode: "login" | "register" }) {
  const [, navigate] = useLocation();
  const { t } = useLanguage();
  const [state, setState] = useState<"idle" | "loading" | "error">("idle");
  const [error, setError] = useState("");

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    setState("loading");
    setError("");

    if (mode === "register") {
      const fullName = String(data.get("name") ?? "").trim().split(/\s+/);
      const result = await api.register({
        email: String(data.get("email")),
        phone_number: String(data.get("phone") || ""),
        first_name: fullName[0] || "Member",
        last_name: fullName.slice(1).join(" ") || "",
        password: String(data.get("password")),
      });
      if (result.data) {
        navigate(`/verify-email?email=${encodeURIComponent(result.data.email)}`);
      } else {
        setState("error");
        setError(t(result.error ?? "We could not create your account."));
      }
      return;
    }

    const result = await api.login(String(data.get("email")), String(data.get("password")));
    if (result.data) {
      localStorage.setItem("vetkonnect_access_token", result.data.access);
      localStorage.setItem("vetkonnect_refresh_token", result.data.refresh);
      navigate("/portal/overview");
    } else {
      setState("error");
      setError(t(result.error ?? "We could not sign you in."));
    }
  };

  const isLogin = mode === "login";

  return <main className="grid min-h-dvh bg-[#f8f2e6] lg:h-dvh lg:min-h-0 lg:grid-cols-[.9fr_1.1fr] lg:overflow-hidden">
    <section className="relative hidden overflow-hidden bg-[#244c3d] p-12 text-[#fffaf0] lg:block lg:p-9 xl:p-12">
      <div className="absolute inset-0 contour opacity-20" />
      <div className="relative flex h-full max-w-md flex-col">
        <BrandMark />
        <div className="my-auto">
          <p className="eyebrow !text-[#e5c66f]">{t("Protected care space")}</p>
          <h1 className="display mt-5 text-6xl leading-[.92]">{t("Your animal’s story deserves more than a scattered note.")}</h1>
          <p className="mt-6 leading-7 text-[#d9e2d8]">{t("A private space for care records, chosen access, professional messages, and the practical work behind a healthier routine.")}</p>
        </div>
        <div className="flex items-center gap-3 text-xs font-bold text-[#d9e2d8]"><ShieldCheck size={18} className="text-[#e7c56d]" />{t("Role-aware access protects the data you entrust to VetKonnect.")}</div>
      </div>
    </section>
    <section className="flex items-center justify-center p-5 sm:p-10 lg:min-h-0 lg:p-6 xl:p-8">
      <div className="w-full max-w-md lg:max-w-[31rem]">
        <div className="lg:hidden"><BrandMark /></div>
        <p className="eyebrow mt-12 lg:mt-0">{t(isLogin ? "Welcome back" : "Create your account")}</p>
        <h2 className="display mt-4 text-5xl leading-[.95] text-[#244c3d] lg:mt-3 lg:text-[2.6rem] xl:text-[2.85rem]">{t(isLogin ? "Sign in to care, clearly." : "Start with one calm account.")}</h2>
        <p className="mt-4 text-sm leading-6 text-[#68776e] lg:mt-2 lg:leading-5">{t(isLogin ? "Use the credentials you created for your VetKonnect account." : "There is no role to choose here. After sign-up, the profile studio helps you select or switch the workspace that fits your work.")}</p>
        {!isLogin && <div className="mt-5 flex gap-3 rounded-2xl bg-[#fff6df] p-4 text-xs font-bold leading-5 text-[#665431] lg:mt-3 lg:rounded-xl lg:p-3 lg:text-[11px] lg:leading-4"><Sparkles size={16} className="shrink-0 text-[#a87822]" />{t("You can return to the profile studio whenever your responsibilities change.")}</div>}
        <form className={`mt-8 grid gap-4 lg:mt-4 lg:gap-x-3 lg:gap-y-2.5 ${!isLogin ? "lg:grid-cols-2" : ""}`} onSubmit={submit}>
          {!isLogin && <>
            <label className="grid gap-2 text-xs font-extrabold text-[#405b4c] lg:gap-1.5">{t("Full name")}<input required name="name" className="h-13 rounded-xl border border-[#dfcfaa] bg-white px-4 text-sm outline-none focus:border-[#b78a38] lg:h-11" placeholder={t("Your full name")} /></label>
            <label className="grid gap-2 text-xs font-extrabold text-[#405b4c] lg:gap-1.5">{t("Phone number")} <span className="font-medium text-[#819087]">{t("(optional)")}</span><input name="phone" className="h-13 rounded-xl border border-[#dfcfaa] bg-white px-4 text-sm outline-none focus:border-[#b78a38] lg:h-11" placeholder="+255…" /></label>
          </>}
          <label className="grid gap-2 text-xs font-extrabold text-[#405b4c] lg:gap-1.5">{t("Email address")}<input required type="email" name="email" className="h-13 rounded-xl border border-[#dfcfaa] bg-white px-4 text-sm outline-none focus:border-[#b78a38] lg:h-11" placeholder="you@example.com" /></label>
          <label className="grid gap-2 text-xs font-extrabold text-[#405b4c] lg:gap-1.5">{t("Password")}<input required minLength={isLogin ? 8 : 12} type="password" name="password" className="h-13 rounded-xl border border-[#dfcfaa] bg-white px-4 text-sm outline-none focus:border-[#b78a38] lg:h-11" placeholder={t(isLogin ? "Your password" : "At least 12 characters")} /></label>
          {state === "error" && <p className={`rounded-xl bg-[#fff1eb] px-4 py-3 text-xs font-bold text-[#a04d33] ${!isLogin ? "lg:col-span-2 lg:py-2" : ""}`}>{error}</p>}
          <button disabled={state === "loading"} className={`ink-button mt-2 disabled:opacity-60 lg:mt-0 lg:py-2.5 ${!isLogin ? "lg:col-span-2" : ""}`}>{state === "loading" ? t(isLogin ? "Signing in…" : "Creating account…") : t(isLogin ? "Sign in securely" : "Continue to email verification")}<ArrowRight size={16} /></button>
        </form>
        <p className="mt-6 text-center text-sm font-semibold text-[#68776e] lg:mt-3 lg:text-[13px]">{isLogin ? <>{t("New to VetKonnect?")} <Link href="/register" className="font-extrabold text-[#9e752a]">{t("Create an account")}</Link></> : <>{t("Already have an account?")} <Link href="/login" className="font-extrabold text-[#9e752a]">{t("Sign in")}</Link></>}</p>
        <p className="mt-8 flex items-center justify-center gap-2 text-center text-[11px] leading-5 text-[#889187] lg:mt-3 lg:leading-4"><LockKeyhole size={13} />{t("Please use a private device when viewing animal records.")}</p>
      </div>
    </section>
  </main>;
}
