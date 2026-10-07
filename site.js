// Shared behaviour: the phone menu. Pages work without it; the menu just stays open.
(function () {
  var head = document.querySelector('.site-head');
  var btn = head && head.querySelector('.nav-toggle');
  if (!btn) return;
  btn.addEventListener('click', function () {
    var open = head.classList.toggle('open');
    btn.setAttribute('aria-expanded', String(open));
    btn.textContent = open ? 'Close' : 'Menu';
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && head.classList.contains('open')) { head.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); btn.textContent = 'Menu'; btn.focus(); }
  });
})();

// Analytics events (GoatCounter, cookie-free). Counts resume and report downloads,
// email clicks and LinkedIn clicks. Does nothing when the analytics script is absent.
document.addEventListener('click', function (e) {
  var a = e.target.closest && e.target.closest('a[href]');
  if (!a || !window.goatcounter || !window.goatcounter.count) return;
  var h = a.getAttribute('href'), name = null;
  if (/\.pdf$/i.test(h)) name = 'download-' + h.split('/').pop();
  else if (h.indexOf('mailto:') === 0) name = 'click-email';
  else if (/linkedin\.com/i.test(h)) name = 'click-linkedin';
  if (name) window.goatcounter.count({ path: name, title: a.textContent.trim(), event: true });
});
