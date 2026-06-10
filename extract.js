// Extract the lineara.xyz JS data structures into plain JSON.
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const SRC = path.join(__dirname, 'corpus-src');
const OUT = path.join(__dirname, 'data');
fs.mkdirSync(OUT, { recursive: true });

const ctx = {};
vm.createContext(ctx);
for (const f of ['LinearAInscriptions.js', 'words_in_linearb.js']) {
  vm.runInContext(fs.readFileSync(path.join(SRC, f), 'utf8'), ctx);
}

const dump = (name, map) =>
  fs.writeFileSync(path.join(OUT, name + '.json'),
    JSON.stringify(Object.fromEntries(map), null, 1));

dump('inscriptions', ctx.inscriptions);
dump('lexicon', ctx.lexicon);
dump('sequences', ctx.sequences);
dump('wordsInCorpus', ctx.wordsInCorpus);
dump('ligatures', ctx.ligatures);
dump('identicalWordsInLinearB', ctx.identicalWords);
dump('identicalRootsInLinearB', ctx.identicalRoots);
dump('similarWordsInLinearB', ctx.similarWords);

console.log('inscriptions:', ctx.inscriptions.size);
console.log('lexicon:', ctx.lexicon.size);
console.log('sequences:', ctx.sequences.size);
console.log('wordsInCorpus:', ctx.wordsInCorpus.size);
console.log('ligatures:', ctx.ligatures.size);
