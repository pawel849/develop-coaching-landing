(() => {
  const booking = document.querySelector('#booking');
  const mobileButton = document.querySelector('.mobile-book');
  if (!booking || !mobileButton || !('IntersectionObserver' in window)) return;

  const observer = new IntersectionObserver(([entry]) => {
    mobileButton.classList.toggle('is-hidden', entry.isIntersecting);
    mobileButton.setAttribute('aria-hidden', String(entry.isIntersecting));
  }, { threshold: 0.08 });

  observer.observe(booking);
})();
