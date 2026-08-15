/* Sunlit Credential workspace state: roles are chosen after account creation and remain locally switchable until the backend profile assignment is connected. */
import { useEffect, useState } from "react";
import { Building2, HeartPulse, ShieldCheck, ShoppingBag, Stethoscope } from "lucide-react";

export type WorkspaceRole = "OWNER" | "VETERINARIAN" | "CLINIC" | "VENDOR" | "ADMIN";

export const roleOptions: Array<{ key: WorkspaceRole; label: string; short: string; copy: string; icon: typeof HeartPulse; accent: string }> = [
  { key: "OWNER", label: "Animal owner", short: "Owner", copy: "Keep animal details, care records, and trusted connections together.", icon: HeartPulse, accent: "#315d49" },
  { key: "VETERINARIAN", label: "Veterinary doctor", short: "Doctor", copy: "Manage professional readiness, credentials, care relationships, and follow-up.", icon: Stethoscope, accent: "#9b742c" },
  { key: "CLINIC", label: "Clinic workspace", short: "Clinic", copy: "Coordinate services, team readiness, and an accountable local presence.", icon: Building2, accent: "#735830" },
  { key: "VENDOR", label: "Care supplier", short: "Vendor", copy: "Prepare a responsible catalogue, stock controls, and customer enquiries.", icon: ShoppingBag, accent: "#7b5435" },
  { key: "ADMIN", label: "Network administrator", short: "Admin", copy: "Oversee verification, reports, operations, and platform integrity.", icon: ShieldCheck, accent: "#244c3d" },
];

export const getRole = (): WorkspaceRole => (localStorage.getItem("vetkonnect_active_role") as WorkspaceRole) || "OWNER";
export const setRole = (role: WorkspaceRole) => {
  localStorage.setItem("vetkonnect_active_role", role);
  window.dispatchEvent(new Event("vetkonnect-role-change"));
};
export const getRoleMeta = (role: WorkspaceRole) => roleOptions.find((option) => option.key === role) ?? roleOptions[0];

export function useActiveRole() {
  const [role, setRoleState] = useState<WorkspaceRole>(() => getRole());
  useEffect(() => {
    const update = () => setRoleState(getRole());
    window.addEventListener("vetkonnect-role-change", update);
    window.addEventListener("storage", update);
    return () => { window.removeEventListener("vetkonnect-role-change", update); window.removeEventListener("storage", update); };
  }, []);
  return { role, meta: getRoleMeta(role), switchRole: setRole };
}
