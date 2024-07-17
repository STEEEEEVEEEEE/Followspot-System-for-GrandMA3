Followspot-System

As I made this followspot-system for my "Maturaarbeit", a final highschool project in Switzerland, there is some sort of documentation of my progress needed, which will be done here in German. You can just skip this part and go directly to the actual README at line (START README).

02.06.24 (3h) Erster grosser Fortschritt: OSC auf der GrandMA3 funktioniert, bisher war das nicht der Fall, da ich versucht habe, die OSC Daten auf meinen PC zuhause zu senden, welcher wegen fehlender GrandMA Hardware ein abgeschlossenes Netzwerk hat und deshalb Daten nicht senden oder empfangen lässt. Die Daten wurden zum Testen jetzt über TouchOSC gesendet, da die Konfiguration über diese Software einfacher ist. Den Input habe ich bisher nur auf dem System-Monitor der MA Software gesehen, jedoch hat noch nichts sonst auf der Konsole darauf reagiert. Wahrscheinlich liegt das daran, dass die gesendeten Befehle nicht stimmen.

10.06.24 (1h) Die Befehle wurden nun so abgeändert, dass sie die Konsole auch steuern können und so auch die Lichter angeschaltet werden. Die Dokumentation zu OSC über GrandMA ist nicht sehr ausführlich, weshalb ich noch herausfinden muss, wie:

Man direkte Befehle an die Konsole geben kann, statt nur die "executors" (Faders, Encoders, Buttons) bewegen zu können,
Die Fixture Attributes, die ich kontrollieren will(Pan, Tilt, Zoom), kontrolliert werden können.

11.06.24 (1.5h) Nach Herumstöbern in Internet-Foren und durchlesen der sehr vielen verschiedenen Befehle auf der GrandMA Software habe ich nun den Weg gefunden, um die gewünschten Attribute direkt ohne Faders anzusteuern. Der nächste Schritt wäre, mithilfe des Flightsticks in Python Input zu erhalten und die Lichter kontrollieren zu können. (Ein erster Code-Snippet ist hochgeladen, um zu sehen wie die Bibliothek funktioniert).


17.07.24 Nun kann der Code mithilfe der Pyglet Bibliothek (für Spieleentwicklung) die Movers auch wirklich bewegen. Dazu habe ich jetzt ein simples Interface geschaffen, in welchem man die Bewegung der Movers mithilfe eines bewegenden Rechtecks sehen kann (nur relativ, ohne wirklichen Massstab). Dazu wird der absolute Pan/Tilt Wert oben links numerisch angezeigt.
