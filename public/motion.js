/* Progressive enhancement: content is visible even when JS/APIs fail. */
(() => {
  const media = window.matchMedia('(prefers-reduced-motion: reduce)');
  const reduceAtStart = media.matches;
  const navigationType = performance.getEntriesByType('navigation')[0]?.type || 'navigate';
  const initialHash = location.hash;
  const homeAddress = initialHash === '' || initialHash === '#inicio';
  // #inicio is a top alias, not a persistent section destination. Keeping it on
  // the history entry makes Chromium reapply the fragment on a later reload.
  // replaceState preserves the entry/state; other anchors remain entirely native.
  const canonicalizeHome = () => {
    if (location.hash !== '#inicio') return;
    const url = new URL(location.href);
    url.hash = '';
    try { history.replaceState(history.state, '', url.href); } catch (_) { /* Native fallback. */ }
  };
  canonicalizeHome();
  window.addEventListener('hashchange', canonicalizeHome);
  if (!Element.prototype.animate) return;
  const targets = document.querySelectorAll('.section-grid > header, .section-grid > .section-copy, .topic-grid article, .highlights-grid, .conversion-bridge .wrap, .questions');
  const seen = new WeakSet();
  const active = new Map();
  let observer;
  const cancel = () => { active.forEach(animation => animation.cancel()); active.clear(); };
  const start = () => {
    if (media.matches || !('IntersectionObserver' in window)) return;
    observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (media.matches || !entry.isIntersecting || seen.has(entry.target)) return;
        const element = entry.target;
        seen.add(element);
        observer.unobserve(element);
        if (element.contains(document.activeElement)) return;
        const animation = element.animate([
          { opacity: 0, transform: 'translateY(8px)' },
          { opacity: 1, transform: 'translateY(0)' }
        ], { duration: 380, easing: 'cubic-bezier(.2,.65,.3,1)', iterations: 1 });
        active.set(element, animation);
        animation.finished.then(() => active.delete(element), () => active.delete(element));
      });
    }, { threshold: 0, rootMargin: '0px 0px -24px 0px' });
    targets.forEach(element => { if (!seen.has(element)) observer.observe(element); });
  };
  document.addEventListener('focusin', event => {
    active.forEach((animation, element) => {
      if (element.contains(event.target)) { animation.cancel(); active.delete(element); }
    });
  });
  media.addEventListener('change', () => {
    if (observer) observer.disconnect();
    cancel();
    start();
  });
  // Never replay on preference changes, hash changes, or history restoration.
  let entranceDecided = false;
  let interacted = false;
  const cancelHero = () => {
    active.forEach((animation, element) => {
      if (animation.id === 'hero-entrance') { animation.cancel(); active.delete(element); }
    });
  };
  const interaction = () => { interacted = true; cancelHero(); };
  ['pointerdown', 'keydown', 'wheel', 'touchstart'].forEach(type =>
    window.addEventListener(type, interaction, { passive: true }));
  window.addEventListener('pagehide', () => { entranceDecided = true; cancel(); });
  const decideEntrance = persisted => {
    if (entranceDecided) return;
    entranceDecided = true;
    if (persisted || navigationType === 'back_forward' || reduceAtStart || media.matches || interacted ||
        !homeAddress || (location.hash && location.hash !== '#inicio') || window.scrollY >= 40) return;
    const steps = [
      ['.hero-identity > .eyebrow, .hero h1', 0, 560],
      ['.hero-media, .hero-profession, .credential', 130, 560],
      ['.hero-statement', 260, 560],
      ['.hero-contact, .hero-microcopy', 390, 560]
    ];
    steps.forEach(([selector, delay, duration]) => {
      document.querySelectorAll(selector).forEach(element => {
        if (element.contains(document.activeElement)) return;
        const animation = element.animate([
          { opacity: 0, transform: 'translateY(20px)' },
          { opacity: 1, transform: 'translateY(0)' }
        ], { duration, delay, easing: 'cubic-bezier(.2,.65,.3,1)', fill: 'backwards', iterations: 1 });
        animation.id = 'hero-entrance';
        active.set(element, animation);
        animation.finished.then(() => active.delete(element), () => active.delete(element));
      });
    });
  };
  // Native restoration can complete around pageshow. Read the viewport two
  // frames after activation, without scrollTo or global manual restoration.
  const afterRestoration = persisted => requestAnimationFrame(() =>
    requestAnimationFrame(() => decideEntrance(persisted)));
  window.addEventListener('pageshow', event => {
    if (event.persisted) { cancel(); return; }
    afterRestoration(false);
  });
  if (document.readyState === 'complete') afterRestoration(false);
  start();
})();
