/* Editable desktop design importer, running in the ordinary Figma Plugin API.
 * DESIGN is generated from build_design.py. It never overwrites the web design.
 * Foundation/variant helpers are the bundled Figma skill helpers (see helpers/).
 */
const ledger = {version: DESIGN.version, status: 'not-started', createdNodeIds: [], variables: {}, styles: {}, screens: {}, components: {}, errors: []};
const refs = [], styleBindings = [], screenNodes = new Map(), vars = new Map(), styles = new Map(), masters = new Map();
let fontFamily, page, componentsArea, buttonLabelProp, buttonIconProp;
const FONT_SIZES = [14, 16, 18, 20, 22, 28];
const rgb = hex => ({r: parseInt(hex.slice(1,3),16)/255, g: parseInt(hex.slice(3,5),16)/255, b: parseInt(hex.slice(5,7),16)/255});
function track(n) { ledger.createdNodeIds.push(n.id); return n; }
function paint(name) {
  const p = {type:'SOLID', color:rgb(DESIGN.tokens[name] || '#FFFFFF')};
  return vars.has(name) ? [figma.variables.setBoundVariableForPaint(p, 'color', vars.get(name))] : [p];
}
function pad(n, amount) {
  const a = Array.isArray(amount) ? amount : [amount,amount];
  n.paddingTop = n.paddingBottom = a[0] || 0;
  n.paddingLeft = n.paddingRight = a[1] || 0;
  for (const k of ['paddingTop','paddingBottom','paddingLeft','paddingRight']) {
    const v = vars.get('space/' + n[k]); if (v) n.setBoundVariable(k,v);
  }
}
function frame(name, axis='V') {
  const n=track(figma.createFrame()); n.name=name; n.fills=[];
  n.layoutMode=axis==='H'?'HORIZONTAL':'VERTICAL';
  n.primaryAxisSizingMode='AUTO'; n.counterAxisSizingMode='AUTO';
  n.counterAxisAlignItems=axis==='H'?'CENTER':'MIN';
  n.itemSpacing=0; n.clipsContent=false; return n;
}
function txt(value,size=16,color='ink',bold=false,width) {
  const n=track(figma.createText()); n.name=value.slice(0,36); n.fontName={family:fontFamily,style:bold?'Bold':'Regular'};
  n.fontSize=size; n.lineHeight={unit:'PIXELS',value:Math.round(size*1.5)}; n.characters=value;
  n.fills=paint(color); n.textAutoResize='WIDTH_AND_HEIGHT';
  const style=styles.get(size+'/'+bold); if(style)styleBindings.push({node:n,styleId:style.id});
  if(width){ n.textAutoResize='HEIGHT'; n.resize(Math.max(1,width),n.height); }
  return n;
}
function attach(n,s,p) {
  p.appendChild(n);
  if(s.w) n.resize(s.w,n.height);
  if(s.h) n.resize(n.width,s.h);
  const horizontal=p.layoutMode==='HORIZONTAL';
  if(s.fill || s.fillY) {
    if (s.kind==='text') {
      n.textAutoResize='HEIGHT'; n.resize(Math.max(1,n.width),n.height); n.layoutSizingHorizontal='FILL';
    } else if (s.fillY || !horizontal) { n.layoutSizingVertical='FILL'; n.layoutSizingHorizontal=s.w?'FIXED':'FILL'; }
    else n.layoutSizingHorizontal='FILL';
  } else if(s.kind==='box' && !s.w && !horizontal) n.layoutSizingHorizontal='FILL';
  if(s.kind==='box' && s.axis==='H' && !s.w && !horizontal) n.layoutSizingHorizontal='FILL';
  if(s.kind==='box' && s.axis!=='H' && horizontal && s.h===undefined && p.name.includes('与')) n.layoutSizingVertical='FILL';
  if(s.action) refs.push({node:n, action:s.action});
  return n;
}
function decorate(n,s) {
  if(s.bg)n.fills=paint(s.bg);
  if(s.border){n.strokes=paint(s.border);n.strokeWeight=1;}
  n.cornerRadius=s.radius||0;
  const r=vars.get('radius/'+(s.radius||0)); if(r)n.setBoundVariable('cornerRadius',r);
  pad(n,s.pad||0); n.itemSpacing=s.gap||0;
  const v=vars.get('space/'+(s.gap||0)); if(v)n.setBoundVariable('itemSpacing',v);
  if(s.w){n.resize(s.w,n.height);n.counterAxisSizingMode='FIXED';}
  if(s.h){n.resize(n.width,s.h); if(s.axis==='H')n.counterAxisSizingMode='FIXED';else n.primaryAxisSizingMode='FIXED';}
  if(s.scroll){n.clipsContent=true;n.overflowDirection='VERTICAL';}
}
function makeButton(s,p) {
  const variant=s.disabled?'disabled':s.variant||'secondary';
  const master=masters.get('button/'+variant)||masters.get('button/secondary');
  const n=track(master.createInstance());
  if(buttonLabelProp)n.setProperties({[buttonLabelProp]:s.text});
  const iconKey={'图文生成':'image_text','AI 热度图文生成':'ai_hot_article','头条发布':'toutiao_publish','系统设置':'system_settings','API 连接设置':'api_settings'}[s.text];
  if(buttonIconProp&&iconKey&&masters.has('icon/'+iconKey))n.setProperties({[buttonIconProp]:masters.get('icon/'+iconKey).id});
  n.name=s.text;
  n.resize(s.w||Math.max(80,s.text.length*16+32),variant==='rail'||variant==='railActive'?48:40);
  if(!s.disabled && s.action) refs.push({node:n,action:s.action});
  p.appendChild(n); return n;
}
function choice(s,p) {
  const n=frame(s.text||'选择控件','H'); n.itemSpacing=12; n.counterAxisAlignItems='CENTER';
  n.resize(n.width,40);n.counterAxisSizingMode='FIXED';
  const master=masters.get((s.radio?'radio':'check')+'/'+!!s.selected);
  n.appendChild(track(master.createInstance()));
  if(s.text){const t=txt(s.text,16,'ink',false);n.appendChild(t);if(s.fill){t.textAutoResize='HEIGHT';t.resize(100,t.height);t.layoutSizingHorizontal='FILL';}}
  attach(n,s,p); return n;
}
function render(s,p) {
  if(s.kind==='button')return makeButton(s,p);
  if(s.kind==='choice')return choice(s,p);
  if(s.kind==='text')return attach(txt(s.text,s.size,s.color,s.bold,s.w),s,p);
  if(s.kind==='badge') {
    const n=frame(s.text,'H'),tone=s.tone||'accent'; pad(n,[4,10]); n.cornerRadius=4;
    n.fills=paint(tone==='neutral'?'subtle':tone==='warning'?'warningSoft':tone==='error'?'errorSoft':tone==='success'?'successSoft':'accentSoft');
    n.appendChild(txt(s.text,14,tone==='neutral'?'secondary':tone==='success'?'success':tone==='error'?'error':tone==='warning'?'warning':'accent',true));
    p.appendChild(n);return n;
  }
  if(s.kind==='input') {
    const n=frame(s.placeholder||'输入框','H');n.resize(s.w,40); n.primaryAxisSizingMode='FIXED';n.counterAxisSizingMode='FIXED';
    n.counterAxisAlignItems='CENTER';pad(n,[0,12]);n.cornerRadius=4;n.fills=paint('surface');n.strokes=paint(s.focus?'focus':'border');n.strokeWeight=s.focus?2:1;
    n.appendChild(txt(s.text,16));p.appendChild(n);return n;
  }
  const n=frame(s.name,s.axis);decorate(n,s);attach(n,s,p);
  for(const ch of s.children||[])render(ch,n);
  return n;
}
async function foundations() {
  const collections=await figma.variables.getLocalVariableCollectionsAsync();
  const oldVars=await figma.variables.getLocalVariablesAsync();
  let primitive=collections.find(c=>c.name==='AIDocStudio / Windows primitives');
  let semantic=collections.find(c=>c.name==='AIDocStudio / Windows');
  if(!primitive)primitive=(await createVariableCollection('AIDocStudio / Windows primitives',['Light'])).collection;
  if(!semantic)semantic=(await createVariableCollection('AIDocStudio / Windows',['Light'])).collection;
  ledger.collections={primitives:primitive.id,semantic:semantic.id};
  for(const [name,value] of Object.entries(DESIGN.tokens)) {
    let raw=oldVars.find(v=>v.variableCollectionId===primitive.id&&v.name==='Color/'+name);
    if(!raw)raw=(await createSemanticTokens(primitive,{Light:primitive.defaultModeId},[{name:'Color/'+name,type:'COLOR',values:{Light:value},scopes:[],codeSyntax:{WEB:'var(--win-raw-'+name+')'}}])).variables['Color/'+name];
    let sem=oldVars.find(v=>v.variableCollectionId===semantic.id&&v.name==='Color/'+name);
    if(!sem)sem=(await createSemanticTokens(semantic,{Light:semantic.defaultModeId},[{name:'Color/'+name,type:'COLOR',values:{Light:{type:'VARIABLE_ALIAS',id:raw.id}},scopes:['FRAME_FILL','SHAPE_FILL','TEXT_FILL','STROKE_COLOR'],codeSyntax:{WEB:'var(--win-'+name+')'}}])).variables['Color/'+name];
    vars.set(name,sem); ledger.variables[name]=sem.id;
  }
  for(const [prefix,values,scopes] of [['space',[0,4,6,8,10,12,16,20,24,32,40],['GAP']],['radius',[0,4,6,8],['CORNER_RADIUS']]]) {
    for(const val of values){const key=prefix+'/'+val;let v=oldVars.find(v=>v.variableCollectionId===semantic.id&&v.name===key);
      if(!v)v=(await createSemanticTokens(semantic,{Light:semantic.defaultModeId},[{name:key,type:'FLOAT',values:{Light:val},scopes,codeSyntax:{WEB:'var(--win-'+prefix+'-'+val+')'}}])).variables[key];
      vars.set(key,v);ledger.variables[key]=v.id;}
  }
  const available=await figma.listAvailableFontsAsync();
  fontFamily=['Microsoft YaHei UI','Noto Sans SC'].find(f=>['Regular','Bold'].every(style=>available.some(a=>a.fontName.family===f&&a.fontName.style===style)));
  if(!fontFamily)throw new Error('需要 Microsoft YaHei UI 或 Noto Sans SC 的 Regular / Bold 字体。');
  await Promise.all(['Regular','Bold'].map(style=>figma.loadFontAsync({family:fontFamily,style})));
  ledger.fontFamily=fontFamily;
  const existing=await figma.getLocalTextStylesAsync();
  for(const size of FONT_SIZES)for(const bold of [false,true]) {
    const key=size+'/'+bold,name='AIDocStudio/Windows/'+size+'/'+(bold?'Bold':'Regular');
    let style=existing.find(s=>s.name===name);
    if(!style){style=figma.createTextStyle();style.name=name;style.fontName={family:fontFamily,style:bold?'Bold':'Regular'};style.fontSize=size;style.lineHeight={unit:'PIXELS',value:Math.round(size*1.5)};}
    styles.set(key,style);ledger.styles[key]=style.id;
  }
}
async function controls() {
  for(const [name,svg] of Object.entries(DESIGN.assets)) {
    const c=track(figma.createComponent());c.name='Windows/Source icon/'+name;c.resize(24,24);c.fills=[];
    const icon=track(figma.createNodeFromSvg(svg));const scale=20/Math.max(icon.width,icon.height);icon.rescale(scale);c.appendChild(icon);icon.x=(24-icon.width)/2;icon.y=(24-icon.height)/2;
    componentsArea.appendChild(c);c.x=800+Object.keys(ledger.components).length*32;c.y=180;c.description='复用项目已有矢量资源 '+DESIGN.assetSources[name];
    masters.set('icon/'+name,c);ledger.components['icon/'+name]=c.id;
  }
  // Use the scoped variant helper; no unrelated component library is created.
  const tones=['primary','secondary','quiet','disabled','focus','rail','railActive','tab','tabActive'];
  const family=await createComponentWithVariants({name:'Windows/Button',description:'40px 桌面按钮；Label 为可编辑文本属性；焦点状态保留 2px 蓝色描边。',variantAxes:{Style:tones},baseProps:{width:184,height:40,layoutMode:'HORIZONTAL',padding:{left:16,right:16},radius:4},page});
  componentsArea.appendChild(family.componentSet); family.componentSet.x=0;family.componentSet.y=0;
  buttonLabelProp=family.componentSet.addComponentProperty('Label','TEXT','按钮');
  buttonIconProp=family.componentSet.addComponentProperty('Icon','INSTANCE_SWAP',masters.get('icon/image_text').id);
  for(let i=0;i<tones.length;i++) {
    const variant=tones[i],n=family.variants[i];track(n);n.fills=paint(['primary','railActive'].includes(variant)?variant==='primary'?'accent':'railActive':variant==='rail'?'rail':variant==='disabled'?'border':variant==='tabActive'?'accentSoft':'surface');
    if(['quiet','tab'].includes(variant))n.fills=[];
    n.strokes=paint(variant==='focus'?'focus':variant==='secondary'?'border':variant==='tabActive'?'accent':variant==='primary'?'accent':variant==='rail'?'rail':'surface');
    n.strokeWeight=variant==='focus'?2:1;
    const label=txt('按钮',16,['primary','rail','railActive'].includes(variant)?'railText':variant==='disabled'?'secondary':variant==='tabActive'?'accent':'ink',!['quiet','tab','rail','secondary'].includes(variant));
    if(variant==='rail'||variant==='railActive'){
      n.primaryAxisAlignItems='MIN';n.paddingLeft=n.paddingRight=12;n.itemSpacing=12;const icon=track(masters.get('icon/image_text').createInstance());n.appendChild(icon);icon.componentPropertyReferences={mainComponent:buttonIconProp};
    }
    n.appendChild(label);label.componentPropertyReferences={characters:buttonLabelProp};masters.set('button/'+variant,n);ledger.components['button/'+variant]=n.id;
  }
  track(family.componentSet);
  for(const type of ['radio','check'])for(const selected of [false,true]) {
    const n=track(figma.createComponent());n.name='Windows/'+type+'/Selected='+selected;n.resize(18,18);n.fills=paint(selected&&type==='check'?'accent':'surface');n.strokes=paint(selected?'accent':'muted');n.strokeWeight=1.5;n.cornerRadius=type==='radio'?9:3;
    if(selected&&type==='radio'){const e=track(figma.createEllipse());e.resize(8,8);e.x=e.y=5;e.fills=paint('accent');n.appendChild(e);}
    if(selected&&type==='check') {
      const icon=track(figma.createNodeFromSvg(DESIGN.assets.check));n.appendChild(icon);icon.x=icon.y=2;
    }
    n.description='18px 原生选择控件视觉；外层点击范围至少 40px。';componentsArea.appendChild(n);n.x=(type==='radio'?0:64)+(selected?24:0);n.y=180;masters.set(type+'/'+selected,n);ledger.components[type+'/'+selected]=n.id;
  }
}
function destination(action,source) {
  if(action.startsWith('tab:'))return {similarity:'step5',breadth:'breadth5',depth:'depth5'}[action.split(':')[1]];
  // Title choice must never navigate to a different manuscript direction.
  // The HTML review implements independent title state; Figma shows named snapshots.
  if(action.startsWith('candidate:'))return null;
  if(action.startsWith('idea'))return 'step2';
  if(action.startsWith('style'))return 'step3';
  if(action==='topic')return 'step1';
  if(action.startsWith('export'))return 'exportDialog';
  if(['illustrate','handoff'].includes(action))return 'handoffDialog';
  if(action==='close'||action==='confirmExport')return null;
  return action;
}
async function wire() {
  for(const ref of refs) {
    const key=destination(ref.action),target=screenNodes.get(key);
    if(ref.action==='close'||ref.action==='confirmExport') {
      await ref.node.setReactionsAsync([{trigger:{type:'ON_CLICK'},actions:[{type:'CLOSE'}]}]);continue;
    }
    if(!target)continue;
    const overlay=key.endsWith('Dialog');
    await ref.node.setReactionsAsync([{trigger:{type:'ON_CLICK'},actions:[{type:'NODE',destinationId:target.id,navigation:overlay?'OVERLAY':'NAVIGATE',transition:{type:'DISSOLVE',easing:{type:'EASE_OUT'},duration:0.15},resetScrollPosition:true,...(overlay?{overlayRelativePosition:{x:0,y:0}}:{})}]}]);
  }
}
function audit() {
  const all=page.findAll(()=>true);
  const errors=[];
  for(const n of all) {
    if(n.type==='TEXT'&&typeof n.fontSize==='number'&&n.fontSize<14)errors.push({id:n.id,type:'small-font',name:n.name});
    if(!Number.isFinite(n.width)||n.width<=0)errors.push({id:n.id,type:'bad-width',name:n.name});
  }
  const textCount=all.filter(n=>n.type==='TEXT').length;
  return {textCount,instanceCount:all.filter(n=>n.type==='INSTANCE').length,autoLayoutCount:all.filter(n=>'layoutMode'in n&&n.layoutMode!=='NONE').length,errors};
}
async function build() {
  if(figma.fileKey&&figma.fileKey!==DESIGN.targetFile)throw new Error('请在指定 AIDocStudio 热度图文文件中运行。');
  if(!figma.root.children.some(p=>p.id==='0:1'&&p.name.includes('AI 热度图文生成')))throw new Error('目标文件校验失败；没有修改画布。');
  const exists=figma.root.children.find(p=>p.name===DESIGN.page);
  if(exists){await figma.setCurrentPageAsync(exists);throw new Error('Windows 页已存在，已定位到该页。为保留设计，不会重复创建或覆盖。');}
  page=track(figma.createPage());page.name=DESIGN.page;await figma.setCurrentPageAsync(page);ledger.pageId=page.id;ledger.status='building';
  await foundations();
  componentsArea=frame('Windows / 共享控件');page.appendChild(componentsArea);componentsArea.layoutMode='NONE';componentsArea.resize(1900,300);componentsArea.x=100;componentsArea.y=7450;
  await controls();
  let index=0;
  for(const screen of DESIGN.screens) {
    let n;
    if(screen.dialog){
      n=frame(screen.name+' / 居中弹窗');page.appendChild(n);n.resize(1440,1000);n.primaryAxisSizingMode='FIXED';n.counterAxisSizingMode='FIXED';n.primaryAxisAlignItems='CENTER';n.counterAxisAlignItems='CENTER';n.fills=[{type:'SOLID',color:{r:0.05,g:0.1,b:0.09},opacity:0.4}];
      render(screen,n);
    }else n=render(screen,page);
    n.x=100+(index%3)*1504;n.y=160+Math.floor(index/3)*1080;
    screenNodes.set(screen.key,n);ledger.screens[screen.key]={id:n.id,name:n.name,width:n.width,height:n.height};index++;
  }
  for(const binding of styleBindings)await binding.node.setTextStyleIdAsync(binding.styleId);
  componentsArea.y=Math.max(...Array.from(screenNodes.values()).map(n=>n.y+n.height))+160;
  await wire();
  ledger.audit=audit();ledger.createdNodeIds=[page.id,...page.findAll(()=>true).map(n=>n.id)];ledger.status=ledger.audit.errors.length?'built-with-warnings':'complete';
  page.selection=[screenNodes.get('step4')];figma.viewport.scrollAndZoomIntoView(page.selection);
  const cover=screenNodes.get('step4');
  const bytes=await cover.exportAsync({format:'PNG',constraint:{type:'WIDTH',value:1440}});
  figma.ui.postMessage({type:'done',ledger,preview:Array.from(bytes)});
}
const UI=`<html><head><meta charset="utf-8"><style>body{font:14px 'Microsoft YaHei UI',sans-serif;margin:24px;color:#162B2A}h2{font-size:20px}button{font:inherit;background:#197D72;color:white;border:0;border-radius:4px;padding:10px 16px;cursor:pointer}pre{font-size:12px;white-space:pre-wrap;max-height:210px;overflow:auto}a{color:#197D72}textarea{width:100%;height:160px}img{width:100%;margin-top:12px}</style></head><body><h2>Windows 桌面设计稿</h2><p>仅新增“03 · Windows 桌面版”，保留原 Web 设计。包含六步主界面、异常状态、弹窗、控件规范及可点击流程。</p><button id="build">创建可编辑设计</button><pre id="status">等待开始</pre><div id="downloads"></div><img id="preview"><script>document.getElementById('build').onclick=()=>{parent.postMessage({pluginMessage:{type:'build'}},'*');document.getElementById('build').disabled=true;document.getElementById('status').textContent='正在构建设计…'};function save(name,data,type){const a=document.createElement('a');a.textContent='下载 '+name;a.download=name;a.href=URL.createObjectURL(new Blob([data],{type}));a.style.display='block';document.getElementById('downloads').appendChild(a)}onmessage=e=>{const m=e.data.pluginMessage;if(!m)return;if(m.type==='done'){document.getElementById('status').textContent=JSON.stringify(m.ledger,null,2);save('figma-windows-state.json',JSON.stringify(m.ledger,null,2),'application/json');const bytes=new Uint8Array(m.preview);save('windows-step4.png',bytes,'image/png');document.getElementById('preview').src=URL.createObjectURL(new Blob([bytes],{type:'image/png'}))}else{document.getElementById('status').textContent=m.message;document.getElementById('build').disabled=false}}</script></body></html>`;
figma.showUI(UI,{width:540,height:640});
figma.ui.onmessage=async m=>{if(m.type!=='build')return;try{await build();}catch(e){ledger.status='failed';ledger.errors.push(String(e));figma.ui.postMessage({type:'error',message:String(e),ledger});}};
