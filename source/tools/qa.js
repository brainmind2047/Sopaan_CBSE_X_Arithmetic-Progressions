// usage: node qa.js page.html  -> checks every blank answer is accepted by the engine and every slide renders
const {chromium}=require('playwright');
(async()=>{ const b=await chromium.launch(); const p=await b.newPage(); const errs=[];
 await p.route('**/fonts.googleapis.com/**',r=>r.abort()); p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file://'+require('path').resolve(process.argv[2])); await p.waitForTimeout(500);
 const r=await p.evaluate(()=>{ const Q=window.__sopaanQA, bad=[]; let n=0, blanks=0;
   Object.keys(Q.SLIDES).forEach(id=>Q.SLIDES[id].forEach((sl,i)=>{ n++;
     if(sl.kind==='mcq'||sl.kind==='ar'){ if(sl.correct==null) bad.push(id+'#'+(i+1)+' no correct'); return; }
     (sl.flat||[]).forEach((st,si)=>{ const keys=(st.t.match(/__B\d+__/g)||[]).map(x=>x.slice(2,-2));
       Object.keys(st.a).forEach(k=>{ blanks++; if(!keys.includes(k)) bad.push(id+'#'+(i+1)+' step'+(si+1)+' '+k+' not in text');
         let ok=false; try{ ok=Q.answerMatches(st.a[k],st.a[k],st.accept,st.expr); }catch(e){}
         if(!ok) bad.push(id+'#'+(i+1)+' step'+(si+1)+' '+k+'="'+st.a[k]+'" expr='+st.expr+' not accepted'); });
       keys.forEach(k=>{ if(!(k in st.a)) bad.push(id+'#'+(i+1)+' step'+(si+1)+' blank '+k+' has no answer'); }); }); }));
   return {n,blanks,bad}; });
 console.log('slides',r.n,'blanks',r.blanks,'problems',r.bad.length); r.bad.slice(0,60).forEach(x=>console.log('  ',x));
 console.log(errs.length?'PAGE ERRORS '+errs.join(' | '):'no page errors'); await b.close(); })();
