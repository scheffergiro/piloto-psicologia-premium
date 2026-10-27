(() => {
 const toggle = document.querySelector('.menu-toggle');
 const nav = document.querySelector('#navigation');
 const mobile = window.matchMedia('(max-width: 1080px)');
 const close = () => { toggle.setAttribute('aria-expanded', 'false'); nav.hidden = mobile.matches; };
 const sync = () => { toggle.hidden = !mobile.matches; close(); };
 toggle.addEventListener('click', () => { const open = toggle.getAttribute('aria-expanded') === 'true'; toggle.setAttribute('aria-expanded', String(!open)); nav.hidden = open; });
 nav.addEventListener('click', event => { if (event.target.closest('a')) close(); });
 document.addEventListener('keydown', event => { if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') { close(); toggle.focus(); } });
 mobile.addEventListener('change', sync); sync();
 // Avoid covering or duplicating a visible contact action on narrow screens.
 // Without IntersectionObserver, the original floating link remains available.
 const floating = document.querySelector('#whatsapp');
 if (floating && 'IntersectionObserver' in window) {
   const visible = new Set();
   const observer = new IntersectionObserver(entries => {
     entries.forEach(entry => {
       if (entry.isIntersecting) visible.add(entry.target);
       else visible.delete(entry.target);
     });
     floating.classList.toggle('contact-in-view', visible.size > 0);
   }, { threshold: 0.1 });
   document.querySelectorAll('main .button').forEach(link => observer.observe(link));
 }
})();
