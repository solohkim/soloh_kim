async function loadCerts(){
 const r=await fetch('certs.json?t='+Date.now());
 if(!r.ok) return;
 const certs=await r.json();
 document.getElementById('certsCount').textContent=certs.length+' certs';
 const grid=document.getElementById('certsGrid');
 grid.innerHTML=certs.map((c,i)=>{
  const pdf=c.file.toLowerCase().endsWith('.pdf');
  const p=c.private;
  const expandUrl = p ? `viewer.html?file=${encodeURIComponent(c.file)}` : c.file;
  let pre=pdf
   ?`<div id="pre-${i}" style="background:#0a0a0a;border:1px solid #222;height:380px;border-radius:8px;overflow:auto;display:flex;justify-content:center;align-items:start"><canvas id="canvas-${i}" style="width:100%"></canvas></div>`
   :`<div style="background:#000;border:1px solid #222;height:380px;border-radius:8px;display:flex;align-items:center;justify-content:center;overflow:auto"><img src="${c.file}" style="max-width:100%"></div>`;
  return `<div class="col-md-4"><div class="card-m"><small class="badge-h" style="color:var(--gold)">${c.cat}</small><h6 class="mt-2" style="font-size:.85rem">${c.name}</h6>${pre}<div class="mt-2 d-flex gap-2"><button onclick="window.open('${expandUrl}','_blank')" class="btn btn-sm w-100" style="background:#111;border:1px solid #222;color:#00FF41">Expand ↕</button></div>${p?`<small class="text-muted" style="font-size:.6rem">View-only • Ctrl+K admin</small>`:``}</div></div>`;
 }).join('');

 // Render PDFs as canvas (works on phone, no download)
 if(window.pdfjsLib){
   pdfjsLib.GlobalWorkerOptions.workerSrc='https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
   certs.forEach(async (c,i)=>{
     if(!c.file.toLowerCase().endsWith('.pdf')) return;
     try{
       const pdf = await pdfjsLib.getDocument(c.file).promise;
       const page = await pdf.getPage(1);
       const canvas = document.getElementById(`canvas-${i}`);
       if(!canvas) return;
       const vp = page.getViewport({scale:1.2});
       canvas.width=vp.width; canvas.height=vp.height;
       await page.render({canvasContext:canvas.getContext('2d'),viewport:vp}).promise;
     }catch(e){ document.getElementById(`pre-${i}`).innerHTML=`<small style="color:#666;padding:20px">${c.name}</small>` }
   });
 }
 window._certsData=certs;
}
document.addEventListener('keydown',e=>{
 if(e.ctrlKey&&e.key.toLowerCase()==='k'){
  e.preventDefault();
  const k=prompt('Admin key:');
  if(k==='kimsec254'&&window._certsData){
   window._certsData.forEach(c=>{let a=document.createElement('a');a.href=c.file;a.download=c.file.split('/').pop();a.click();})
  }
 }
});
loadCerts();