import { useRef, useState, useEffect } from 'react';
import { MessageSquare, Trash2, X } from 'lucide-react';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';

gsap.registerPlugin(useGSAP);

function prefersReducedMotion() {
  return typeof window !== 'undefined'
    && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

export const FloatingSidebar = ({ isOpen, onClose, sessions, activeSessionId, onNewSession, onLoadSession, onDeleteSession }: any) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [mounted, setMounted] = useState(isOpen);

  useEffect(() => {
    if (isOpen) setMounted(true);
  }, [isOpen]);

  useGSAP(() => {
    const container = containerRef.current;
    if (!mounted || !container) return;

    const items = gsap.utils.toArray<HTMLElement>(container.querySelectorAll('.session-item'));
    gsap.killTweensOf([container, ...items]);

    if (prefersReducedMotion()) {
      gsap.set(container, { autoAlpha: isOpen ? 1 : 0, x: 0, scale: 1, clearProps: isOpen ? 'transform' : undefined });
      if (!isOpen) setMounted(false);
      return;
    }

    if (isOpen) {
      gsap.set(container, { willChange: 'transform, opacity' });
      const tl = gsap.timeline({
        defaults: { force3D: true, overwrite: 'auto' },
        onComplete: () => gsap.set(container, { clearProps: 'willChange' }),
      });
      tl.fromTo(container,
        { autoAlpha: 0, scale: 0.96, x: -16 },
        { autoAlpha: 1, scale: 1, x: 0, duration: 0.24, ease: 'power3.out' }
      );
      if (items.length) {
        tl.fromTo(items,
          { autoAlpha: 0, x: -8 },
          { autoAlpha: 1, x: 0, duration: 0.18, stagger: 0.03, ease: 'power2.out', clearProps: 'transform,opacity,visibility' },
          '-=0.14'
        );
      }
    } else {
      gsap.set(container, { willChange: 'transform, opacity' });
      gsap.to(container, {
        autoAlpha: 0,
        scale: 0.97,
        x: -12,
        duration: 0.16,
        ease: 'power2.out',
        force3D: true,
        overwrite: 'auto',
        onComplete: () => {
          gsap.set(container, { clearProps: 'transform,opacity,visibility,willChange' });
          setMounted(false);
        },
      });
    }
  }, { dependencies: [isOpen, mounted], scope: containerRef });

  if (!mounted) return null;

  return (
    <div ref={containerRef} className="absolute top-4 left-4 z-50 flex flex-col w-[260px] max-h-[calc(100vh-88px)] bg-black/40 backdrop-blur-md border border-white/10 rounded-2xl shadow-xl overflow-hidden text-white origin-top-left">
      <div className="p-3 border-b border-white/10 flex items-center justify-between">
        <button
          onClick={onNewSession}
          className="flex items-center justify-center gap-2 px-4 py-2 bg-white/20 text-white rounded-xl text-sm transition-colors duration-150 ease-[var(--ease-out)] hover:bg-white/30 shadow-sm press-scale"
        >
          <MessageSquare className="w-4 h-4" />
          新建对话
        </button>
        <button 
          onClick={onClose}
          className="p-2 text-white/70 hover:text-white rounded-full hover:bg-white/10 transition-colors press-scale"
        >
          <X className="w-5 h-5" />
        </button>
      </div>
      <div className="flex-1 overflow-y-auto p-2 scrollbar-thin">
        {sessions.length === 0 && (
          <div className="text-sm text-white/50 text-center py-6 px-2">暂无历史对话</div>
        )}
        {sessions.map((session: any) => (
          <div
            key={session.id}
            onClick={() => onLoadSession(session)}
            className={`session-item group flex items-center gap-2 px-3 py-3 rounded-xl cursor-pointer transition-colors duration-150 ease-[var(--ease-out)] mb-1 ${
              activeSessionId === session.id
                ? 'bg-white/20 text-white'
                : 'hover:bg-white/10 text-white/80 hover:text-white'
            }`}
          >
            <MessageSquare className="w-4 h-4 shrink-0 opacity-50" />
            <div className="flex-1 min-w-0">
              <div className="text-sm truncate">{session.title}</div>
              <div className="text-[11px] opacity-60 mt-0.5">{session.date}</div>
            </div>
            <button
              onClick={(e) => onDeleteSession(e, session.id)}
              className="opacity-0 group-hover:opacity-100 p-1.5 rounded-lg hover:bg-red-500/20 text-white/50 hover:text-red-400 transition-[opacity,color,background-color] duration-150 ease-[var(--ease-out)] press-scale"
            >
              <Trash2 className="w-3.5 h-3.5" />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};
