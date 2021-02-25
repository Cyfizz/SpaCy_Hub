from ..tokenizer_exceptions import BASE_EXCEPTIONS
from ...symbols import ORTH
from ...util import update_exc


_exc = {}


for orth in [
    "ags.",
    "alb.",
    "ang.",
    "aor.",
    "AWPL",
    "B. L. M.",
    "B. L. P.",
    "bałt.",
    "blm",
    "blm.",
    "blp",
    "blp.",
    "bojkow.",
    "br.",
    "bret.",
    "brus.",
    "bsł.",
    "bułg.",
    "c.b.d.o.",
    "c.b.d.u.",
    "cdn.",
    "celt.",
    "chor.",
    "chorw.",
    "cs.",
    "czakaw.",
    "czes.",
    "d.",
    "daw.",
    "dk",
    "dk.",
    "dł.",
    "dłuż.",
    "DNA",
    "dniem.",
    "dosł.",
    "dr",
    "dubrow.",
    "ekaw.",
    "est.",
    "fiń.",
    "franc.",
    "gal.",
    "germ.",
    "gł.",
    "głęb.",
    "głuż.",
    "gniem.",
    "goc.",
    "godz.",
    "Gorzów Wlkp.",
    "gr",
    "gr.",
    "hebr.",
    "het.",
    "hol.",
    "ie.",
    "ikaw.",
    "irań.",
    "irl.",
    "islandz.",
    "itd.",
    "jekaw.",
    "kajkaw.",
    "kasz.",
    "kirg.",
    "lit.",
    "lm",
    "lp",
    "lp.",
    "łac.",
    "łot.",
    "maced.",
    "mar.",
    "mgr",
    "mies.",
    "mjr",
    "młpol.",
    "moraw.",
    "n.e.",
    "ndk",
    "ndm",
    "ngr.",
    "niem.",
    "nieodm.",
    "nord.",
    "norw.",
    "np.",
    "nr",
    "o.",
    "odc.",
    "ok.",
    "oo.",
    "orm.",
    "oset.",
    "osk.",
    "p.n.",
    "p.n.e.",
    "pchor.",
    "pers.",
    "pie.",
    "pl.",
    "płd.",
    "płn.",
    "podhal.",
    "pol.",
    "połab.",
    "por.",
    "port.",
    "pot.",
    "pow.",
    "ppłk.",
    "ppor.",
    "prekm.",
    "proc.",
    "ps.",
    "pseud.",
    "pskow.",
    "psł.",
    "r.",
    "rad",
    "rez.",
    "rom.",
    "rum.",
    "rus.",
    "sas.",
    "sch.",
    "scs.",
    "sek.",
    "serb.",
    "sierż.",
    "sła.",
    "słe.",
    "słow.",
    "sp. z o.o.",
    "stbułg.",
    "stind.",
    "stpol.",
    "stpr.",
    "strus.",
    "stwniem.",
    "szer.",
    "sztokaw.",
    "szwedz.",
    "śl.",
    "śp.",
    "śrdniem.",
    "śrgniem.",
    "śrirl.",
    "św.",
    "t.",
    "tj.",
    "toch.",
    "tow.",
    "ts.",
    "tur.",
    "tydz.",
    "tzn.",
    "ukr.",
    "ul.",
    "umbr.",
    "UMK",
    "ur.",
    "w/w",
    "wed.",
    "węg.",
    "wg",
    "wlkp.",
    "wlkpol.",
    "właśc.",
    "włos.",
    "ws.",
    "wsch.",
    "wtw",
    "ww.",
    "wyj.",
    "wyr.",
    "z d.",
    "zach.",
    "zakarp.",
    "zł",
    "zm."

]:
    _exc[orth] = [{ORTH: orth}]


TOKENIZER_EXCEPTIONS = update_exc(BASE_EXCEPTIONS, _exc)
