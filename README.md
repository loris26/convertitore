# convertitore
Una semplice app per windows in grado di convertire velocemente i file tiff o tif all'interno di una cartella in formato png, JPEG, BMP, GIF
# Scarica il file compilato "Convertitore da TIF a PNG.exe" per eseguire il file

# Convertitore di Immagini TIFF (Solo Windows)

Questo script Python, realizzato con Tkinter, offre un'interfaccia utente intuitiva per convertire immagini TIFF in altri formati di immagine comuni come PNG, JPEG, JPG, BMP e GIF.  È progettato specificamente per funzionare su sistemi operativi Windows. Permette agli utenti di selezionare una cartella di input contenente file TIFF, scegliere un formato di output e specificare una cartella di output per le immagini convertite.

**Importante:** Questo programma è testato e progettato per funzionare solo su Windows. Non è garantito il suo funzionamento su macOS o Linux.

## Caratteristiche

*   **GUI intuitiva (Windows):** Interfaccia grafica intuitiva costruita con Tkinter per una facile navigazione.
*   **Formati di output multipli:** Supporta la conversione in formati PNG, JPEG, JPG, BMP e GIF.
*   **Barra di avanzamento:** Visualizza una barra di avanzamento durante il processo di conversione per indicare lo stato di completamento.
*   **Gestione degli errori:** Gestione robusta degli errori con messaggi informativi per guidare l'utente.
*   **Selezione cartelle:** Consente agli utenti di selezionare facilmente le cartelle di input e output utilizzando una finestra di dialogo di selezione file.
*   **Creazione cartella di output:** Permette agli utenti di creare una nuova cartella di output direttamente dall'applicazione.
*   **Logging:** Fornisce un logging dettagliato dei processi di conversione e dei potenziali errori.
*   **Creazione eseguibile (PyInstaller):** Progettato per funzionare senza problemi quando viene impacchettato come eseguibile utilizzando PyInstaller.
*   **Conversione in thread separato:** Esegue la conversione delle immagini in un thread separato per evitare il blocco dell'interfaccia grafica.

## Requisiti

*   Windows (Testato e progettato per Windows)
*   Python 3.x
*   Libreria Pillow (PIL) (`pip install Pillow`)
*   Tkinter (solitamente incluso con Python)

## Installazione

1.  **Clona il repository:**

    ```bash
    git clone [URL del repository]
    cd [directory del repository]
    ```

2.  **Installa le dipendenze:**

    ```bash
    pip install Pillow
    ```

## Utilizzo

1.  **Esegui lo script:**

    ```bash
    python main.py
    ```

2.  **Interfaccia grafica:**

    *   **Schermata di benvenuto:** Fornisce una breve introduzione all'applicazione.
    *   **Schermata di selezione:**
        *   Clicca "Seleziona Cartella Input" per scegliere la cartella contenente i tuoi file TIFF.
        *   Seleziona il formato di output desiderato dal menu a tendina.
    *   **Schermata di output:**
        *   Clicca "Seleziona Cartella Esistente" per scegliere una cartella esistente per le immagini convertite.
        *   Clicca "Crea Nuova Cartella" per creare una nuova cartella per le immagini convertite.
    *   **Schermata di conversione:** Visualizza una barra di avanzamento mentre le immagini vengono convertite.
    *   **Schermata dei risultati:** Indica se la conversione è avvenuta con successo e ti permette di aprire la cartella di output.



## Struttura delle directory

*   `main.py`: Lo script Python principale.
*   `data/icon.ico`: (Opzionale) File icona per l'eseguibile. Crea questa directory se intendi creare un file `.exe`.

## Spiegazione del codice

*   `resource_path(relative_path)`: Questa funzione gestisce il percorso delle risorse (come l'icona) in modo diverso a seconda che lo script venga eseguito come script o come eseguibile in bundle con PyInstaller.
*   `converti_tiff_in_png(cartella_input, cartella_output, formato_output, progress_callback)`: Questa funzione esegue la conversione effettiva delle immagini utilizzando la libreria Pillow. Itera sui file TIFF nella cartella di input, li converte nel formato di output specificato e li salva nella cartella di output. Include anche la gestione degli errori e aggiorna la barra di avanzamento.
*   `ImageConverterApp`: Questa classe definisce l'applicazione Tkinter e gestisce gli elementi della GUI.

## Gestione degli errori

Lo script include la gestione degli errori per le seguenti situazioni:

*   Cartella di input non valida.
*   Cartella di output non valida.
*   Nessun file TIFF trovato nella cartella di input.
*   Errori durante la conversione dell'immagine.
*   Errore di file non trovato.
*   Errore di immagine non identificata.

## Logging

Lo script utilizza il modulo `logging` per registrare informazioni importanti sul processo di conversione. I log vengono scritti nella console.

## Contributi

I contributi sono benvenuti! Invia pull request con correzioni di bug, nuove funzionalità o miglioramenti alla documentazione.

## Licenza

[Specifica la tua licenza qui, ad esempio, Licenza MIT]

## Autore

[Il tuo nome/organizzazione]
