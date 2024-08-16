Followspot-System

As I made this followspot-system for my "Maturaarbeit", a final highschool project in Switzerland, there is some sort of documentation of my progress needed, which will be done here in German. You can just skip this part and go directly to the actual README at line (START README).

02.06.24 (3h) Erster grosser Fortschritt: OSC auf der GrandMA3 funktioniert, bisher war das nicht der Fall, da ich versucht habe, die OSC Daten auf meinen PC zuhause zu senden, welcher wegen fehlender GrandMA Hardware ein abgeschlossenes Netzwerk hat und deshalb Daten nicht senden oder empfangen lässt. Die Daten wurden zum Testen jetzt über TouchOSC gesendet, da die Konfiguration über diese Software einfacher ist. Den Input habe ich bisher nur auf dem System-Monitor der MA Software gesehen, jedoch hat noch nichts sonst auf der Konsole darauf reagiert. Wahrscheinlich liegt das daran, dass die gesendeten Befehle nicht stimmen.

10.06.24 (1h) Die Befehle wurden nun so abgeändert, dass sie die Konsole auch steuern können und so auch die Lichter angeschaltet werden. Die Dokumentation zu OSC über GrandMA ist nicht sehr ausführlich, weshalb ich noch herausfinden muss, wie:

Man direkte Befehle an die Konsole geben kann, statt nur die "executors" (Faders, Encoders, Buttons) bewegen zu können,
Die Fixture Attributes, die ich kontrollieren will(Pan, Tilt, Zoom), kontrolliert werden können.

11.06.24 (1.5h) Nach Herumstöbern in Internet-Foren und durchlesen der sehr vielen verschiedenen Befehle auf der GrandMA Software habe ich nun den Weg gefunden, um die gewünschten Attribute direkt ohne Faders anzusteuern. Der nächste Schritt wäre, mithilfe des Flightsticks in Python Input zu erhalten und die Lichter kontrollieren zu können. (Ein erster Code-Snippet ist hochgeladen, um zu sehen wie die Bibliothek funktioniert).

17.07.24 Nun kann der Code mithilfe der Pyglet Bibliothek (für Spieleentwicklung) die Movers auch wirklich bewegen. Dazu habe ich jetzt ein simples Interface geschaffen, in welchem man die Bewegung der Movers mithilfe eines bewegenden Rechtecks sehen kann (nur relativ, ohne wirklichen Massstab). Dazu wird der absolute Pan/Tilt Wert oben links numerisch angezeigt.

Zusätzlich erkennt es jetzt die Kollision des Joystick Rechtecks und einer "Fixture" (Licht, auf dem Bildschirm ebenfalls durch ein Rechteck grafisch dargestellt). Dadurch wird man in Zukunft zuerst eine spezifische Fixture auswählen können um sie dann zu kontrollieren. Ebenfalls kann man nun die Anzahl Fixtures angeben und sie werden auf dem Bildschirm der Reihe nach angereiht mit dem Mittelpunkt in der Mitte des Fensters.

20.07.24 Das Followspot-System hat jetzt noch ein paar zusätzliche Features erhalten. Neben kleineren Verbesserungen im Skalieren der HUD Elemente mit der Fenstergrösse kann man nun noch zusätzlich die "intensity" (Lichtstärke) und den "zoom" (Lichtwinkel) mithilfe einer "throttle" ansteuern, die beim Kauf des Flightstick-HOTAS mitgeliefert wurde.

Ebenfalls kann man noch mit einer Achse am Flightstick die Sensitivität der Bewegung einstellen, um sowohl schnelle Bewegungen als auch präzise Korrekturen zu ermöglichen.

Dazu wurde der gesendete Befehl an die Konsole so abgeändert, dass die Befehle, die 60 mal pro Sekunde in die Konsole reinfliessen, sie nicht vollständig Sperren und jegliche Bedienung der Konsole verhindern. Man kann jetzt sogar die gewünschte Fixture über die Konsole auswählen und dann nahtlos ihre Parameter über die Joysticks kontrollieren, wodurch bessere Zusammenarbeit zwischen den zwei LDs (Light Designers) ermöglicht wird.

11.08.24 Dem System wurde nun noch die Möglichkeit gegeben, mit der Betätigung eines Knopfes zwischen dem "Show", "No_Output" und "Edit" Modus zu wechseln. Der Show Modus ist das schon vorhandene System ohne grosse Abänderung. Im No_Ouput Modus werden keine Befehle an die Konsole gesendet, wodurch man die Konsole ohne Störung verwenden kann. Der Edit Modus wird in der Zukunft als Editierfunktion dienen, damit man neue Fixtures im System definieren und ihre Position ändern kann.

Zusätzlich wurde eine Warnung hinzugefügt, wenn das Licht seine maximale Umdrehung erreicht hat und sich nicht mehr weiter in die vorgegebene Richtung bewegen kann. Zudem wird im Interface die Pan/Tilt Anzeige kontinuierlich rot, wenn eine der Werte in die Nähe dieser Grenze kommt.

Ebenfalls gibt es jetzt Funktionen, welche vom Kartesischen in das Sphärische oder vom Sphärischen in das Kartesische Koordinatensystem umwandeln. Beim jetzigen Stand kann man vom Kartesischen in das Sphärische Koordinatensystem nur die Kartesischen Werte eingeben, welche dann umgewandelt werden. In der Zukunft sollte dies jedoch fliessend mit der Bedienung des Joysticks funktionieren sollen.

16.08.24 Die Transformation funktioniert nun auch noch fliessend mit dem Joystick. Die Position des Lichtes wird auch auf dem Interface grafisch angezeigt und zusätzlich auch die X und Y Werte (je von 0-100, mit 0,0 als unten links auf der Bühne und 100,100 als oben rechts).
Für die Anzeige auf dem Interface brauchte es noch zusätzlich eine Funktion, welche den Joystick Input auf dem Interface in die nicht intuitiven, scheinbar zufälligen kartesischen Koordinaten umwandelt, um diese dann nachher in das sphärische Koordinatensystem(pan/tilt) zu transformieren.

Somit funktioniert dieses System vollständig und der praktische Teil der MA ist fertig. Der Fokus wird nun auf den schriftlichen Kommentar gelegt.
