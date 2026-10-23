async function loadCerts(){
 const r=await fetch('certs.json?t='+Date.now());
 if(!r.ok) return;
 const certs=await r.json();
 document.getElementById('certsCount').textContent=certs.length+' certs';
 document.getElementById('certsGrid').innerHTML=certs.map(c=>{
  const pdf=c.file.toLowerCase().endsWith('.pdf');
  const p=c.private;
  let pre=pdf
   ?`<div style="background:#0a0a0a;border:1px solid #222;height:380px;border-radius:8px;overflow:hidden"><iframe src="${c.file}#toolbar=0&navpanes=0" style="width:100%;height:100%;border:none"></iframe></div>`
   :`<div style="background:#000;border:1px solid #222;height:380px;border-radius:8px;display:flex;align-items:center;justify-content:center;overflow:auto"><img src="${c.file}" style="max-width:100%"></div>`;
  // If private, Expand goes to protected viewer, not raw pdf
  const expandUrl = p ? `viewer.html?file=${encodeURIComponent(c.file)}` : c.file;
  return `<div class="col-md-4"><div class="card-m"><small class="badge-h" style="color:var(--gold)">${c.cat}</small><h6 class="mt-2" style="font-size:.85rem">${c.name}</h6>${pre}<div class="mt-2 d-flex gap-2"><button onclick="window.open('${expandUrl}','_blank')" class="btn btn-sm w-100" style="background:#111;border:1px solid #222;color:#00FF41">Expand ↕</button></div>${p?`<small class="text-muted" style="font-size:.6rem">View-only • Ctrl+K admin download</small>`:``}</div></div>`;
 }).join('');
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