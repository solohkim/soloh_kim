async function loadCerts(){
 const r=await fetch('certs.json?t='+Date.now());
 if(!r.ok) return;
 const certs=await r.json();
 document.getElementById('certsCount').textContent=certs.length+' certs';
 document.getElementById('certsGrid').innerHTML=certs.map(c=>{
  const pdf=c.file.toLowerCase().endsWith('.pdf');
  const p=c.private;
  let pre=pdf?`<div style="background:#0a0a0a;border:1px solid #222;height:220px;border-radius:8px;overflow:hidden;position:relative"><iframe src="${c.file}#toolbar=0" style="width:100%;height:100%;border:none;pointer-events:none"></iframe><div style="position:absolute;inset:0"></div></div>`:`<div style="background:#000;border:1px solid #222;height:220px;border-radius:8px;display:flex;align-items:center;justify-content:center"><img src="${c.file}" style="max-width:100%;max-height:100%"></div>`;
  return `<div class="col-md-4"><div class="card-m"><small class="badge-h" style="color:var(--gold)">${c.cat}</small><h6 class="mt-2" style="font-size:.85rem">${c.name}</h6>${pre}<div class="mt-2">${!p?`<a href="${c.file}" target="_blank" class="btn btn-sm w-100" style="background:#111;color:#00FF41">Open</a>`:`<button disabled class="btn btn-sm w-100" style="background:#111;color:#666">View-only</button>`}</div></div></div>`;
 }).join('');
 window._certsData=certs;
}
document.addEventListener('keydown',e=>{if(e.ctrlKey&&e.key.toLowerCase()==='k'){e.preventDefault();const k=prompt('Admin key:');if(k==='kimsec254'&&window._certsData){window._certsData.forEach(c=>{let a=document.createElement('a');a.href=c.file;a.download=c.file.split('/').pop();a.click();})}}});
loadCerts();