from ..tokenizer_exceptions import BASE_EXCEPTIONS
from ...symbols import ORTH, NORM
from ...util import update_exc

_exc = {}

_abbrev_exc = [
    # Weekdays abbreviations
    {ORTH: "пн", NORM: "понедельник"},
    {ORTH: "вт", NORM: "вторник"},
    {ORTH: "ср", NORM: "среда"},
    {ORTH: "чт", NORM: "четверг"},
    {ORTH: "чтв", NORM: "четверг"},
    {ORTH: "пт", NORM: "пятница"},
    {ORTH: "сб", NORM: "суббота"},
    {ORTH: "сбт", NORM: "суббота"},
    {ORTH: "вс", NORM: "воскресенье"},
    {ORTH: "вскр", NORM: "воскресенье"},
    {ORTH: "воскр", NORM: "воскресенье"},
    # Months abbreviations
    {ORTH: "янв", NORM: "январь"},
    {ORTH: "фев", NORM: "февраль"},
    {ORTH: "февр", NORM: "февраль"},
    {ORTH: "мар", NORM: "март"},
    # {ORTH: "март", NORM: "март"},
    {ORTH: "мрт", NORM: "март"},
    {ORTH: "апр", NORM: "апрель"},
    # {ORTH: "май", NORM: "май"},
    {ORTH: "июн", NORM: "июнь"},
    # {ORTH: "июнь", NORM: "июнь"},
    {ORTH: "июл", NORM: "июль"},
    # {ORTH: "июль", NORM: "июль"},
    {ORTH: "авг", NORM: "август"},
    {ORTH: "сен", NORM: "сентябрь"},
    {ORTH: "сент", NORM: "сентябрь"},
    {ORTH: "окт", NORM: "октябрь"},
    {ORTH: "октб", NORM: "октябрь"},
    {ORTH: "ноя", NORM: "ноябрь"},
    {ORTH: "нояб", NORM: "ноябрь"},
    {ORTH: "нбр", NORM: "ноябрь"},
    {ORTH: "дек", NORM: "декабрь"},
]

for abbrev_desc in _abbrev_exc:
    abbrev = abbrev_desc[ORTH]
    for orth in (abbrev, abbrev.capitalize(), abbrev.upper()):
        _exc[orth] = [{ORTH: orth, NORM: abbrev_desc[NORM]}]
        _exc[orth + "."] = [{ORTH: orth + ".", NORM: abbrev_desc[NORM]}]


for abbr in [
    # Year slang abbreviations
    {ORTH: "2к15", NORM: "2015"},
    {ORTH: "2к16", NORM: "2016"},
    {ORTH: "2к17", NORM: "2017"},
    {ORTH: "2к18", NORM: "2018"},
    {ORTH: "2к19", NORM: "2019"},
    {ORTH: "2к20", NORM: "2020"},
    {ORTH: "2к21", NORM: "2021"},
    {ORTH: "2к22", NORM: "2022"},
    {ORTH: "2к23", NORM: "2023"},
    {ORTH: "2к24", NORM: "2024"},
    {ORTH: "2к25", NORM: "2025"},
]:
    _exc[abbr[ORTH]] = [abbr]

