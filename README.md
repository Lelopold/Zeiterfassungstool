Der bereitgestellte Code implementiert ein Task-Management-System mit einer grafischen Benutzeroberfläche (GUI) unter Verwendung der Bibliothek CustomTkinter. Das System ermöglicht es Benutzern, Aufgaben (Tasks) zu erstellen, zu bearbeiten, zu archivieren und zu verwalten. Darüber hinaus können Benutzer Kategorien erstellen und Aufgaben diesen Kategorien zuordnen. Hier ist eine ausführliche Beschreibung der Hauptfunktionen und Konzepte des Codes:
1. Klassen und Datenstrukturen

    Task-Klasse:
        Diese Klasse repräsentiert eine Aufgabe und enthält Attribute wie name (Name der Aufgabe), description (Beschreibung), category (Kategorie der Aufgabe), time_used (verwendete Zeit in Sekunden) und id (eindeutige ID der Aufgabe). Die Klasse hat auch ein Attribut active, um den Status der Aufgabe zu verfolgen.
    Category-Klasse:
        Diese Klasse repräsentiert eine Kategorie, die Aufgaben gruppiert. Sie enthält Attribute wie name (Name der Kategorie), tasks (Liste der zugehörigen Aufgaben), id (eindeutige ID der Kategorie), active (Status der Kategorie) und active_task_count (Anzahl der aktiven Aufgaben in der Kategorie).

2. TaskManager-Klasse

    Initialisierung:
        Der Konstruktor (__init__) initialisiert die GUI-Komponenten und Datenstrukturen wie category_map (Wörterbuch, das Kategorien nach ihrem Namen speichert), task_map (Wörterbuch, das Aufgaben nach ihrem Namen speichert) und day_data (Wörterbuch, das die Tagesberichte speichert).

    GUI-Methoden:

        home_gui(): Diese Methode erstellt das Hauptfenster der Anwendung und richtet alle GUI-Komponenten wie Buttons, Labels und Scrollbars ein. Sie ruft auch Methoden zum Laden und Aktualisieren der Daten auf.

        disable_buttons() und enable_buttons(): Diese Methoden deaktivieren bzw. aktivieren die Buttons der GUI, um die Interaktion zu steuern, wenn bestimmte Aktionen ausgeführt werden.

        add_category_gui() und add_category(): Diese Methoden zeigen ein Popup-Fenster zum Erstellen einer neuen Kategorie an und fügen dann die neue Kategorie den Datenstrukturen hinzu.

        archive_category_gui() und archive_category(): Diese Methoden zeigen ein Popup-Fenster zum Archivieren einer Kategorie an und aktualisieren den Status der Kategorie sowie ihrer Aufgaben.

        new_task_gui() und add_task(): Diese Methoden zeigen ein Popup-Fenster zum Erstellen einer neuen Aufgabe an und fügen die neue Aufgabe den Datenstrukturen hinzu.

        mark_task_as_done() und delete_task(): Diese Methoden ermöglichen es, eine Aufgabe als erledigt zu markieren oder zu löschen.

        show_details(): Diese Methode zeigt die Details der ausgewählten Aufgabe im Detailbereich der GUI an.

        switch_active_task_gui() und set_active_task(): Diese Methoden ermöglichen das Wechseln der aktiven Aufgabe und das Starten der Zeitverfolgung für die ausgewählte Aufgabe.

        count_time() und pause_running_task(): Diese Methoden implementieren die Zeitverfolgung für die aktive Aufgabe und pausieren sie bei Bedarf.

        daily_report_gui(): Diese Methode zeigt einen Tagesbericht der verwendeten Zeit für alle Aufgaben an.

3. Datenmanagement

    save_tasks() und save_day_data(): Diese Methoden speichern die aktuellen Aufgaben- und Kategoriendaten sowie die Tagesberichte in JSON-Dateien.

    load_and_update(): Diese Methode lädt die gespeicherten Daten aus den JSON-Dateien und aktualisiert die Datenstrukturen und die GUI entsprechend.

4. Tastenkombinationen

    Der Code nutzt die Bibliothek keyboard, um Tastenkombinationen zu registrieren, die bestimmte Aktionen in der Anwendung auslösen, wie das Wechseln der aktiven Aufgabe oder das Ändern der Auswahl in der Liste der Aufgaben.

Zusammenfassung

Der TaskManager ermöglicht eine umfassende Verwaltung von Aufgaben und Kategorien durch eine benutzerfreundliche GUI. Mit Funktionen zum Erstellen, Bearbeiten, Löschen und Archivieren von Aufgaben und Kategorien sowie zur Zeitverfolgung und zum Erstellen von Tagesberichten bietet das System eine breite Palette von Werkzeugen zur effizienten Aufgabenverwaltung. Die Verwendung von JSON-Dateien zur Datenspeicherung stellt sicher, dass die Daten zwischen den Sitzungen erhalten bleiben.
