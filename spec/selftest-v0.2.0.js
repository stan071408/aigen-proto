const {chromium}=require('/var/tmp/sand-playwright-runtime/94507eada9e1d0027bcd4ac5ae198dee/node_modules/playwright-core');
const FILE='/workspace/aigen-platform/spec/AIGenPlatform控件规范-261112-v0.2.0.html';
const R=[];
const ok=(n,c,d='')=>{R.push({n,pass:!!c,d});console.log(c?'PASS':'FAIL',n,c?'':d)};
(async()=>{
  const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
  const ctx=await b.newContext({viewport:{width:1366,height:768}});
  const p=await ctx.newPage();
  p.setDefaultTimeout(8000);
  const errs=[], reqs=[];
  p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
  p.on('pageerror',e=>errs.push(String(e)));
  p.on('requestfailed',r=>reqs.push(r.url()+' '+r.failure().errorText));
  p.on('request',r=>{
    const u=r.url();
    if(/^https?:/i.test(u) && !u.startsWith('file:')) reqs.push('external '+u);
  });
  await p.goto('file://'+FILE,{waitUntil:'domcontentloaded'});
  await p.waitForTimeout(500);

  ok('顶栏标注「控件规范 · 已确认（2026-11-12）」', await p.evaluate(()=>{
    const n=document.querySelector('header .note')?.textContent||'';
    const f=[...document.querySelectorAll('main > .foot')].pop()?.textContent||'';
    return n.includes('控件规范 · 已确认（2026-11-12）') && f.includes('控件规范 · 已确认（2026-11-12）');
  }));

  const overflow=await p.evaluate(()=>{
    const doc=document.documentElement;
    return {scrollW:doc.scrollWidth, clientW:doc.clientWidth, bodyW:document.body.scrollWidth};
  });
  ok('无横向溢出', overflow.scrollW<=1366+1 && overflow.bodyW<=1366+1, JSON.stringify(overflow));

  // tokens exist
  ok('主色与控件令牌已定义', await p.evaluate(()=>{
    const s=getComputedStyle(document.documentElement);
    return s.getPropertyValue('--accent').trim()==='#1c5fc4'
      && s.getPropertyValue('--ctl-h').trim()==='36px'
      && s.getPropertyValue('--ctl-radius').trim()==='12px'
      && s.getPropertyValue('--ctl-border').trim()==='#6b7c94'
      && s.getPropertyValue('--ctl-border-w').trim()==='2px';
  }));

  ok('已定结论区存在且无拍板表单', await p.evaluate(()=>!!document.querySelector('#sec-picks .decided')&&!document.querySelector('#picksForm')));
  const chkApp=await p.evaluate(()=>{
    const el=document.querySelector('#sec-choice input[type=checkbox]');
    const cs=getComputedStyle(el);
    return {app:cs.appearance||cs.webkitAppearance, w:Math.round(el.getBoundingClientRect().width), r:cs.borderRadius};
  });
  ok('勾选自绘 appearance:none 且 16px', /none/.test(chkApp.app)&&chkApp.w===16, JSON.stringify(chkApp));

  // buttons loading
  await p.click('#btnLoad');
  ok('按钮加载切换为「生成中…」且有 spinner', await p.evaluate(()=>{
    const b=document.querySelector('#btnLoad');
    const spin=b.querySelector('.spin');
    const txt=b.querySelector('.txt');
    return !spin.hidden && txt.textContent==='生成中…';
  }));
  await p.click('#btnLoad');
  ok('加载示例可再点切回', await p.evaluate(()=>{
    const b=document.querySelector('#btnLoad');
    return b.querySelector('.spin').hidden && b.querySelector('.txt').textContent==='开始生成';
  }));

  // gen scene
  await p.click('#genStart');
  ok('生成原稿进入加载并出现取消', await p.evaluate(()=>{
    const start=document.querySelector('#genStart');
    const cancel=document.querySelector('#genCancel');
    return start.disabled && !cancel.hidden && start.querySelector('.txt').textContent==='生成中…';
  }));
  const cancelBox=await p.evaluate(()=>{
    const el=document.querySelector('#genCancel');
    const s=getComputedStyle(el);
    return {h:Math.round(el.getBoundingClientRect().height), r:s.borderRadius, bw:s.borderTopWidth, bc:s.borderTopColor, bg:s.backgroundColor};
  });
  ok('取消为次要按钮（高36、圆角12、1px描边）', cancelBox.h===36 && cancelBox.r==='12px' && cancelBox.bw==='1px', JSON.stringify(cancelBox));
  await p.click('#genCancel');
  ok('取消后出现重试', await p.evaluate(()=>!document.querySelector('#genRetry').hidden && document.querySelector('#genStart').hidden));
  await p.click('#genRetry');
  ok('重试回到生成中', await p.evaluate(()=>!document.querySelector('#genStart').hidden && document.querySelector('#genStart').querySelector('.txt').textContent==='生成中…'));

  // textarea count
  const taN=await p.evaluate(()=>document.querySelector('#taCount').textContent);
  ok('textarea 字数已统计', Number(taN)>0, taN);
  await p.fill('#taDemo','测试字数');
  ok('textarea 字数随输入更新', await p.evaluate(()=>document.querySelector('#taCount').textContent==='4'));

  // search clear
  await p.click('#searchClr');
  ok('搜索清除', await p.evaluate(()=>document.querySelector('#searchDemo').value===''));

  // number stepper
  const before=await p.inputValue('#titleCount');
  await p.click('#titleCount ~ .ctl-spin [data-dir="1"]');
  const after=await p.inputValue('#titleCount');
  ok('数字框 +1', Number(after)===Number(before)+1, before+'→'+after);
  await p.evaluate(()=>{
    const el=document.querySelector('#titleCount');
    el.focus();
    el.value='';
    el.dispatchEvent(new Event('input',{bubbles:true}));
    el.dispatchEvent(new FocusEvent('focusout',{bubbles:true}));
  });
  ok('非法值失焦回退', await p.evaluate(()=>{
    const el=document.querySelector('#titleCount');
    return el.value!=='' && Number.isFinite(Number(el.value));
  }));

  // disabled number stays 5
  ok('整框禁用数字不变', await p.evaluate(()=>{
    const inp=document.querySelector('.ctl-step.is-disabled input');
    return inp && inp.disabled && inp.value==='5';
  }));

  // range
  ok('字数范围 800—1200', await p.evaluate(()=>document.querySelector('#wordMin').value==='800' && document.querySelector('#wordMax').value==='1200'));

  // number style
  const numStyle=await p.evaluate(()=>{
    const box=document.querySelector('#titleCount').closest('.ctl-step');
    const s=getComputedStyle(box);
    const inp=getComputedStyle(document.querySelector('#titleCount'));
    const spin=box.querySelector('.ctl-spin');
    return {
      w:Math.round(box.getBoundingClientRect().width),
      h:Math.round(box.getBoundingClientRect().height),
      r:s.borderRadius, bw:s.borderTopWidth, bc:s.borderTopColor,
      align:inp.textAlign, padL:inp.paddingLeft, spinW:Math.round(spin.getBoundingClientRect().width),
      shadow:s.boxShadow
    };
  });
  ok('数字框规格 92×36、圆角12、2px描边、数字靠左、箭头竖条22',
    numStyle.w===92 && numStyle.h===36 && numStyle.r==='12px' && numStyle.bw==='2px'
    && numStyle.align==='left' && numStyle.padL==='12px' && numStyle.spinW===22,
    JSON.stringify(numStyle));

  // select
  await p.click('#demoMode .sel-btn');
  ok('下拉展开', await p.evaluate(()=>document.querySelector('#demoMode').classList.contains('open')));
  await p.click('#demoMode .sel-opt[data-v="api"]');
  ok('下拉选「API 生图」', await p.evaluate(()=>{
    const btn=document.querySelector('#demoMode .sel-btn');
    return !document.querySelector('#demoMode').classList.contains('open') && btn.textContent.trim()==='API 生图';
  }));

  // tags
  const tagN0=await p.evaluate(()=>document.querySelectorAll('#tagBox .tag').length);
  await p.click('#tagAdd');
  ok('多选标签可增加', await p.evaluate(n=>document.querySelectorAll('#tagBox .tag').length===n+1, tagN0));
  await p.click('#tagBox .tag button');
  ok('多选标签可移除', await p.evaluate(n=>document.querySelectorAll('#tagBox .tag').length===n, tagN0));

  // switch
  await p.click('label.switch:has(#swDemo)');
  ok('开关可切换', await p.evaluate(()=>!document.querySelector('#swDemo').checked));

  // choice cards
  await p.click('#sourceCards label.choice-card:nth-child(2)');
  ok('单选卡可切换', await p.evaluate(()=>document.querySelector('#sourceCards input[value="library"]').checked));

  // tabs
  await p.click('#segDemo button[data-seg="direct"]');
  ok('一级标签可切换', await p.evaluate(()=>document.querySelector('#segHint').textContent.includes('直接指定标题') && document.querySelector('#segDemo button[data-seg="direct"]').classList.contains('on')));

  // capsules
  await p.click('.caps .cap:nth-child(3)');
  ok('二级胶囊可勾选', await p.evaluate(()=>document.querySelector('.caps .cap:nth-child(3) input').checked));

  // progress, toast, modal
  await p.click('#progGo');
  await p.waitForTimeout(400);
  ok('进度条开始增长', await p.evaluate(()=>{
    const w=document.querySelector('#progBar').style.width;
    return parseFloat(w)>20;
  }));
  await p.click('#toastOk');
  ok('成功 Toast 出现', await p.evaluate(()=>!!document.querySelector('#toasts .toast.ok')));
  await p.click('#openModal');
  ok('确认弹窗打开', await p.evaluate(()=>!document.querySelector('#modalBg').hidden));
  await p.click('#modalCancel');
  ok('确认弹窗可取消', await p.evaluate(()=>document.querySelector('#modalBg').hidden));

  // form validate
  await p.click('#formSubmit');
  ok('空主题校验出现错误', await p.evaluate(()=>!document.querySelector('#formTopicErr').hidden && document.querySelector('#formTopic').classList.contains('is-invalid')));
  await p.fill('#formTopic','社区生活的新变化');
  ok('填入主题后错误消失', await p.evaluate(()=>document.querySelector('#formTopicErr').hidden && !document.querySelector('#formTopic').classList.contains('is-invalid')));

  // no native form navigation
  const url=p.url();
  ok('未发生原生表单跳转', url.startsWith('file://') && decodeURIComponent(url).includes('AIGenPlatform控件规范-261112-v0.2.0.html') && !url.includes('?'));

  // clean white input (no inset shadow)
  ok('文本输入为干净白底无内阴影', await p.evaluate(()=>{
    const s=getComputedStyle(document.querySelector('#topicDemo'));
    return s.boxShadow==='none' && s.backgroundColor==='rgb(255, 255, 255)';
  }));

  await p.waitForTimeout(200);
  ok('无控制台错误、无 pageerror、无外部请求', errs.length===0 && reqs.length===0, JSON.stringify({errs,reqs}));

  const fail=R.filter(x=>!x.pass);
  console.log('\nRESULT', R.filter(x=>x.pass).length+'/'+R.length, 'failed', fail.length);
  if(fail.length) fail.forEach(x=>console.log(' -', x.n, x.d));
  await b.close();
  process.exit(fail.length?1:0);
})().catch(e=>{console.error(e);process.exit(2)});