for abbr in [
    # Profession and academic titles abbreviations
    {ORTH: "ак.", NORM: "академик"},
    {ORTH: "акад.", NORM: "академик"},
    {ORTH: "д-р архитектуры", NORM: "доктор архитектуры"},
    {ORTH: "д-р биол. наук", NORM: "доктор биологических наук"},
    {ORTH: "д-р ветеринар. наук", NORM: "доктор ветеринарных наук"},
    {ORTH: "д-р воен. наук", NORM: "доктор военных наук"},
    {ORTH: "д-р геогр. наук", NORM: "доктор географических наук"},
    {ORTH: "д-р геол.-минерал. наук", NORM: "доктор геолого-минералогических наук"},
    {ORTH: "д-р искусствоведения", NORM: "доктор искусствоведения"},
    {ORTH: "д-р ист. наук", NORM: "доктор исторических наук"},
    {ORTH: "д-р культурологии", NORM: "доктор культурологии"},
    {ORTH: "д-р мед. наук", NORM: "доктор медицинских наук"},
    {ORTH: "д-р пед. наук", NORM: "доктор педагогических наук"},
    {ORTH: "д-р полит. наук", NORM: "доктор политических наук"},
    {ORTH: "д-р психол. наук", NORM: "доктор психологических наук"},
    {ORTH: "д-р с.-х. наук", NORM: "доктор сельскохозяйственных наук"},
    {ORTH: "д-р социол. наук", NORM: "доктор социологических наук"},
    {ORTH: "д-р техн. наук", NORM: "доктор технических наук"},
    {ORTH: "д-р фармацевт. наук", NORM: "доктор фармацевтических наук"},
    {ORTH: "д-р физ.-мат. наук", NORM: "доктор физико-математических наук"},
    {ORTH: "д-р филол. наук", NORM: "доктор филологических наук"},
    {ORTH: "д-р филос. наук", NORM: "доктор философских наук"},
    {ORTH: "д-р хим. наук", NORM: "доктор химических наук"},
    {ORTH: "д-р экон. наук", NORM: "доктор экономических наук"},
    {ORTH: "д-р юрид. наук", NORM: "доктор юридических наук"},
    {ORTH: "д-р", NORM: "доктор"},
    {ORTH: "д.б.н.", NORM: "доктор биологических наук"},
    {ORTH: "д.г.-м.н.", NORM: "доктор геолого-минералогических наук"},
    {ORTH: "д.г.н.", NORM: "доктор географических наук"},
    {ORTH: "д.и.н.", NORM: "доктор исторических наук"},
    {ORTH: "д.иск.", NORM: "доктор искусствоведения"},
    {ORTH: "д.м.н.", NORM: "доктор медицинских наук"},
    {ORTH: "д.п.н.", NORM: "доктор психологических наук"},
    {ORTH: "д.пед.н.", NORM: "доктор педагогических наук"},
    {ORTH: "д.полит.н.", NORM: "доктор политических наук"},
    {ORTH: "д.с.-х.н.", NORM: "доктор сельскохозяйственных наук"},
    {ORTH: "д.социол.н.", NORM: "доктор социологических наук"},
    {ORTH: "д.т.н.", NORM: "доктор технических наук"},
    {ORTH: "д.т.н", NORM: "доктор технических наук"},
    {ORTH: "д.ф.-м.н.", NORM: "доктор физико-математических наук"},
    {ORTH: "д.ф.н.", NORM: "доктор филологических наук"},
    {ORTH: "д.филос.н.", NORM: "доктор философских наук"},
    {ORTH: "д.фил.н.", NORM: "доктор филологических наук"},
    {ORTH: "д.х.н.", NORM: "доктор химических наук"},
    {ORTH: "д.э.н.", NORM: "доктор экономических наук"},
    {ORTH: "д.э.н", NORM: "доктор экономических наук"},
    {ORTH: "д.ю.н.", NORM: "доктор юридических наук"},
    {ORTH: "доц.", NORM: "доцент"},
    {ORTH: "и.о.", NORM: "исполняющий обязанности"},
    {ORTH: "к.б.н.", NORM: "кандидат биологических наук"},
    {ORTH: "к.воен.н.", NORM: "кандидат военных наук"},
    {ORTH: "к.г.-м.н.", NORM: "кандидат геолого-минералогических наук"},
    {ORTH: "к.г.н.", NORM: "кандидат географических наук"},
    {ORTH: "к.геогр.н", NORM: "кандидат географических наук"},
    {ORTH: "к.геогр.наук", NORM: "кандидат географических наук"},
    {ORTH: "к.и.н.", NORM: "кандидат исторических наук"},
    {ORTH: "к.иск.", NORM: "кандидат искусствоведения"},
    {ORTH: "к.м.н.", NORM: "кандидат медицинских наук"},
    {ORTH: "к.п.н.", NORM: "кандидат психологических наук"},
    {ORTH: "к.псх.н.", NORM: "кандидат психологических наук"},
    {ORTH: "к.пед.н.", NORM: "кандидат педагогических наук"},
    {ORTH: "канд.пед.наук", NORM: "кандидат педагогических наук"},
    {ORTH: "к.полит.н.", NORM: "кандидат политических наук"},
    {ORTH: "к.с.-х.н.", NORM: "кандидат сельскохозяйственных наук"},
    {ORTH: "к.социол.н.", NORM: "кандидат социологических наук"},
    {ORTH: "к.с.н.", NORM: "кандидат социологических наук"},
    {ORTH: "к.т.н.", NORM: "кандидат технических наук"},
    {ORTH: "к.ф.-м.н.", NORM: "кандидат физико-математических наук"},
    {ORTH: "к.ф.н.", NORM: "кандидат филологических наук"},
    {ORTH: "к.фил.н.", NORM: "кандидат филологических наук"},
    {ORTH: "к.филол.н", NORM: "кандидат филологических наук"},
    {ORTH: "к.фарм.наук", NORM: "кандидат фармакологических наук"},
    {ORTH: "к.фарм.н.", NORM: "кандидат фармакологических наук"},
    {ORTH: "к.фарм.н", NORM: "кандидат фармакологических наук"},
    {ORTH: "к.филос.наук", NORM: "кандидат философских наук"},
    {ORTH: "к.филос.н.", NORM: "кандидат философских наук"},
    {ORTH: "к.филос.н", NORM: "кандидат философских наук"},
    {ORTH: "к.х.н.", NORM: "кандидат химических наук"},
    {ORTH: "к.х.н", NORM: "кандидат химических наук"},
    {ORTH: "к.э.н.", NORM: "кандидат экономических наук"},
    {ORTH: "к.э.н", NORM: "кандидат экономических наук"},
    {ORTH: "к.ю.н.", NORM: "кандидат юридических наук"},
    {ORTH: "к.ю.н", NORM: "кандидат юридических наук"},
    {ORTH: "канд. архитектуры", NORM: "кандидат архитектуры"},
    {ORTH: "канд. биол. наук", NORM: "кандидат биологических наук"},
    {ORTH: "канд. ветеринар. наук", NORM: "кандидат ветеринарных наук"},
    {ORTH: "канд. воен. наук", NORM: "кандидат военных наук"},
    {ORTH: "канд. геогр. наук", NORM: "кандидат географических наук"},
    {ORTH: "канд. геол.-минерал. наук", NORM: "кандидат геолого-минералогических наук"},
    {ORTH: "канд. искусствоведения", NORM: "кандидат искусствоведения"},
    {ORTH: "канд. ист. наук", NORM: "кандидат исторических наук"},
    {ORTH: "к.ист.н.", NORM: "кандидат исторических наук"},
    {ORTH: "канд. культурологии", NORM: "кандидат культурологии"},
    {ORTH: "канд. мед. наук", NORM: "кандидат медицинских наук"},
    {ORTH: "канд. пед. наук", NORM: "кандидат педагогических наук"},
    {ORTH: "канд. полит. наук", NORM: "кандидат политических наук"},
    {ORTH: "канд. психол. наук", NORM: "кандидат психологических наук"},
    {ORTH: "канд. с.-х. наук", NORM: "кандидат сельскохозяйственных наук"},
    {ORTH: "канд. социол. наук", NORM: "кандидат социологических наук"},
    {ORTH: "к.соц.наук", NORM: "кандидат социологических наук"},
    {ORTH: "к.соц.н.", NORM: "кандидат социологических наук"},
    {ORTH: "к.соц.н", NORM: "кандидат социологических наук"},
    {ORTH: "канд. техн. наук", NORM: "кандидат технических наук"},
    {ORTH: "канд. фармацевт. наук", NORM: "кандидат фармацевтических наук"},
    {ORTH: "канд. физ.-мат. наук", NORM: "кандидат физико-математических наук"},
    {ORTH: "канд. филол. наук", NORM: "кандидат филологических наук"},
    {ORTH: "канд. филос. наук", NORM: "кандидат философских наук"},
    {ORTH: "канд. хим. наук", NORM: "кандидат химических наук"},
    {ORTH: "канд. экон. наук", NORM: "кандидат экономических наук"},
    {ORTH: "канд. юрид. наук", NORM: "кандидат юридических наук"},
    {ORTH: "в.н.с.", NORM: "ведущий научный сотрудник"},
    {ORTH: "мл. науч. сотр.", NORM: "младший научный сотрудник"},
    {ORTH: "м.н.с.", NORM: "младший научный сотрудник"},
    {ORTH: "проф.", NORM: "профессор"},
    {ORTH: "профессор.кафедры", NORM: "профессор кафедры"},
    {ORTH: "ст. науч. сотр.", NORM: "старший научный сотрудник"},
    {ORTH: "чл.-к.", NORM: "член корреспондент"},
    {ORTH: "чл.-корр.", NORM: "член-корреспондент"},
    {ORTH: "чл.-кор.", NORM: "член-корреспондент"},
    {ORTH: "дир.", NORM: "директор"},
    {ORTH: "зам. дир.", NORM: "заместитель директора"},
    {ORTH: "зав. каф.", NORM: "заведующий кафедрой"},
    {ORTH: "зав.кафедрой", NORM: "заведующий кафедрой"},
    {ORTH: "зав. кафедрой", NORM: "заведующий кафедрой"},
    {ORTH: "асп.", NORM: "аспирант"},
    {ORTH: "гл. науч. сотр.", NORM: "главный научный сотрудник"},
    {ORTH: "вед. науч. сотр.", NORM: "ведущий научный сотрудник"},
    {ORTH: "науч. сотр.", NORM: "научный сотрудник"},
    {ORTH: "к.м.с.", NORM: "кандидат в мастера спорта"},
]:
    _exc[abbr[ORTH]] = [abbr]


