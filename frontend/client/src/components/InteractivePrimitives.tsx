/* Sunlit Credential interaction primitives: paper surfaces acquire subtle, accessibility-safe depth only through direct user intent. */
import { motion } from "framer-motion";
import { useState, type CSSProperties, type ReactNode } from "react";

export function TiltSurface({ children, className = "", intensity = 6 }: { children: ReactNode; className?: string; intensity?: number }) {
  const [style, setStyle] = useState<React.CSSProperties>({});
  return <motion.div className={`tilt-surface ${className}`} style={style} onMouseMove={(event) => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const box = event.currentTarget.getBoundingClientRect();
    const rotateY = ((event.clientX - box.left) / box.width - 0.5) * intensity;
    const rotateX = ((event.clientY - box.top) / box.height - 0.5) * -intensity;
    setStyle({ transform: `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-3px)` });
  }} onMouseLeave={() => setStyle({})} transition={{ type: "spring", stiffness: 260, damping: 22 }}>{children}</motion.div>;
}

export function OrbitProgress({ value, label, detail }: { value: number; label: string; detail: string }) {
  const dash = `${Math.max(0, Math.min(value, 100))} 100`;
  return <div className="orbit-wrap" aria-label={`${label}: ${value}%`}><svg viewBox="0 0 42 42" className="h-24 w-24 -rotate-90" aria-hidden="true"><circle cx="21" cy="21" r="16" fill="none" stroke="#efe4cd" strokeWidth="3"/><circle cx="21" cy="21" r="16" fill="none" stroke="#b78a38" strokeWidth="3" strokeLinecap="round" pathLength="100" strokeDasharray={dash}/></svg><div className="orbit-copy"><strong>{value}%</strong><span>{label}</span></div><p>{detail}</p></div>;
}

export function SectionReveal({ children, className = "", style }: { children: ReactNode; className?: string; style?: CSSProperties }) {
  return <motion.section style={style} className={className} initial={{ opacity: 0, y: 18 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.15 }} transition={{ duration: 0.45, ease: [0.23, 1, 0.32, 1] }}>{children}</motion.section>;
}
