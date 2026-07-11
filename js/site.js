// Shared site behaviour
(function(){
  // Mobile menu
  var mb=document.getElementById('mb'),nav=document.getElementById('nav');
  if(mb&&nav){mb.addEventListener('click',function(){nav.classList.toggle('show');});
    nav.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){nav.classList.remove('show');});});}
  // Reveal on scroll
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
    if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.14});
  document.querySelectorAll('.reveal').forEach(function(el){io.observe(el);});
  // Counters
  var cio=new IntersectionObserver(function(es){es.forEach(function(e){
    if(!e.isIntersecting)return;var el=e.target,to=+el.dataset.to,n=0,
    step=Math.max(1,Math.round(to/60));
    var t=setInterval(function(){n+=step;if(n>=to){n=to;clearInterval(t);}
      el.textContent=n.toLocaleString('en-US');},22);cio.unobserve(el);});},{threshold:.6});
  document.querySelectorAll('.num[data-to]').forEach(function(el){cio.observe(el);});
})();
