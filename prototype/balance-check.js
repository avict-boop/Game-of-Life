// Прогон стратегий без отрисовки: node prototype/balance-check.js flagchemo|photo|small|none (нужен playwright).
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  const fs=require('fs'); const html=fs.readFileSync(require('path').join(__dirname,'index.html'),'utf8');
  await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>');
  await p.waitForTimeout(200);
  const strat = process.argv[2] || 'none';
  const r = await p.evaluate(strat => {
    // отключаем раннюю победу: смотрим чистую траекторию долей
    const out=[];
    const pref = {none:[], flagchemo:['flag','chemo','etc','capsule','repair'], photo:['etc','photo','small','capsule','repair'], small:['small','small','slim','etc','capsule']}[strat];
    for (let run=0; run<6; run++) {
      restart(); const sh=[];
      for (let gen=0; gen<10; gen++) {
        while (S.t < LIFE) step(1/30);
        const c=countLin(), tot=c.own+c.ferm+c.purp; sh.push(Math.round(c.own/tot*100));
        if (c.own===0) break;
        const ids=draft(); const want=pref.find(x=>ids.includes(x) && cardAllowed(S.genomes.own,x));
        if (want) takeCard(S.genomes.own,want);
        S.history.push({}); nextGeneration();
      }
      out.push(sh.join(' '));
    }
    return out;
  }, strat);
  console.log(strat); r.forEach(x=>console.log('  '+x));
  await b.close();
})();
