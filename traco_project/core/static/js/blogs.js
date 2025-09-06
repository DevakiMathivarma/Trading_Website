// Reveal on scroll (no AOS)
(function(){
  const els = document.querySelectorAll('.reveal-left, .reveal-up, .blog-card');
  const obs = new IntersectionObserver(entries=>{
    entries.forEach(e=>{
      if(e.isIntersecting){
        e.target.classList.add('reveal','in');
        obs.unobserve(e.target);
      }
    })
  },{ threshold:.15 });
  els.forEach(el=>obs.observe(el));
})();

// Category switching + More
(function(){
  const tabWrap = document.getElementById('categoryTabs');
  if(!tabWrap) return;

  const sections = [...document.querySelectorAll('.posts-section')];

  // show only first 3 posts initially for each section
  const clampView = (section, showCount=3)=>{
    const cols = section.querySelectorAll('.post-col');
    cols.forEach((c,i)=> c.style.display = (i<showCount ? '' : 'none'));
    const btn = section.querySelector('.btn-more');
    if(btn){
      const total = cols.length;
      btn.dataset.shown = Math.min(showCount, total);
      btn.style.display = total > showCount ? '' : 'none';
    }
  };

  sections.forEach(sec => clampView(sec, 3));

  // tab click
  tabWrap.addEventListener('click', (e)=>{
    const btn = e.target.closest('.btn-tab');
    if(!btn) return;
    // active styles
    tabWrap.querySelectorAll('.btn-tab').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');

    // switch sections
    const slug = btn.dataset.slug;
    sections.forEach(s => s.classList.toggle('d-none', s.id !== `posts-${slug}`));

    // ensure clamped state for that section
    const activeSec = document.getElementById(`posts-${slug}`);
    clampView(activeSec, 3);

    // smooth scroll to tabs on mobile
    tabWrap.scrollIntoView({behavior:'smooth', block:'start'});
  });

  // delegate "More" click for each section
  document.addEventListener('click', (e)=>{
    const more = e.target.closest('.btn-more');
    if(!more) return;
    const slug = more.dataset.target;
    const sec  = document.getElementById(`posts-${slug}`);
    const cols = [...sec.querySelectorAll('.post-col')];

    let shown = parseInt(more.dataset.shown || '3', 10);
    const add = 6; // show 6 more
    const nextShow = Math.min(shown + add, cols.length);
    cols.slice(0, nextShow).forEach(el=>{
      el.style.display = '';
      // small appear animation
      el.querySelector('.blog-card')?.classList.add('reveal','in');
    });
    shown = nextShow;
    more.dataset.shown = shown;

    if(shown >= cols.length){
      more.style.display = 'none';
    }
  });
})();
