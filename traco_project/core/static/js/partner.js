// IntersectionObserver animations
(function(){
  const els = document.querySelectorAll('.reveal-in, .slide-in');
  const io = new IntersectionObserver((entries)=>{
    entries.forEach(e=>{
      if(e.isIntersecting){
        e.target.classList.add('show');
        io.unobserve(e.target);
      }
    });
  }, {threshold:.15});
  els.forEach(el=>io.observe(el));
})();

// Client-side strict typing
(function(){
  const form = document.querySelector('.partner-form');
  if(!form) return;

  const name = form.querySelector('input[name="name"]');
  const phone = form.querySelector('input[name="phone"]');
  const pin = form.querySelector('input[name="pincode"]');

  // letters only for name
  name?.addEventListener('input', e => e.target.value = e.target.value.replace(/[^a-zA-Z\s]/g,''));
  // digits only for phone/pin
  [phone, pin].forEach(inp => inp?.addEventListener('input', e => e.target.value = e.target.value.replace(/\D/g,'')));
})();
