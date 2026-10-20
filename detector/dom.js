() => {
 const selector = el => {
   let parts=[];
   for(let n=el;n&&n.nodeType===1;n=n.parentElement){
     let p=n.localName;
     if(n.id){p+='#'+CSS.escape(n.id); if(document.querySelectorAll(p).length===1){parts.unshift(p);break;}}
     else {p += [...n.classList].slice(0,2).map(c=>'.'+CSS.escape(c)).join('');}
     if(n.parentElement){const peers=[...n.parentElement.children].filter(x=>x.localName===n.localName);if(peers.length>1)p+=':nth-of-type('+(peers.indexOf(n)+1)+')';}
     parts.unshift(p);
   }
   const s=parts.join(' > ');return document.querySelectorAll(s).length===1&&document.querySelector(s)===el?s:null;
 };
 const style = el => {
   const s=getComputedStyle(el),r=el.getBoundingClientRect();
   let opacity=1,displayNone=false,invisible=false,clipped=false,bg=null;
   const rgba=c=>(c.match(/[\d.]+/g)||[]).map(Number);
   for(let n=el;n;n=n.parentElement){const t=getComputedStyle(n), box=n.getBoundingClientRect();opacity*=Number(t.opacity);displayNone ||= t.display==='none';invisible ||= ['hidden','collapse'].includes(t.visibility);clipped ||= t.clipPath==='inset(50%)'||t.clip==='rect(0px, 0px, 0px, 0px)'||(['hidden','clip'].includes(t.overflow)&&(box.width<=1||box.height<=1));if(!bg){let b=rgba(t.backgroundColor);if(b.length===3||b[3]>.98)bg=b;}}
   let fg=rgba(s.color);bg ||= [255,255,255];
   return {opacity,alpha:fg.length>3?fg[3]:1,sameColor:fg.length>=3&&Math.max(...fg.slice(0,3).map((v,i)=>Math.abs(v-bg[i])))<5,displayNone,invisible,tiny:parseFloat(s.fontSize)<=1,clipped,outside:r.right<0||r.bottom<0||(['absolute','fixed'].includes(s.position)&&(r.left>innerWidth*3||(s.position==='fixed'&&r.top>innerHeight*3))),fontSize:s.fontSize,color:s.color,background:s.backgroundColor,rect:{x:r.x,y:r.y,width:r.width,height:r.height}};
 };
 const elements=[];
 for(const el of document.querySelectorAll('body *')){
   if(['SCRIPT','STYLE','NOSCRIPT','TEMPLATE','IFRAME'].includes(el.tagName))continue;
   const own=[...el.childNodes].some(n=>n.nodeType===3&&n.textContent.trim());
   if(!own)continue;
   const text=el.textContent.trim();if(!text)continue;
   const location=selector(el);if(!location)continue;
   const a=el.closest('a[href]')||el.querySelector('a[href]');
   elements.push({text,location,style:style(el),context:(el.parentElement?.textContent||'').slice(0,2000),href:a?.href||'',external:a?new URL(a.href,window.location.href).origin!==window.location.origin:false});
 }
 return {elements,links:[...document.querySelectorAll('a[href]')].map(a=>a.href)};
}
