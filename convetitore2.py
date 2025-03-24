import os
import sys
from PIL import Image
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import logging
import subprocess
import threading

# Configura il logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def resource_path(relative_path):
    """Ottiene il percorso assoluto di una risorsa, funziona sia in sviluppo che in PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def converti_tiff_in_png(cartella_input, cartella_output, formato_output, progress_callback):
    """Converte i file TIFF nel formato specificato e aggiorna la barra di progresso."""
    formato_output = formato_output.upper()  # Converti in maiuscolo per PIL

    # Crea la cartella di output se non esiste
    if not os.path.exists(cartella_output):
        try:
            os.makedirs(cartella_output)
            logging.info(f"Creata cartella di output: {cartella_output}")
        except OSError as e:
            logging.error(f"Impossibile creare la cartella di output: {e}")
            return False, str(e)  # Indica fallimento e restituisce l'errore

    # Conta i file TIFF
    tiff_files = [f for f in os.listdir(
        cartella_input) if f.lower().endswith((".tiff", ".tif"))]
    num_files = len(tiff_files)
    if num_files == 0:
        return False, "Nessun file TIFF trovato nella cartella di input."

    # Itera sui file e converti
    successi = 0  # Conta le conversioni riuscite
    for i, filename in enumerate(tiff_files):
        filepath = os.path.join(cartella_input, filename)
        try:
            img = Image.open(filepath)
            nome_file_senza_estensione = os.path.splitext(filename)[0]
            nome_file_output = nome_file_senza_estensione + "." + formato_output.lower()
            filepath_output = os.path.join(cartella_output, nome_file_output)

            img.save(filepath_output, formato_output)
            logging.info(f"Convertito: {filename} -> {nome_file_output}")
            successi += 1
        except FileNotFoundError:
            logging.error(f"File non trovato: {filepath}")
        except Image.UnidentifiedImageError:
            logging.error(
                f"Impossibile identificare il formato immagine di: {filename}")
        except Exception as e:
            logging.error(f"Errore durante la conversione di {filename}: {e}")
            return False, str(e)

        # Aggiorna la barra di progresso
        progress = int((i + 1) / num_files * 100)
        progress_callback(progress)

    if successi == 0:
        return False, "Nessun file convertito correttamente."

    return True, None  # Indica successo


def apri_cartella(path):
    """Apre la cartella specificata."""
    try:
        os.startfile(path)
        logging.info(f"Aperta la cartella: {path}")
    except Exception as e:
        logging.error(f"Impossibile aprire la cartella: {e}")


class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Convertitore Immagini TIFF")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        try:
            icon_path = resource_path("data/icon.ico")
            self.root.iconbitmap(icon_path)
        except:
            logging.warning("Icona non trovata.")

        self.current_frame = None  # Frame corrente
        self.cartella_input = None
        self.formato_output = "PNG"
        self.cartella_output = None
        self.create_welcome_frame()

    def clear_frame(self):
        """Distrugge il frame corrente."""
        if self.current_frame:
            self.current_frame.destroy()

    def create_welcome_frame(self):
        """Crea il frame di benvenuto."""
        self.clear_frame()
        self.current_frame = ttk.Frame(self.root, padding=20)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        label = ttk.Label(self.current_frame, text="Converti le tue immagini da TIFF ad un altro formato!",
                          font=("Arial", 16), wraplength=500, justify="center")
        label.pack(pady=50)

        avanti_button = ttk.Button(
            self.current_frame, text="Avanti", command=self.create_selection_frame)
        avanti_button.pack(pady=20)

        self.create_lorisoftware_label()

    def create_selection_frame(self):
        """Crea il frame di selezione cartella e formato."""
        self.clear_frame()
        self.current_frame = ttk.Frame(self.root, padding=20)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        # Seleziona cartella input
        input_label = ttk.Label(
            self.current_frame, text="Seleziona la cartella contenente i file TIFF da convertire:", wraplength=400, justify="left")
        input_label.pack(pady=(0, 5), anchor=tk.W)
        input_button = ttk.Button(
            self.current_frame, text="Seleziona Cartella Input", command=self.seleziona_cartella_input)
        input_button.pack(pady=(0, 20), anchor=tk.W)

        # Seleziona formato output
        output_label = ttk.Label(
            self.current_frame, text="Seleziona il formato di output:", wraplength=400, justify="left")
        output_label.pack(pady=(0, 5), anchor=tk.W)
        self.formato_combo = ttk.Combobox(self.current_frame, values=[
                                          "PNG", "JPEG", "JPG", "BMP", "GIF"], state="readonly")
        self.formato_combo.set("PNG")  # Valore predefinito
        self.formato_combo.pack(pady=(0, 20), anchor=tk.W)
        self.formato_combo.bind("<<ComboboxSelected>>",
                                self.aggiorna_formato_output)

        avanti_button = ttk.Button(
            self.current_frame, text="Avanti", command=self.create_output_frame)
        avanti_button.pack(pady=20)

        self.create_lorisoftware_label()

    def seleziona_cartella_input(self):
        """Apre la finestra di dialogo per selezionare la cartella di input."""
        self.cartella_input = filedialog.askdirectory(
            title="Seleziona la cartella di input")

    def aggiorna_formato_output(self, event=None):
        """Aggiorna il formato di output in base alla selezione della combobox."""
        self.formato_output = self.formato_combo.get()

    def create_output_frame(self):
        """Crea il frame per selezionare/creare la cartella di output."""
        if not self.cartella_input:
            messagebox.showerror(
                "Errore", "Seleziona prima la cartella di input!")
            return

        self.clear_frame()
        self.current_frame = ttk.Frame(self.root, padding=20)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        output_label = ttk.Label(
            self.current_frame, text="Seleziona o crea la cartella dove salvare le immagini convertite:", wraplength=400, justify="left")
        output_label.pack(pady=(0, 5), anchor=tk.W)

        esistente_button = ttk.Button(
            self.current_frame, text="Seleziona Cartella Esistente", command=self.seleziona_cartella_esistente)
        esistente_button.pack(pady=(0, 10), anchor=tk.W)

        nuova_button = ttk.Button(
            self.current_frame, text="Crea Nuova Cartella", command=self.crea_nuova_cartella)
        nuova_button.pack(pady=(0, 20), anchor=tk.W)

        avanti_button = ttk.Button(
            self.current_frame, text="Avvia Conversione", command=self.create_conversion_frame)
        avanti_button.pack(pady=20)

        self.create_lorisoftware_label()

    def seleziona_cartella_esistente(self):
        """Apre la finestra di dialogo per selezionare una cartella esistente."""
        self.cartella_output = filedialog.askdirectory(
            title="Seleziona la cartella di output")

    def crea_nuova_cartella(self):
        """Apre la finestra di dialogo per creare una nuova cartella."""
        cartella_base = filedialog.askdirectory(
            title="Seleziona dove creare la cartella")
        if cartella_base:
            nome_cartella = tk.simpledialog.askstring(
                "Nome Cartella", "Inserisci il nome della nuova cartella:")
            if nome_cartella:
                self.cartella_output = os.path.join(
                    cartella_base, nome_cartella)
            else:
                messagebox.showerror("Errore", "Nome cartella non valido.")
                self.cartella_output = None
        else:
            self.cartella_output = None

    def create_conversion_frame(self):
        """Crea il frame per visualizzare la fase di conversione."""
        if not self.cartella_output:
            messagebox.showerror(
                "Errore", "Seleziona o crea prima la cartella di output!")
            return

        self.clear_frame()
        self.current_frame = ttk.Frame(self.root, padding=20)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        self.progress_label = ttk.Label(
            self.current_frame, text="Conversione in corso...", font=("Arial", 12))
        self.progress_label.pack(pady=(0, 5))

        self.progress_bar = ttk.Progressbar(
            self.current_frame, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=(0, 20))

        self.conversione_thread = threading.Thread(
            target=self.avvia_conversione)
        self.conversione_thread.start()

        self.create_lorisoftware_label()

    def avvia_conversione(self):
        """Avvia la conversione in un thread separato."""
        successo, messaggio = converti_tiff_in_png(
            self.cartella_input, self.cartella_output, self.formato_output, self.aggiorna_barra_progresso)
        self.root.after(0, self.mostra_risultato_conversione,
                        successo, messaggio)

    def aggiorna_barra_progresso(self, progress):
        """Aggiorna la barra di progresso."""
        self.progress_bar["value"] = progress

    def mostra_risultato_conversione(self, successo, messaggio):
        """Mostra il risultato della conversione e offre di aprire la cartella."""
        self.clear_frame()
        self.current_frame = ttk.Frame(self.root, padding=20)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        if successo:
            risultato_label = ttk.Label(
                self.current_frame, text="Conversione avvenuta con successo!", font=("Arial", 14))
        else:
            risultato_label = ttk.Label(self.current_frame, text=f"Conversione fallita: {messaggio}", font=(
                "Arial", 14), wraplength=500, justify="center")
        risultato_label.pack(pady=20)

        apri_button = None  # Definisci apri_button al di fuori del blocco if
        if successo:  # Mostra il pulsante solo se la conversione ha avuto successo
            apri_button = ttk.Button(
                self.current_frame, text="Apri Cartella Output", command=self.apri_cartella_output)
            apri_button.pack(pady=10)

        fine_button = ttk.Button(
            self.current_frame, text="Torna alla schermata iniziale", command=self.create_welcome_frame)
        fine_button.pack(pady=10)

        self.create_lorisoftware_label()

    def apri_cartella_output(self):
        """Apre la cartella di output."""
        apri_cartella(self.cartella_output)

    def create_lorisoftware_label(self):
        """Crea l'etichetta Lorisoftware in basso."""
        lorisoftware_label = ttk.Label(
            self.current_frame, text="LoriSoftware", font=("Arial", 8), foreground="gray")
        lorisoftware_label.pack(side=tk.BOTTOM, anchor=tk.S, pady=(0, 5))


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()
