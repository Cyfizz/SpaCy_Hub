# coding: utf8
from __future__ import unicode_literals

from ...symbols import ORTH

_exc = {}

for orth in [
    'G.',
    'J. E.',
    'J. Em.',
    'J.E.',
    'J.Em.',
    'K.',
    'N.',
    'V.',
    'Vt.',
    'a.',
    'a.k.',
    'a.s.',
    'adv.',
    'akad.',
    'aklg.',
    'akt.',
    'al.',
    'ang.',
    'angl.',
    'aps.',
    'apskr.',
    'apyg.',
    'arbat.',
    'asist.',
    'asm.',
    'asm.k.',
    'asmv.',
    'atk.',
    'atsak.',
    'atsisk.',
    'atsisk.sąsk.',
    'atv.',
    'aut.',
    'avd.',
    'b.k.',
    'baud.',
    'biol.',
    'bkl.',
    'bot.',
    'bt.',
    'buv.',
    'ch.',
    'chem.',
    'corp.',
    'd.',
    'dab.',
    'dail.',
    'dek.',
    'deš.',
    'dir.',
    'dirig.',
    'doc.',
    'dol.',
    'dr.',
    'drp.',
    'dvit.',
    'dėst.',
    'dš.',
    'dž.',
    'e.b.',
    'e.bankas',
    'e.p.',
    'e.parašas',
    'e.paštas',
    'e.v.',
    'e.valdžia',
    'egz.',
    'eil.',
    'ekon.',
    'el.',
    'el.bankas',
    'el.p.',
    'el.parašas',
    'el.paštas',
    'el.valdžia',
    'etc.',
    'ež.',
    'fak.',
    'faks.',
    'feat.',
    'filol.',
    'filos.',
    'g.',
    'gen.',
    'geol.',
    'gerb.',
    'gim.',
    'gr.',
    'gv.',
    'gyd.',
    'gyv.',
    'habil.',
    'inc.',
    'insp.',
    'inž.',
    'ir pan.',
    'ir t. t.',
    'isp.',
    'istor.',
    'it.',
    'just.',
    'k.',
    'k. a.',
    'k.a.',
    'kab.',
    'kand.',
    'kart.',
    'kat.',
    'ketv.',
    'kh.',
    'kl.',
    'kln.',
    'km.',
    'kn.',
    'koresp.',
    'kpt.',
    'kr.',
    'kt.',
    'kub.',
    'kun.',
    'kv.',
    'kyš.',
    'l. e. p.',
    'l.e.p.',
    'lenk.',
    'liet.',
    'lot.',
    'lt.',
    'ltd.',
    'ltn.',
    'm.',
    'm.e..',
    'm.m.',
    'mat.',
    'med.',
    'mgnt.',
    'mgr.',
    'min.',
    'mjr.',
    'ml.',
    'mln.',
    'mlrd.',
    'mob.',
    'mok.',
    'moksl.',
    'mokyt.',
    'mot.',
    'mr.',
    'mst.',
    'mstl.',
    'mėn.',
    'nkt.',
    'no.',
    'nr.',
    'ntk.',
    'nuotr.',
    'op.',
    'org.',
    'orig.',
    'p.',
    'p.d.',
    'p.m.e.',
    'p.s.',
    'pab.',
    'pan.',
    'past.',
    'pav.',
    'pavad.',
    'per.',
    'perd.',
    'pirm.',
    'pl.',
    'plg.',
    'plk.',
    'pr.',
    'pr.Kr.',
    'pranc.',
    'proc.',
    'prof.',
    'prom.',
    'prot.',
    'psl.',
    'pss.',
    'pvz.',
    'pšt.',
    'r.',
    'raj.',
    'red.',
    'rez.',
    'rež.',
    'rus.',
    'rš.',
    's.',
    'sav.',
    'saviv.',
    'sek.',
    'sekr.',
    'sen.',
    'sh.',
    'sk.',
    'skg.',
    'skv.',
    'skyr.',
    'sp.',
    'spec.',
    'sr.',
    'st.',
    'str.',
    'stud.',
    'sąs.',
    't.',
    't. p.',
    't. y.',
    't.p.',
    't.t.',
    't.y.',
    'techn.',
    'tel.',
    'teol.',
    'th.',
    'tir.',
    'trit.',
    'trln.',
    'tšk.',
    'tūks.',
    'tūkst.',
    'up.',
    'upl.',
    'v.s.',
    'vad.',
    'val.',
    'valg.',
    'ved.',
    'vert.',
    'vet.',
    'vid.',
    'virš.',
    'vlsč.',
    'vnt.',
    'vok.',
    'vs.',
    'vtv.',
    'vv.',
    'vyr.',
    'vyresn.',
    'zool.',
    'Įn',
    'įl.',
    'š.m.',
    'šnek.',
    'šv.',
    'švč.',
    'ž.ū.',
    'žin.',
    'žml.',
    'žr.'
]:
    _exc[orth] = [{ORTH: orth}]

TOKENIZER_EXCEPTIONS = _exc
