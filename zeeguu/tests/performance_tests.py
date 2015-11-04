# coding=utf-8
__author__ = 'mircea'

# We need this even before the zeeguu_testcase import
# so we are sure to setup the right db for pefromance testing
import os
os.environ["ZEEGUU_PERFORMANCE_TESTING"] = "True"

import zeeguu_testcase
# Always must be imported first
# it sets the test DB

from zeeguu.model import User
import zeeguu
import json
import time

class Performance_Tests(zeeguu_testcase.ZeeguuTestCase):

    texts = [dict(content="Zuerst gab VW Manipulationen beim Schadstoffausstoss zu, jetzt ist klar, dass der Konzern auch Kohlendioxidwerte falsch angegeben hat. Inwiefern unterscheiden sich die beiden Fälle? Die Schadstoffe sind gesundheitsschädlich, Forscher in den USA haben denn auch errechnet, dass statistisch gesehen 60 Amerikaner zehn bis zwanzig Jahre früher sterben werden, weil sie die durch VW höher belastete Luft atmen mussten. Kohlendioxid schadet zwar nicht der Gesundheit, aber dem Klima. Deshalb haben die Umweltbehörden in der EU Zielwerte vorgegeben, wie viel CO2 neue Autos pro Kilometer ausstossen dürfen. Diese Zielwerte gelten auch für die Schweiz. Sind die neuen CO2-Manipulationen eine Überraschung? Studien zeigen, dass es beim Verbrauch und folglich beim CO2 teils grosse Unterschiede bei Test- und Realwerten gibt. Gemäss der Nonprofitorganisation International Council on Clean Transportation (ICCT) lagen 2013 die realen Verbrauchswerte eines Autos im Schnitt 38 Prozent über den Werten, welche Autohersteller angeben. Konsumentenorganisationen, etwa in Italien, haben deshalb sogar schon mit einer Klage gegen VW und Fiat gedroht. Insofern sind Experten nicht überrascht, dass VW auch bei CO2- und Verbrauchswerten zu tiefe Angaben gemacht hat. Wie gross ist das Ausmass des neuen Skandals? Laut VW sind von den Unregelmässigkeiten bei den Angaben zu CO2 und Verbrauch 800'000 Autos betroffen, darunter auch Benziner. Zum Vergleich: Im Fall des Abgasbetrugs sind weltweit 11 Millionen Fahrzeuge von der Manipulation betroffen, in der Schweiz über 128'000. Ob im CO2-Fall ebenfalls Autos in der Schweiz betroffen sind, ist gemäss VW-Importeur Amag immer noch unklar. Was bedeutet der Fall für Besitzer von VW-Marken? Im Zuge des Abgasskandals sollen die betroffenen VW-Modelle nachgerüstet werden. Die betroffenen Autobesitzer in der Schweiz werden dazu direkt von der Amag informiert. Unklar ist, wie VW beim CO2-Fall vorgehen wird und ob eine Anpassung des Fahrzeuges überhaupt möglich ist. Der Schweizer Importeur Amag sagt dazu: «Volkswagen (VW 118.95 -4.15%) setzt alles daran, nach Absprache mit den zuständigen Behörden schnellstmöglich eine Klärung der weiteren Vorgehensweise sowie eine korrekte Einstufung der CO2-Werte bei den betroffenen Fahrzeugen vorzunehmen.» Können Autofahrer die Hersteller auf Schadenersatz belangen, wenn die Herstellerangaben zu Verbrauch und CO2 nicht eingehalten werden? Die Hersteller für die Unterschiede zwischen Test- und den realen Werten zu belangen, ist in der Schweiz fast aussichtslos. Hersteller stellen sich auf den Standpunkt, dass der tatsächliche Verbrauch eine Autos von unzähligen Faktoren abhängt: Wetter, Verkehrsverhältnissen, Strassenzustand oder individueller Fahrweise. In Deutschland sieht die Rechtslage anders aus. Bessere Aussichten werden Schweizer Autobesitzer haben, wenn es sich um falsche Angaben des Herstellers handelt. Experten erwarten deshalb im Zusammenhang mit dem neuen CO2-Skandal bei VW zahlreiche Schadenersatzklagen. Können die geltenden CO2-Zielwerte angesichts der gefälschten Angaben überhaupt eingehalten werden? Aktuell dürfen Neuwagen in der EU und in der Schweiz maximal 130 Gramm CO2 pro Kilometer ausstossen. Bis 2020 soll der Wert auf 95 Gramm sinken. Da noch unklar ist, um wie viel der CO2-Wert bei VW zu tief angegeben wurde, ist es schwierig zu sagen, ob die Zielwerte erreicht werden können oder nicht. Wie werden die Behörden mit den Falschangaben umgehen? Für das Bundesamt für Energie sind die Angaben wichtig, weil es aufgrund dieser Zahlen Sanktionszahlungen für die nicht eingehaltenen CO2-Zielwerte von Autoimporteuren erhebt. 2014 mussten die Markenvertreter 1,7 Millionen Franken Strafe bezahlen. Für 2015 werden die Strafzahlungen in der Autobranche auf einen zweistelligen Millionenbetrag geschätzt, weil in diesem Jahr zum ersten Mal hundert Prozent der Neuwagen den Grenzwert erreichen müssen. Ob die Strafzahlungen wegen der Falschangaben nun höher ausfallen werden, klärt das Bundesamt für Energie nach eigenen Angaben derzeit ab: «Sobald konkrete Informationen zu den betroffenen Fahrzeugen und Modellen sowie korrigierte CO2-Werte vorliegen, werden die Sanktionsberechnungen mithilfe der korrigierten CO2-Werte erneut durchgeführt werden. Danach kann festgelegt werden, ob der entsprechende Importeur zu zusätzlichen Sanktionszahlungen verpflichtet ist», sagt Sprecherin Angela Brunner. Was bedeutet die Ausweitung des Skandals für den VW-Konzern? Gemäss dem deutschen Autoprofessor Ferdinand Dudenhöffer ist der neue Skandal für VW und dessen Image noch viel schlimmer. «Die Tests zur Messung von CO2-Werten sind heute sehr moderat, wenn dann noch falsche Angaben gemacht werden, ist das schon sehr dramatisch», sagt Dudenhöffer zu DerBund.ch/Newsnet. Er sieht die Lage für den Konzern sehr pessimistisch. «VW mit der aktuellen Aufstellung wird kaum aus der Krise finden.» Weil Bundesländer und Gewerkschaften einen grossen Einfluss hätten, seien beispielsweise Kostensenkungen durch einen Stellenabbau oder Lohnkosteneinsparungen nicht möglich. «Deshalb kann auch die Rentabilität der Kernmarke VW nicht erzielt werden», so Dudenhöffer, «oder offenbar nur mit illegalen Mitteln.»", id=10445659),
             dict(content="VW hat wegen manipulierter Abgaswerte Riesenärger in den USA. Aber das ist nicht das einzige Problem. Nun kündigt der deutsche Autobauer eine Rückrufaktion wegen möglicher Mängel an Bremsen an. Der Wolfsburger Konzern beordert auf dem US-Markt 91'800 Fahrzeuge wegen eines Defekts an der Nockenwelle in die Werkstätten zurück. Betroffen von dem freiwilligen Rückruf seien unter anderem Benziner vom Typ Jetta, Passat, Beetle und Golf der Modelljahre 2015 und 2016, wie die US-Tochter von VW am Mittwoch mitteilte. Der Autobauer steht bereits wegen der Affäre um manipulierte Abgaswerte bei Diesel-Fahrzeugen stark unter Druck. Der Defekt an der Nockenwelle kann den Angaben zufolge zu einer Schwächung der Bremsen führen, was das Unfallrisiko erhöhe. Ein Unternehmenssprecher wollte nicht mitteilen, ob es bereits Zwischenfälle gegeben hat, sagte aber, es gebe keine Berichte über Verletzten in dem Zusammenhang. Der Mangel soll bis Ende März behoben sein. Bis dahin rät VW den Besitzern, ihre Wagen einfach weiter zu nutzen. Falls ein Warnlämpchen anginge, sollten sie zur Werkstatt fahren, hiess es. Weitere Benziner betroffen Das Unternehmen habe die US-Verkehrssicherheitsbehörde NHTSA über die Rückrufaktion informiert. Nach Informationen des «Wall Street Journal» wies Volkswagen (VW 118.95 -4.15%) ausserdem seine Händler in den USA an, die Verkäufe bestimmter Fahrzeuge mit Benzinmotoren der Modelljahre 2015 und 2016 zu stoppen, bis eine Lösung des Problems gefunden worden sei. Der US-Zeitung zufolge fielen Volkswagen die Mängel an der Nockenwelle bereits im Februar auf. Nach mehreren Tests habe sich das Unternehmen im Oktober zu einem Rückruf entschieden. Volkswagen suche noch immer nach der Ursache des Problems, berichtete das «Wall Street Journal» unter Berufung auf eine Mitteilung von VW an die NHTSA. Das Unternehmen werde seine Kunden im Dezember über die Reparaturen informieren, die sich bis Ende März hinziehen könnten. Auch in Kanada würden Fahrzeuge wegen des Defekts in die Werkstätten gerufen. Aus Deutschland kommt derweil die Nachricht, dass neben den gestern bekannt gewordenen 800'000 Benzin-Fahrzeugen weitere 98'000 Benziner vom Abgas-Skandal betroffen sind. Das berichtet die Nachrichtenagentur AFP.", id=24861902),
             dict(content="Das Bankgeheimnis in der Schweiz wird nicht gelockert. Der Bundesrat hat am Mittwoch beschlossen, vorerst auf die geplante Revision des Steuerstrafrechts zu verzichten. Er begründet dies mit den geringen Erfolgschancen für das Projekt. Umfrage Das Bankgeheimnis im Inland wird nicht aufgehoben. Das ist ... richtig falsch Abstimmen Mit der Reform wollte der Bundesrat erreichen, dass sich Steuerhinterzieher nicht länger hinter dem Bankgeheimnis verstecken können. Steuerämter sollten bei konkretem Verdacht auf Steuerhinterziehung von Banken Auskunft verlangen können. Kein Schutz für Steuerhinterzieher Damit wäre die Unterscheidung zwischen Steuerhinterziehung und -betrug bezüglich der Untersuchungsmittel weggefallen. Hintergrund war nicht zuletzt die Kritik der Kantone, die sich nach dem Ende des Bankgeheimnisses für ausländische Kunden gegenüber ausländischen Steuerbehörden benachteiligt fühlen. Für die meisten Bürgerinnen und Bürger würde sich nichts ändern, betonte Finanzministerin Eveline Widmer-Schlumpf bei der Präsentation der Vorschläge. Das Bankgeheimnis sollte aber kein Schutz für Steuerhinterzieher sein. Bürgerliche Parteien dagegen Während die Linke die Vorschläge als Schritt in die richtige Richtung begrüssten, sahen die bürgerlichen Parteien und die Wirtschaftsverbände darin einen Angriff auf das Bankgeheimnis. Das bewährte Vertrauensverhältnis zwischen Bürger und Staat würde zerstört, monierten sie. Der Bundesrat krebste in der Folge zurück und beauftragte das Finanzdepartement, die Vorlage abzuschwächen: Die kantonalen Steuerbehörden sollten bei Verdacht auf Steuerhinterziehung nur dann Bankdaten einsehen dürfen, wenn es sich um schwere Fälle handelt und wenn ein Gericht oder eine andere Instanz sie dazu ermächtigt hat. Keine neue Definition Festhalten wollte der Bundesrat indes am Plan, Steuerbetrug neu zu definieren. Heute liegt dann Steuerbetrug vor, wenn zwecks Steuerhinterziehung falsche oder gefälschte Urkunden verwendet werden, etwa ein manipulierter Lohnausweis. Künftig sollte Steuerbetrug nicht mehr ein eigenständiger Straftatbestand sein, sondern eine qualifizierte Form der Steuerhinterziehung. Jede Form der arglistig begangenen Steuerhinterziehung sollte künftig als Steuerbetrug gelten. Nun verzichtet der Bundesrat gänzlich auf die Reform, wie das Finanzdepartement (EFD) mitteilte. Stattdessen wolle er die derzeit sistierte Reform der Verrechnungssteuer vorantreiben. Eine Expertenkommission soll entsprechende Reformvorschläge entwickeln.", id=31140028),
             dict(content="Man muss sich das einmal vorstellen: Der letzte Bundesrat aus dem Kanton Baselland, der letzte Vertreter dieses nicht unwichtigen Kantons in der Landesregierung – er kämpfte noch in der Schlacht von Gettysburg. Amerika war in Nord- und Südstaaten gespalten, und Emil Frey, ein arbeitsloser Studienabbrecher, sass anschliessend eineinhalb Jahre in einem Kerker der Konföderierten. Er kehrte 1865 als Kriegsheld in die Schweiz zurück, 1890 wurde er Bundesrat. Der Mann, der Freys Nachfolger werden will, heisst Thomas de Courten. Von den mehr als zehn Bewerbern, die von den SVP-Kantonalparteien nominiert worden sind, ist de Courten der grosse Unbekannte. Niemand hat den Nationalrat mit dem leicht näselnden Baseldeutsch auf der Rechnung – und genau das macht ihn für seine parteiinternen Konkurrenten so gefährlich. Schon oft wurde de Courten unterschätzt, auch in seiner eigenen SVP. Schon oft hat er überrascht. Der Pharmalobbyist Wie Emil Frey hat auch de Courten einen Bezug zu Amerika, den er selbst hergestellt hat – doch der ist ziemlich weit hergeholt. «Der mit dem Kennedy-Effekt» stand auf den gigantischen Plakaten, mit denen de Courten vor einigen Jahren für seine Wahl in das Baselbieter Kantonsparlament warb. Den Spruch hatte ihm einst eine Zeitung als Anspielung auf sein Aussehen zugedacht - de Courten übernahm die Zuschreibung nur zu gerne. Dass seine politische Schnittmenge mit der Ikone der amerikanischen Demokraten gering ist, steht allerdings ausser Zweifel. In Bern ist der Ökonom, der in Basel und St. Gallen studierte, nach vier Jahren keine politische Grösse. In der Sozial- und Gesundheitskommission, in der er sitzt, fiel er vor allem als konsequenter Lobbyist der Pharmabranche auf. Auch seine ersten beiden Vorstösse im Nationalrat behandelten den Pharmastandort, weitere kamen dazu. De Courten ist Präsident der Intergenerika, dem Verband der Generikahersteller, und führt auch den Verband der schweizerischen Speditions- und Logistikunternehmen (Spedlogswiss). Daneben sitzt er in verschiedenen Verwaltungsräten von regionalen Firmen. Umstrittene Bilanz als Wirtschaftsförderer Noch immer bezeichnet ihn die Website der Parlamentsdienste (und fast jede Zeitung) als Leiter der Baselbieter Wirtschaftsförderung, aber diese Stelle verliess er bereits im vergangenen Juli. «Baselland verliert Wirtschaftsförderer», titelte die «Basler Zeitung», als de Courten seinen Rücktritt bekannt gab. Es klang nach einem Verlust – doch viele im Baselbiet empfanden das anders. In seinen drei Jahren im Amt gelang es dem Kanton kaum, neue Unternehmen anzulocken. Immer wieder stand de Courten in der Kritik aus Wirtschaft und Politik: Wie könne ein SVP-Politiker, der die Masseneinwanderungsinitiative befürworte, gleichzeitig als staatlich besoldeter Wirtschaftsförderer tätig sein? Die Stelle erhalten hatte de Courten, nachdem ihn die Kantonsregierung eilig und ohne formelle Ausschreibung darauf berufen hatte – für viele überraschend. Nicht mit de Courten gerechnet hatte kurz zuvor auch SVP-Nationalrat Christian Miesch. Es war sein Sitz, den de Courten bei den Wahlen 2011 eroberte. Wie Miesch, der nur dank des Rücktritts von Caspar Baader noch einmal in den Nationalrat nachrücken durfte, lebt auch de Courten im oberen, bäuerlich geprägten Teil des Kantons. Die Leutseligkeit der Landschäftler geht ihm aber ab. Im öffentlichen Auftritt wirkt de Courten spröde und etwas roboterhaft. Kennedy ist das nicht. Im Bundesparlament hat de Courten Sympathien, weil er – auch mit seinen Vorstössen – für die Themen des «bürgerlichen Schulterschlusses» steht: Deregulierungen, Bürokratieabbau, Stärkung des Wirtschaftsstandorts. In der SVP-Fraktion ist sein Gewicht allerdings gering. Und nicht einmal in seinem Kanton mag man sich über seine Kandidatur richtig freuen. Es wäre wichtig, dass die Region Basel endlich wieder einmal einen Bundesrat hätte, sagt die Baselbieter CVP-Nationalrätin Elisabeth Schneider-Schneiter. «Aber es sollte jemand sein, der die ganze Region vertritt. Ich bin mir auch gar nicht sicher, ob Thomas de Courten dieses Amt überhaupt will.» «Ich habe grossen Rückhalt» Doch, er wolle – sagt er selbst. Die Aufgabe sei riesig, die Verantwortung auch. «Aber ich habe in der Region und in meiner Kantonalpartei einen grossen Rückhalt. Und bei den Wahlen war ich der bestgewählte bürgerliche Nationalrat.» Seine Bilanz als kantonaler Wirtschaftsförderer sei besser, als sie oft dargestellt werde, und im Parlament sei er inzwischen angekommen. Dass er sich für die Pharma einsetze, sei nur logisch: «Die Life Sciences sind die Leitbranche unserer Region.» Trotzdem weiss de Courten: «Ich bin in diesen Wahlen eher in der Rolle des Aussenseiters.» Schon oft sei es allerdings bei Bundesratswahlen zu Überraschungen gekommen. «Warum nicht auch diesmal?» Auf einer seiner alten Kaffeetassen stand einst ein Satz von Friedrich Nietzsche: «Die Zeit für kleine Politik ist vorbei. Schon das nächste Jahrhundert bringt den Kampf um die Erdherrschaft.» Der Kampf des Thomas de Courten: Er beginnt zuerst einmal in der SVP-Fraktion.", id=23743517),
             dict(content="In den Ohren vieler FDP-Mitglieder klang das Szenario für die Stadtwahlen im nächsten Jahr düster: Gemeinderätin Ursula Wyss (SP) werde von ihrem Vorgänger «Wyss-gewaschen» und gleichsam ins Stadtpräsidium katapultiert. Und Rot-grün werde drei oder gar vier Sitze im Gemeinderat erobern. «Doch es könnte durchaus anders kommen», sagte Parteipräsident Philippe Müller diese Woche an der Mitgliederversammlung der FDP Stadt Bern. Dies sei dann der Fall, wenn sich die Grüne Freie Liste (GFL) von Rot-Grün-Mitte (RGM) löse und Alec von Graffenried als Kandidaten fürs Stadtpräsidium präsentiere. «Ich wünsche Alec von Graffenried ein Quentchen mehr Mut», sagte Müller. Am Tag danach gibt sich der Präsident nicht minder entschlossen: Klar, es sei «speziell», wenn der FDP-Präsident einen Grünen zur Kandidatur fürs Berner Stadtpräsidium auffordere. «Aber die im Stadtrat vorherrschende Polpolitik muss ein Ende haben.» Und dafür sei der gemässigte Grüne von Graffenried nun einmal geeigneter als die «ideologisch politisierende» SP-Gemeinderätin Wyss. Teuscher werde «zurückstecken» Müller ist überzeugt, dass eine Kandidatur von Graffenrieds für den Erlacherhof eine breite Unterstützung erhalten würde. «Die Chancen von Graffenrieds wären intakt.» Dies insbesondere deshalb, weil Franziska Teuscher (GB) ihre Ambitionen fürs Stadtpräsidium zugunsten von Wyss werde zurückstecken müssen, um das rot-grüne Bündnis nicht zu gefährden. SVP schadet «bürgerlicher Sache» Eine Kandidatur von Graffenrieds fürs Stadtpräsidium hätte allerdings nur dann eine reelle Chancen, wenn SVP, FDP und CVP auf eine eigene Kandidatur für den Erlacherhof verzichten würden. Und wenn die SVP vom bereits angekündigten Alleingang bei den Gemeinderatswahlen wieder absehe und gemeinsam mit der FDP eine Liste bildete. Denn die FDP erzielte bei den Nationalratswahlen bloss einen Wähleranteil von knapp unter zehn Prozent – zuwenig für ein Gemeindratsmandat. «Bezüglich der bereits mehrfach angekündigten SVP-Liste für die Gemeinderatswahlen ist das letzte Wort noch nicht gesprochen», sagt Müller. Ein Alleingang der SVP schade der bürgerlichen Sache, weil dadurch Schmidt gefährdet würde. Zudem wären die SVP-Spitzenkandidaten Erich Hess oder Thomas Fuchs bei einer Wahl in die Stadtregierung «völlig isoliert». Die SVP Stadt Bern solle sich ein Beispiel nehmen an der FDP-Kantonalpartei, sagte Müller in der Rede vor der Mitgliederversammlung. Diese verzichte bei der Regierungsratsersatzwahl auf eine eigene Kandidatur, um die bürgerliche Wende in der Kantonsregierung zu ermöglichen. Nause? – «Hat keine Chance» Ein Knackpunkt bleibt allerdings die Frage, ob die amtierenden Gemeinderäte Alexandre Schmidt (FDP) und Reto Nause (CVP) auf eine eigene Stadtpräsidiumskandidatur verzichten würden. Die Wähler seien nicht dumm und merkten, ob eine solche Kandidatur eine reelle Chance habe oder nicht, sagt Müller. Zumindest was Nause betrifft, ist er sich sicher: «Er hat keine Chance.» Zu Schmidts Chancen möchte sich Müller nicht äussern. Ein Verzicht Schmidts auf eine eigene Stadtpräsidiumskandidatur sei die «mögliche Konsequenz» einer Kandidatur von Graffenrieds. In einem ersten Wahlgang werde es vielleicht mehrere Kandidaten geben. «In einem zweiten Wahlgang fürs Stadtpräsidium müssten sich aber alle auf von Graffenried einigen», sagt Müller.", id=30143442),
             dict(content="Noch fahren sie nur zu Testzwecken, dereinst sollen selbstfahrende Autos im Strassenverkehr aber die Norm sein. An dieser Zukunftsvision arbeiten derzeit gleich mehrere Firmen und Forschungsinstitute. Google soll mit seinen Roboterautos bereits über eine Million Kilometer auf US-Strassen zurückgelegt haben; Volvo kurvte mit seinem selbstfahrenden Auto schon mehrere Male durch Göteborg, und die Swisscom fährt seit diesem Frühling mit dem Zukunftsauto der Freien Universität Berlin durch Zürich. Doch längst beschäftigen sich nicht mehr nur Ingenieure, Informatiker und Juristen mit unserer automobilen Zukunft. So wirft die neue Technik nämlich auch ethische Fragen auf, an denen sich Philosophen abmühen. Konkret geht es darum, wie weit der Computer am Steuer gehen darf, um seine Passagiere zu schützen. Was zählt im Extremfall mehr: das Leben des Insassen oder dasjenige eines Fussgängers? Fetter Mann auf der Brücke Ein Forschungsteam um den Psychologen Jean-François Bonnefon veröffentlichte ein Paper zu diesem Thema. Das Team der Toulouse School of Economics hatte 900 Probanden eine Reihe von Unfallszenarien vorgelegt. Die Probanden mussten jeweils entscheiden, ob das selbstfahrende Auto einen Passanten überfahren sollte, um den Insassen zu retten, oder umgekehrt. Das Resultat der Studie: 75 Prozent der Befragten waren der Meinung, dass Auto solle ein Ausweichmanöver vollziehen, welches gleichbedeutend war mit dem Tod des Passagiers – selbst wenn damit das Leben eines einzelnen Fussgängers gerettet wurde. Diese Art der Fragestellung ist keine unbekannte, greift sie doch das Trolley-Problem der britischen Philosophin Philippa Foot auf. In Foots Gedankenexperiment fährt ein Tram auf eine Gruppe von fünf Menschen zu. Die Probanden müssen nun entscheiden, ob sie das Leben der fünf retten, indem sie eingrefen, eine Weiche stellen und das Tram auf ein Gleis lenken, auf welchem jedoch eine Person vom Wagen überfahren wird. Sie übernehmen so aber eine Mitschuld. Das Experiment wurde später um das sogenannte Fetter-Mann-Problem erweitert. Dieses sieht vor, dass Probanden auf einer Brücke über den Tramgleisen stehen, neben ihnen ein dicker Mann. Das Gewicht dieses Mannes wäre hoch genug, um den Tramwagen zu stoppen. Ist es nun moralisch vertretbar, den Mann von der Brücke zu stossen, um fünf Menschen auf den Tramgleisen zu retten? Wer einsteigt, geht Risiko ein Soll ein fahrerloses Auto nun also einen unschuldigen Fussgänger überfahren, um mehrere Insassen zu retten? Für Helen Frowe von der Universität Stockholm greift dieser utilitaristische Ansatz zu kurz, wonach das beste Ergebnis für möglichst viele Menschen erreicht werden soll. Frowe ist der Meinung, dass die moralische Verantwortung des Individuums in die Gleichung aufgenommen werden muss. Gegenüber dem Wirtschaftsmagazin «Quartz» sagt sie, selbstfahrende Autos müssten so programmiert werden, dass sie stets den Fussgänger schützten: «Denn der Passagier entschied sich, in ein Roboterauto zu steigen, also trägt er das höhere Risiko und die moralische Verantwortung.» Das Töten eines Passanten ist laut Frowe selbst dann nicht moralisch vertretbar, wenn mehrere Erwachsene oder Kinder im Auto sitzen. Doch: Gibt es eine Zahl von Autopassagieren, die das Töten eines einzelnen Fussgängers plötzlich doch legitimiert? Für Helen Frowe gibt es eine solche; sie verortet diese bei einer vagen «Busladung» von Menschen. Einige von Frowes Ethikkollegen werden das anders sehen, denn die Philosophie ist sich bezüglich dieses moralischen Dilemmas längst nicht einig. Aber den Kopf darüber zerbrechen werden sich auch die Softwareingenieure. Am Schluss des Tages werden sie die selbstfahrenden Autos programmieren.", id=14734484),
             dict(content="Das Zwangsmassnahmengericht des Kantons Bern hat zurecht eine rückwirkende Randdatenerhebung für das Handy eines 15-Jährigen nicht zugelassen. Dies hat das Bundesgericht im Rahmen einer öffentlichen Beratung entschieden. Es hat damit eine Lockerung bei der Überwachung von Personen abgelehnt. Die Erhebung der Randdaten - also wann der Junge wo war und mit wem er kommuniziert hat - war ein Vorschlag von dessen Eltern. Diese mussten im Rahmen einer Untersuchung gegen einen Polizisten aussagen. Der Polizist soll ihr Kind bei einer Hausdurchsuchung mit der Faust und der flachen Hand geschlagen haben. Weil der Junge jedoch zwei Tage vor der Hausdurchsuchung mit dem Velo gestürzt war und an der Hand operiert werden musste, ist unklar, ob die festgestellten Verletzungen im Gesicht allenfalls vom Sturz herrührten. Auch die behandelnden Ärzte verneinten dies. Um belegen zu können, wo der Junge sich in den beiden Tagen vor und am Tag der Hausdurchsuchung befand, brachten die Eltern die Randdatenerhebung ins Spiel. Damit wollte die Staatsanwaltschaft die Aussagen der Zeugen überprüfen. Gemäss dem Gerichtsschreiber des Bundesgerichts in diesem Fall geht aus den Akten klar hervor, dass Eltern und Junge dazu einwilligten. Eine offizielle schriftliche Erklärung wurde jedoch erst nach dem negativen Entscheid des Zwangsmassnahmengerichts eingereicht. Die Staatsanwaltshaft legte Beschwerde ein. Knappe Entscheidung Die Beschwerde ist in der öffentlichen Sitzung mit drei zu zwei Stimmen abgelehnt worden. Die Mehrheit der beratenden Richter ist der Ansicht, dass die Randdatenerhebung nicht auf beliebige Personen ausgedehnt werden darf. Sie stelle einen nicht vernachlässigbaren Grundrechtseingriff dar und müsse deshalb vorsichtig eingesetzt werden. In diesem Fall haben die Handydaten des Jungen keine direkte Verbindung zum Beschuldigten oder zum mutmasslichen Delikt. Die Minderheit der Richter sieht keine Notwendigkeit für den Link zwischen Straftat beziehungsweise Beschuldigtem und der überwachten Person. Auch führt sie ins Feld, dass die entsprechenden Gesetzesartikel, welche die Überwachung regeln, ausdrücklich unter dem Titel «Geheime Überwachungsmassnahmen» laufen. Es handle sich vorliegend aber nicht um eine geheime Überwachung.", id=12504490),
             dict(content="An der Vorstandssitzung sei vor allem darüber diskutiert worden, ob die Berner Sektion einen Vorschlag machen solle, da doch bereits eine Bernerin und ein Berner im Bundesrat sitzen. Das sagte die Geschäftsführerin der SVP Kanton Bern, Aliki Panayides, nach der Sitzung auf Anfrage. Der Vorstand habe sich schliesslich zugunsten eines Vorschlags an die Findungskommission entschieden, weil sie der Meinung sei, die SVP-Bundeshausfraktion solle zwischen mehreren Kandidaten auswählen können. Zudem sei Albert Rösti ein guter Kandidat. Die SVP-Fraktion entscheidet schliesslich, wer für die SVP bei den Bundesratswahlen antritt. Eine Rolle gespielt habe bei den Überlegungen auch, so Panayides weiter, dass die bernische SVP die zweitgrösste Kantonalsektion sei und neun Nationalräte stelle. Deshalb finde es die bernische SVP angemessen, jemanden zu melden. Rösti ist laut Panayides auch bereit, Bundesrat zu werden. Abgesagt haben hingegen drei andere bekannte Berner SVP-Vertreterinnen und -Vertreter in Bundesbern, welche von der Spitze der bernischen SVP kontaktiert wurden: Die Nationalräte Adrian Amstutz, Nadja Pieren und Andreas Aebi. Bisher zwei Meldungen aus Kantonen Abgesehen von der Berner Sektion haben bisher zwei Kantonalsektionen der SVP-Findungskommission Personalvorschläge unterbreitet. Es sind dies die SVP des Kantons Aargau - sie empfiehlt Nationalrat Hansjörg Knecht - und die SVP des Kantons Schaffhausen. Diese entschied am Montagabend, Ständerat Hannes Germann und Nationalrat Thumas Hurter der Findungskommission zu melden. Im Kanton Waadt dürfte am 11. November Nationalrat Guy Parmelin zuhanden der Findungskommission nominiert werden. Ebenfalls im Gespräch als möglicher Bundesratskandidat ist der Bündner Nationalrat Heinz Brand. Die SVP Schweiz lässt den Kantonalsektionen bis zum 13. November Zeit, ihre Kandidaten offiziell vorzuschlagen.", id=20176000),
             dict(content="Das Augenmittel Ala Octa, das im Verdacht steht, bei mehreren Patienten in Spanien und Frankreich zu einer Erblindung geführt zu haben, ist auch in der Schweiz vertrieben worden. In einem Westschweizer Spital wurde ein kritischer Fall entdeckt. Die Schweizer Arzneimittelbehörde Swissmedic erwäge deshalb, noch am Mittwoch einen Anwendungsstopp auszusprechen, sagte Swissmedic-Sprecher Peter Balzli gegenüber der Nachrichtenagentur SDA. Die Abteilung Marktüberwachung stehe in Kontakt mit dem deutschen Produzenten Alamedics. «Die Möglichkeit, dass ein Qualitätsproblem besteht, ist sehr hoch», sagte Balzli. Vorfälle in Spanien und Frankreich Das Augenmittel Ala Octa wird vor allem bei Netzhaut-Operationen verwendet. In Nordspanien waren nach dessen Anwendung nach Angaben der dortigen Gesundheitsbehörde im Juni insgesamt 13 Menschen auf einem Auge erblindet. In Frankreich gab es im Juli zwei Fälle, wie die französische Nachrichtenagentur AFP unter Berufung auf die nationale Medikamentenbehörde (ANSM) berichtete. Allerdings machte die ANSM nicht direkt Ala Octa für die Erblindungen verantwortlich. Auch in Italien gab es einen verdächtigen Fall. «Keine Verunreinigung» Der deutsche Hersteller teilte Anfang Woche mit, es sei verfrüht, sein Mittel für die tragischen Vorfälle verantwortlich zu machen. Analysen unabhängiger Labore hätten ergeben, dass es keinen Hinweis auf eine Verunreinigung oder sonstige Auffälligkeiten gegeben habe, sagte der Geschäftsführer der Alamedics GmbH mit Sitz in Dornstadt (Baden-Württemberg), Christian Lingenfelder, am Dienstag. Möglicherweise habe es Fehler bei der Anwendung des Mittels gegeben, hiess es bei Alamedics weiter. Dem Unternehmen sei mindestens ein Fall aus Spanien bekannt, in dem das Produkt eine Woche lang im Auge belassen worden sei und nicht nach der Operation sofort wieder entfernt wurde. «Sollten Reste im Auge verbleiben, kann dies zu Entzündungsreaktionen führen.» Alamedics hatte nach den Vorfällen im Sommer einen Rückruf des Mittels gestartet und das Produkt vom Markt genommen. Wie viele Einheiten des Medikaments im Umlauf sind und in welchen Ländern sie vertrieben wurden, teilte das Unternehmen nicht mit.", id=14490796),
             dict(content="Bei dem französischen Rechtsextremisten Jean-Marie Le Pen hat es wegen des Verdachts der Steuerhinterziehung eine Hausdurchsuchung gegeben. Das Haus des Gründers des rechtsextremen Front National (FN) im Grossraum Paris wurde am Mittwoch auf Anordnung der Justiz durchsucht, wie die Nachrichtenagentur AFP aus Justizkreisen erfuhr. Gegen den langjährigen FN-Vorsitzenden, der kürzlich mit der inzwischen von seiner Tochter Marine geführten Partei gebrochen hatte, laufen seit Juni Ermittlungen wegen des Verdachts der Steuerhinterziehung und Geldwäscherei. Ende April hatte die investigative Onlinezeitschrift «Mediapart» enthüllt, dass die Anti-Geldwäsche-Abteilung des Finanzministeriums (Tracfin) wegen eines Trusts auf den britischen Jungferninseln ermittelt, der von Genf aus verwaltet wurde und auf den persönlichen Assistenten von Le Pen lief. Demnach enthielt er 2,2 Millionen Euro, davon 1,7 Millionen in Gold. Nach Angaben aus Justizkreisen wurde das Konto 2014 geschlossen und das Geld auf eine Bank auf den Bahamas überwiesen. Le Pen bestreitet, an einem Trust im Ausland beteiligt zu sein.", id=28445042)]

    # We must override the super implementation, which
    # repopulates the DB
    def setUp(self):
        self.app = zeeguu.app.test_client()
        zeeguu.app.test_request_context().push()
        self.session = self.get_session()

    def test_user_bookmarks(self):
        user = User.find("i@mir.lu")
        assert user.all_bookmarks() > 100


    def test_text_difficulty(self):
        data = json.dumps(dict(
            texts=self.texts,
            personalized='true',
            method='median'))

        start = time.clock()
        rv = self.api_get('/get_difficulty_for_text/de', data, 'application/json')
        end = time.clock()

        difficulties = json.loads(rv.data)
        for difficulty in difficulties:
            assert 0.0 <= difficulty['score'] <= 1.0

        print str(end - start) + ' seconds'


    def test_text_learnability(self):
        data = json.dumps(dict(texts=self.texts))

        start = time.clock()
        rv = self.api_get('/get_learnability_for_text/de', data, 'application/json')
        end = time.clock()

        learnabilities = json.loads(rv.data)
        for learnability in learnabilities:
            assert 0.0 <= learnability['score'] <= 1.0

        print str(end - start) + ' seconds'