for abbr in [
    # Literary phrases abbreviations
    {ORTH: "и т.д.", NORM: "и так далее"},
    {ORTH: "и т.п.", NORM: "и тому подобное"},
    {ORTH: "т.д.", NORM: "так далее"},
    {ORTH: "т.п.", NORM: "тому подобное"},
    {ORTH: "т.е.", NORM: "то есть"},
    {ORTH: "т.к.", NORM: "так как"},
    {ORTH: "в т.ч.", NORM: "в том числе"},
    {ORTH: "и пр.", NORM: "и прочие"},
    {ORTH: "и др.", NORM: "и другие"},
    {ORTH: "т.н.", NORM: "так называемый"}
]:
    _exc[abbr[ORTH]] = [abbr]


for abbr in [
    # Appeal to a person abbreviations
    {ORTH: "г-н", NORM: "господин"},
    {ORTH: "г-да", NORM: "господа"},
    {ORTH: "г-жа", NORM: "госпожа"},
    {ORTH: "тов.", NORM: "товарищ"}
]:
    _exc[abbr[ORTH]] = [abbr]


for abbr in [
    # Time periods abbreviations
    {ORTH: "до н.э.", NORM: "до нашей эры"},
    {ORTH: "по н.в.", NORM: "по настоящее время"},
    {ORTH: "в н.в.", NORM: "в настоящее время"},
    {ORTH: "наст.", NORM: "настоящий"},
    {ORTH: "наст. время", NORM: "настоящее время"},
    {ORTH: "г.г.", NORM: "годы"},
    {ORTH: "гг.", NORM: "годы"},
    {ORTH: "т.г.", NORM: "текущий год"}
]:
    _exc[abbr[ORTH]] = [abbr]


