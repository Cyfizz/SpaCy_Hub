import pytest


def test_noun_chunks_is_parsed_nl(nl_tokenizer):
    """Test that noun_chunks raises Value Error for 'nl' language if Doc is not parsed."""
    # fmt: off
    txt = "We zijn vandaag de hele dag geweest. Dan denk ik dus dat was, zeg ik wist niet winkels. Wat. Je. Ja. Jullie gingen toch deurtjes zoeken. Ja, dat dachten. Ja, ja, ja, dat is. Uiteindelijk hebben we nu. Is het eigenlijk niet alleen een nieuwe keuken kopen. Kun je kun je kun je niet deurtjes kopen of kan dat niet. Jawel, jawel, ja, dat is een dus die met de keuken zijn vanmorgen die ze met de zaak geweest. Dus we hebben nu wie alleen een vervolgafspraak, maar dat die ja alles is mogelijk, alles en ook deze deurtjes die we hebben. We kunnen ook nog kastjes bijkopen kleuren, die zijn er nog die, die worden nog gemaakt. Die kastjes dus. Maar waarom zou je dat niet doen? Hoor. Nou, het punt, het punt is dat? Ja het het past eigenlijk niet zo mooi die en die keuken die is gemaakt voor in zo'n in zo'n zij keuken, zo'n, lange smalle keuken en als je daar een woonkeuken in gemaakt. Wij wilden we eigenlijk een beetje je gewoon. Helemaal rond zijn. Ja, maar wat gezelliger maken, want hij is nu een beetje heel zo zwartwit en en dan dan moet je eigenlijk dat dat blad of zo op één of andere manier doormidden zagen dan een stuk tussen maken. Daar in ieder geval ja is een beetje veranderd. Te? Maken. Ja, het is allemaal op maat gemaakt en dat maar je kunt, je kan je ook niet meer verkopen. Ja, dat kan wel ouders met een vriendje van joh, die hebben hun keuken verkocht hebben net een nieuwe keuken. Maar ja, wat wat handig is, we waren, dat was één van de laatste winkels en toen kwamen er eigenlijk pas achter dat bij een een zaak. Dan kun je gewoon dan in de keuken en niet de apparatuur. En bij die apparatuur hebben we al is dat dat. Inderdaad niet hebben. Ja, ja, dat is gewoon perfect, ja, het liefst het blad, dat vinden we ook mooi, dat is een heel duur en en voor de rest ja, die kastjes die daar gaat het ons eigenlijk en en dan kun je je eigenlijk voor voor voor. Nou ja, zeg maar tussen de nou, maar tussen de drie en en en en en 8000 gulden kun je gewoon de hele wereld kopen. Zeg maar dan heb je echt alles, dan heb je en als je bereid bent om 8000 gulden uit te geven, dan heb je gewoon hartstikke mooie keuken. Maar voor alleen kastjes of. Ja, dan heb je een zonder apparatuur dan ja, zonder apparatuur nodig hebt. Geen voor nodig, maar dat is wel een hoop geld voor alleen kastjes. Hè is dat. Voor de keuken gezien van 60000 gulden en dan. 30000 je hebt toch duidelijk. Ja, maar daar zit een bij, daar zit een afwasmachine, zit een fornuis in alles, inbouw magnetron, ah, opgehaald. Dat scheelt ja. Toen heb ik gezegd. Keuken was 60000 gulden zes nee, 40 soort. Vind je het na 40000 gulden. Dat was maar dat was een inclusief de plaatsing en het verlaagd plafond spotjes. Wat is nou moesten dan om te doen? Is dat het laten plaatsen of is dat de apparatuur. Plaatsen is iets van dus 500 of 2000 gulden, maar die kastjes zijn heel duur. Wij hadden vandaag hebben gekeken naar andere panelen voor deurtjes. Het deurtje is 600 gulden, één deurtje van elkaar zien. Wat is daar voor bijzonders aan? Een deurtje van zn. Of ik weet niet hoe het met andere dingen, maar die deurtjes die wij hebben, die, daar kun je dus gewoon. Daar kan een kind met de fiets tegen haar rijden en die zijn zijn knoerthard. En dan kun je op schrijven. En dan kun je je hebben. Het is echt, dan wordt het niet vies, doet overheen, en die hebben gewoon en en in dat blad. We hebben dat blad van ons, dat keukenblad 6000 gulden. Dat is een speciaal soort kunststof van DuPont, dus dat koriander en dat super hygiënisch is echt super dicht lijkt een beetje op gaan, niet open, maar je kunt je kunt het ook in granito krijgen, dus gewoon een ja soort vulstoffen en maar het is zo mooi. We hadden mijn schoonmoeder eens een keer pan opgezet. Koeman dus, en die die zaagt dus gewoon een rond gat erin. Mmm. Ik neem de een stuk van dat spul mee, dus als een stuk uit. Dat leidt iedereen vast en schuurt het glad je niks meer van van zo'n boetseerklei. Ja, het is echt fantastisch dag bezig bent met de keuken ontruimen, afgeplakt, maar als ie weggaat dan dan zie je dus niks meer. Dat is geweldig. En je weet wel zeker dat ie niet intussen gewoon ergens een heel nieuwsblad vandaan nadenken. Van heel mooi spul, ja, en dan al die apparatuur is lekker. Ja. Nou. Het goeie pad. Dan moeten we die kerstboom nog. Ja. Het is een beetje overdreven, geloof ik, nou is morgen driekoningen. Vandaag komt er een is. Er is er een Utrechtse, nooit een grote kerstboomverbranding om een hele lange woorden. Ik ben is nog moeilijk kerstboomverbranding, verbrandingsovens. Het zijn allemaal sterretje n woorden. Wordt is in Utrecht. Maar bewaren. Hadden we in Eindhoven altijd keer per was een? Ik weet nog heel goed, gingen we altijd heen. Met mijn vader kerstboomverbranding. Een enorme fik werkte gigantisch groot kerstbomen s ochtends. Mmm. Eigenlijk moet je op toen dat betreft ja, maar dat was echt groot jongeren lager dan gewoon 10000 kerstbomen op. Het is wel leuk, ja, heel vaak een half jaar nog langs de kant van de straat staan of ergens op een balkonnetje boven of zo allang ontdaan van mijn. Is een tijd geleden toen toen werden van illegale vuurtjes gestookt doen vinden? Jongens, dat weet ik dat een inzamelingsactie hebben gedaan en dan krijg je dus vijf gulden of een cd bon van 50 gulden. Elke boom die eh soms heel effectief. De gemeente is al die jongens, die kun je allemaal bomen wel aan mogelijk wel meenemen, maar dat is niet meer. Ik vind het ook nogal wat vijf gulden. Mmm. Dat tikt echt aan. Maar dan moet je zo bomen met stekels moet je dan misschien weet ik veel hoeveel kilometer dat je interviews toen bij die post daar af kan geven. Dan weet je wel even zoeken.\n"
    doc = nl_tokenizer(txt)
    with pytest.raises(ValueError):
        list(doc.noun_chunks)
