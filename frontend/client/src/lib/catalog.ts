/* Sunlit Credential information architecture: the same calm vocabulary organises public discovery and every role-specific workspace. */
import { Activity, BookOpen, Building2, CircleDollarSign, ClipboardCheck, HeartPulse, MessagesSquare, ShieldCheck, ShoppingBag, Stethoscope, UsersRound } from "lucide-react";

export const services = [
  { icon: Stethoscope, title: "Verified professionals", description: "Choose from KYC-reviewed veterinary doctors and paraprofessionals." },
  { icon: Building2, title: "Clinics near you", description: "Compare accessible clinics, services, and practical directions." },
  { icon: ShoppingBag, title: "Care marketplace", description: "Source animal-health essentials from accountable local vendors." },
  { icon: HeartPulse, title: "Practical tools", description: "Use feed and disease-support tools with clear clinical boundaries." },
];

export const workspaceLinks = [
  { href: "/portal/overview", icon: Activity, label: "Overview" },
  { href: "/portal/animals", icon: HeartPulse, label: "Animals & records" },
  { href: "/portal/messages", icon: MessagesSquare, label: "Secure messages" },
  { href: "/portal/community", icon: UsersRound, label: "Community" },
  { href: "/portal/credentials", icon: ShieldCheck, label: "Credentials & badge" },
  { href: "/portal/marketplace", icon: ShoppingBag, label: "Marketplace" },
  { href: "/portal/tools", icon: BookOpen, label: "Care tools" },
  { href: "/portal/billing", icon: CircleDollarSign, label: "Billing" },
  { href: "/portal/kyc", icon: ClipboardCheck, label: "KYC centre" },
];

export const journeyCards = [
  { number: "01", title: "Find care that meets the moment", body: "Search specialist, clinic, location, and availability before you need to make a difficult decision.", href: "/find-care" },
  { number: "02", title: "Keep records purposeful and private", body: "Animal records and access grants are managed through your authenticated workspace — never through a public profile.", href: "/portal/animals" },
  { number: "03", title: "Build a healthier routine", body: "Move from practical guidance to trusted supplies and follow-up, in one connected care network.", href: "/marketplace" },
];
