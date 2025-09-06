// Reveal animations via IntersectionObserver
(function(){
  const single = document.querySelectorAll('.reveal-up');
  const groups = document.querySelectorAll('.reveal-group');

  const io = new IntersectionObserver((entries)=>{
    entries.forEach(e=>{
      if(e.isIntersecting){
        e.target.classList.add('in');
        if(e.target.classList.contains('reveal-group')){
          // mark inner inputs in sequence
          const inputs = e.target.querySelectorAll('.form-control');
          inputs.forEach((el,i)=> setTimeout(()=>el.classList.add('in'), 90*i));
        }
        io.unobserve(e.target);
      }
    });
  }, {threshold:.2});

  [...single, ...groups].forEach(el=>io.observe(el));
})();

// Strict client validations
(function(){
  const reg = document.getElementById('registerForm');
  if(reg){
    const name   = reg.querySelector('input[name="name"]');
    const mobile = reg.querySelector('input[name="mobile"]');

    // block numbers in name
    name.addEventListener('keypress', e=>{
      if(!/[a-zA-Z\s]/.test(e.key)) e.preventDefault();
    });
    name.addEventListener('input', e=>{
      e.target.value = e.target.value.replace(/[^a-zA-Z\s]/g,'');
    });

    // block letters in mobile
    mobile.addEventListener('keypress', e=>{
      if(!/[0-9]/.test(e.key)) e.preventDefault();
    });
    mobile.addEventListener('input', e=>{
      e.target.value = e.target.value.replace(/[^0-9]/g,'');
    });
  }

  // simple client-side required check for both forms
  const forms = [document.getElementById('registerForm'), document.getElementById('loginForm')].filter(Boolean);
  forms.forEach(f=>{
    f.addEventListener('submit', (e)=>{
      const invalid = [...f.querySelectorAll('input')].some(inp=>{
        if(inp.type === 'email'){
          const ok = /\S+@\S+\.\S+/.test(inp.value);
          inp.classList.toggle('is-invalid', !ok);
          return !ok;
        }
        const empty = !inp.value.trim();
        inp.classList.toggle('is-invalid', empty);
        return empty;
      });
      if(invalid) e.preventDefault();
    });
  });
})();


// Floating label controller (no placeholders needed)
(function(){
  const wrapSel = '.float-group';
  const groups = document.querySelectorAll(wrapSel);
  if(!groups.length) return;

  const setState = (input) => {
    const g = input.closest(wrapSel);
    if(!g) return;
    g.classList.toggle('is-filled', !!input.value.trim());
  };

  groups.forEach(g=>{
    const input = g.querySelector('input');
    if(!input) return;

    // initial state
    setState(input);

    input.addEventListener('focus', ()=> g.classList.add('is-focused'));
    input.addEventListener('blur',  ()=> g.classList.remove('is-focused'));
    input.addEventListener('input', ()=> setState(input));
  });
})();