for abbr in [
    # Address forming elements abbreviations
    {ORTH: "респ.", NORM: "республика"},
    {ORTH: "обл.", NORM: "область"},
    {ORTH: "г.ф.з.", NORM: "город федерального значения"},
    {ORTH: "а.обл.", NORM: "автономная область"},
    {ORTH: "а.окр.", NORM: "автономный округ"},
    {ORTH: "м.р-н", NORM: "муниципальный район"},
    {ORTH: "г.о.", NORM: "городской округ"},
    {ORTH: "г.п.", NORM: "городское поселение"},
    {ORTH: "с.п.", NORM: "сельское поселение"},
    {ORTH: "вн.р-н", NORM: "внутригородской район"},
    {ORTH: "вн.тер.г.", NORM: "внутригородская территория города"},
    {ORTH: "пос.", NORM: "поселение"},
    {ORTH: "р-н", NORM: "район"},
    {ORTH: "с/с", NORM: "сельсовет"},
    {ORTH: "г.", NORM: "город"},
    {ORTH: "п.г.т.", NORM: "поселок городского типа"},
    {ORTH: "пгт.", NORM: "поселок городского типа"},
    {ORTH: "р.п.", NORM: "рабочий поселок"},
    {ORTH: "рп.", NORM: "рабочий поселок"},
    {ORTH: "кп.", NORM: "курортный поселок"},
    {ORTH: "гп.", NORM: "городской поселок"},
    {ORTH: "п.", NORM: "поселок"},
    {ORTH: "в-ки", NORM: "выселки"},
    {ORTH: "г-к", NORM: "городок"},
    {ORTH: "з-ка", NORM: "заимка"},
    {ORTH: "п-к", NORM: "починок"},
    {ORTH: "киш.", NORM: "кишлак"},
    {ORTH: "п. ст. ", NORM: "поселок станция"},
    {ORTH: "п. ж/д ст. ", NORM: "поселок при железнодорожной станции"},
    {ORTH: "ж/д бл-ст", NORM: "железнодорожный блокпост"},
    {ORTH: "ж/д б-ка", NORM: "железнодорожная будка"},
    {ORTH: "ж/д в-ка", NORM: "железнодорожная ветка"},
    {ORTH: "ж/д к-ма", NORM: "железнодорожная казарма"},
    {ORTH: "ж/д к-т", NORM: "железнодорожный комбинат"},
    {ORTH: "ж/д пл-ма", NORM: "железнодорожная платформа"},
    {ORTH: "ж/д пл-ка", NORM: "железнодорожная площадка"},
    {ORTH: "ж/д п.п.", NORM: "железнодорожный путевой пост"},
    {ORTH: "ж/д о.п.", NORM: "железнодорожный остановочный пункт"},
    {ORTH: "ж/д рзд.", NORM: "железнодорожный разъезд"},
    {ORTH: "ж/д ст. ", NORM: "железнодорожная станция"},
    {ORTH: "м-ко", NORM: "местечко"},
    {ORTH: "д.", NORM: "деревня"},
    {ORTH: "с.", NORM: "село"},
    {ORTH: "сл.", NORM: "слобода"},
    {ORTH: "ст. ", NORM: "станция"},
    {ORTH: "ст-ца", NORM: "станица"},
    {ORTH: "у.", NORM: "улус"},
    {ORTH: "х.", NORM: "хутор"},
    {ORTH: "рзд.", NORM: "разъезд"},
    {ORTH: "зим.", NORM: "зимовье"},
    {ORTH: "б-г", NORM: "берег"},
    {ORTH: "ж/р", NORM: "жилой район"},
    {ORTH: "кв-л", NORM: "квартал"},
    {ORTH: "мкр.", NORM: "микрорайон"},
    {ORTH: "ост-в", NORM: "остров"},
    {ORTH: "платф.", NORM: "платформа"},
    {ORTH: "п/р", NORM: "промышленный район"},
    {ORTH: "р-н", NORM: "район"},
    {ORTH: "тер.", NORM: "территория"},
    {ORTH: "тер. СНО", NORM: "территория садоводческих некоммерческих объединений граждан"},
    {ORTH: "тер. ОНО", NORM: "территория огороднических некоммерческих объединений граждан"},
    {ORTH: "тер. ДНО", NORM: "территория дачных некоммерческих объединений граждан"},
    {ORTH: "тер. СНТ", NORM: "территория садоводческих некоммерческих товариществ"},
    {ORTH: "тер. ОНТ", NORM: "территория огороднических некоммерческих товариществ"},
    {ORTH: "тер. ДНТ", NORM: "территория дачных некоммерческих товариществ"},
    {ORTH: "тер. СПК", NORM: "территория садоводческих потребительских кооперативов"},
    {ORTH: "тер. ОПК", NORM: "территория огороднических потребительских кооперативов"},
    {ORTH: "тер. ДПК", NORM: "территория дачных потребительских кооперативов"},
    {ORTH: "тер. СНП", NORM: "территория садоводческих некоммерческих партнерств"},
    {ORTH: "тер. ОНП", NORM: "территория огороднических некоммерческих партнерств"},
    {ORTH: "тер. ДНП", NORM: "территория дачных некоммерческих партнерств"},
    {ORTH: "тер. ТСН", NORM: "территория товарищества собственников недвижимости"},
    {ORTH: "тер. ГСК", NORM: "территория гаражно-строительного кооператива"},
    {ORTH: "ус.", NORM: "усадьба"},
    {ORTH: "тер.ф.х.", NORM: "территория фермерского хозяйства"},
    {ORTH: "ю.", NORM: "юрты"},
    {ORTH: "ал.", NORM: "аллея"},
    {ORTH: "б-р", NORM: "бульвар"},
    {ORTH: "взв.", NORM: "взвоз"},
    {ORTH: "взд.", NORM: "въезд"},
    {ORTH: "дор.", NORM: "дорога"},
    {ORTH: "ззд.", NORM: "заезд"},
    {ORTH: "км", NORM: "километр"},
    {ORTH: "к-цо", NORM: "кольцо"},
    {ORTH: "лн.", NORM: "линия"},
    {ORTH: "мгстр.", NORM: "магистраль"},
    {ORTH: "наб.", NORM: "набережная"},
    {ORTH: "пер-д", NORM: "переезд"},
    {ORTH: "пер.", NORM: "переулок"},
    {ORTH: "пл-ка", NORM: "площадка"},
    {ORTH: "пл.", NORM: "площадь"},
    {ORTH: "пр-д", NORM: "проезд"},
    {ORTH: "пр-к", NORM: "просек"},
    {ORTH: "пр-ка", NORM: "просека"},
    {ORTH: "пр-лок", NORM: "проселок"},
    {ORTH: "пр-кт", NORM: "проспект"},
    {ORTH: "проул.", NORM: "проулок"},
    {ORTH: "рзд.", NORM: "разъезд"},
    {ORTH: "ряд", NORM: "ряд(ы)"},
    {ORTH: "с-р", NORM: "сквер"},
    {ORTH: "с-к", NORM: "спуск"},
    {ORTH: "сзд.", NORM: "съезд"},
    {ORTH: "туп.", NORM: "тупик"},
    {ORTH: "ул.", NORM: "улица"},
    {ORTH: "ш.", NORM: "шоссе"},
    {ORTH: "влд.", NORM: "владение"},
    {ORTH: "г-ж", NORM: "гараж"},
    {ORTH: "д.", NORM: "дом"},
    {ORTH: "двлд.", NORM: "домовладение"},
    {ORTH: "зд.", NORM: "здание"},
    {ORTH: "з/у", NORM: "земельный участок"},
    {ORTH: "кв.", NORM: "квартира"},
    {ORTH: "ком.", NORM: "комната"},
    {ORTH: "подв.", NORM: "подвал"},
    {ORTH: "кот.", NORM: "котельная"},
    {ORTH: "п-б", NORM: "погреб"},
    {ORTH: "к.", NORM: "корпус"},
    {ORTH: "ОНС", NORM: "объект незавершенного строительства"},
    {ORTH: "оф.", NORM: "офис"},
    {ORTH: "пав.", NORM: "павильон"},
    {ORTH: "помещ.", NORM: "помещение"},
    {ORTH: "раб.уч.", NORM: "рабочий участок"},
    {ORTH: "скл.", NORM: "склад"},
    {ORTH: "coop.", NORM: "сооружение"},
    {ORTH: "стр.", NORM: "строение"},
    {ORTH: "торг.зал", NORM: "торговый зал"},
    {ORTH: "а/п", NORM: "аэропорт"},
    {ORTH: "им.", NORM: "имени"}
]:
    _exc[abbr[ORTH]] = [abbr]


for abbr in [
    # Others abbreviations
    {ORTH: "тыс.руб.", NORM: "тысяч рублей"},
    {ORTH: "тыс.", NORM: "тысяч"},
    {ORTH: "руб.", NORM: "рубль"},
    {ORTH: "долл.", NORM: "доллар"},
    {ORTH: "прим.", NORM: "примечание"},
    {ORTH: "прим.ред.", NORM: "примечание редакции"},
    {ORTH: "см. также", NORM: "смотри также"},
    {ORTH: "кв.м.", NORM: "квадрантный метр"},
    {ORTH: "м2", NORM: "квадрантный метр"},
    {ORTH: "б/у", NORM: "бывший в употреблении"},
    {ORTH: "сокр.", NORM: "сокращение"},
    {ORTH: "чел.", NORM: "человек"},
    {ORTH: "б.п.", NORM: "базисный пункт"}
]:
    _exc[abbr[ORTH]] = [abbr]


TOKENIZER_EXCEPTIONS = update_exc(BASE_EXCEPTIONS, _exc)
