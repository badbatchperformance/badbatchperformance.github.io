// Movement demo videos. The movement → video list ships encrypted (demos.enc.json);
// the key only travels in the URL fragment (#k=...) printed in the gym's TV QR code.
window.BBDemos = (() => {
  const b64 = s => Uint8Array.from(atob(s.replace(/-/g, '+').replace(/_/g, '/')), c => c.charCodeAt(0));

  function getKey() {
    const k = new URLSearchParams(location.hash.slice(1)).get('k');
    try { if (k) localStorage.setItem('bbDemoKey', k); } catch (e) {}
    if (k) return k;
    try { return localStorage.getItem('bbDemoKey'); } catch (e) { return null; }
  }

  async function load(k) {
    if (!k || !crypto.subtle) return null;
    try {
      const enc = await (await fetch(`demos.enc.json?v=${Date.now()}`, { cache: 'no-store' })).json();
      const key = await crypto.subtle.importKey('raw', b64(k), 'AES-GCM', false, ['decrypt']);
      const plain = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: b64(enc.iv) }, key, b64(enc.ct));
      return index(JSON.parse(new TextDecoder().decode(plain)));
    } catch (e) { return null; }
  }

  // Same normalizing on both sides so "KB Swings" finds "Kettlebell Swings", etc.
  function norm(s) {
    return ' ' + String(s).toLowerCase()
      .replace(/\(.*?\)/g, ' ')
      .replace(/\bdb\b/g, 'dumbbell').replace(/\bkb\b/g, 'kettlebell')
      .replace(/\bmb\b|\bmed ball\b/g, 'medicine ball')
      .replace(/['’]/g, '').replace(/[^a-z0-9]+/g, ' ')
      .split(' ').filter(Boolean).map(w => (w.length > 2 && w.endsWith('s') && !w.endsWith('ss')) ? w.slice(0, -1) : w)
      .join(' ') + ' ';
  }

  function index({ videos, aliases }) {
    const lib = Object.entries(videos).map(([name, id]) => ({ name, id, key: norm(name) }))
      .sort((a, b) => b.key.length - a.key.length); // longest match wins
    const byName = Object.fromEntries(lib.map(v => [v.name, v]));
    const alias = Object.entries(aliases || {}).map(([a, name]) => ({ key: norm(a), v: byName[name] })).filter(x => x.v);
    return { lib, alias };
  }

  // Find the video for one movement name (or null).
  function match(db, text) {
    if (!db) return null;
    const t = norm(text);
    const exact = db.alias.find(a => a.key === t);
    if (exact) return exact.v;
    // A dumbbell/kettlebell version of a barbell lift shouldn't show the barbell video.
    const implement = /\s(dumbbell|kettlebell)\s/.test(t);
    const barbellOnly = / (bench press|push press|strict press|back squat|front squat) $/;
    const lib = db.lib.find(v => t.includes(v.key) && !(implement && barbellOnly.test(v.key) && !/(dumbbell|kettlebell)/.test(v.key)));
    if (lib) return lib;
    // Loose alias match, but never hand a dumbbell movement the barbell video.
    return db.alias.find(a => t.includes(a.key) && !(t.includes(' dumbbell ') && !a.key.includes('dumbbell')))?.v || null;
  }

  // Split a workout into individual movement names, tagged by section.
  function movements(wod) {
    const out = [];
    const add = (section, s) => String(s).split(/→|\+|·|,|:|;| then /).forEach(p => {
      const name = p.replace(/[×x]\s*[\d(].*$/, '').replace(/^\s*(min \d+|odd|even|\d+(\/\d+)?\s*(cal|yd|m|sec)?)\b/i, '').trim();
      if (name.length > 3) out.push({ section, name });
    });
    add('Warm-up', wod.warmup);
    (wod.jumps || []).forEach(j => add('Jumps', /contrast/i.test(j[0]) ? j[1] : j[0]));
    (wod.strength || []).forEach(j => add('Strength', j[0]));
    (wod.cond?.items || []).forEach(i => add('Metcon', i));
    return out;
  }

  // Unique [{section, name, video}] for a day, in workout order.
  function forDay(db, wod) {
    const seen = new Set(), list = [];
    for (const m of movements(wod)) {
      const v = match(db, m.name);
      if (v && !seen.has(v.id)) { seen.add(v.id); list.push({ ...m, video: v }); }
    }
    return list;
  }

  return { getKey, load, match, forDay };
})();
