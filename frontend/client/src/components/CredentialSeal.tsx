/* Sunlit Credential proof motif: this is the recurring badge mark for verified status and protected, accountable care actions. */
export function CredentialSeal({ size = 20, className = "" }: { size?: number; className?: string }) {
  return <span className={`inline-grid shrink-0 place-items-center rounded-full bg-[#f4e6bd] ring-1 ring-[#d2b46b]/45 ${className}`} style={{ width: size + 6, height: size + 6 }} aria-label="VetKonnect credential seal"><img src="/manus-storage/vetkonnect-logo-seal_11196867.png" alt="" style={{ width: size, height: size }} className="object-contain"/></span>;
}
