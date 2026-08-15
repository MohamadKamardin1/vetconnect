/* Sunlit Credential interaction system: route changes glide to the next reading position while anchors retain room beneath the site header. */
import { useEffect, useRef } from "react";
import { useLocation } from "wouter";

function preferredScrollBehavior(): ScrollBehavior {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth";
}

function scrollToHash(behavior: ScrollBehavior) {
  const rawHash = window.location.hash.slice(1);
  if (!rawHash) return false;

  const target = document.getElementById(decodeURIComponent(rawHash));
  if (!target) return false;

  target.scrollIntoView({ behavior, block: "start" });
  return true;
}

export function ScrollManager() {
  const [location] = useLocation();
  const previousLocation = useRef(location);

  useEffect(() => {
    const frame = window.requestAnimationFrame(() => {
      const behavior = preferredScrollBehavior();
      const movedToAnchor = scrollToHash(behavior);

      if (!movedToAnchor && previousLocation.current !== location) {
        window.scrollTo({ top: 0, left: 0, behavior });
      }

      previousLocation.current = location;
    });

    return () => window.cancelAnimationFrame(frame);
  }, [location]);

  useEffect(() => {
    const handleHashChange = () => scrollToHash(preferredScrollBehavior());
    window.addEventListener("hashchange", handleHashChange);
    return () => window.removeEventListener("hashchange", handleHashChange);
  }, []);

  return null;
}
