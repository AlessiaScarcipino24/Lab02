import csv

def carica_da_file(filename):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    album = {}
    try:
        with open(filename,'r',encoding="utf-8") as file:
            reader = csv.DictReader(file, fieldnames=['codice', 'titolo', 'autore', 'mese', 'anno'])
            next(reader,None)
            for record in reader:
                codice = record['codice']
                titolo = record['titolo']
                autore = record['autore']
                mese = int(record['mese'])
                anno = int(record['anno'])

                if anno not in album:
                    album[anno] = []
                album[anno].append((codice,titolo,autore,mese))

    except FileNotFoundError:
        return None

    return album


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""

    # Verifichiamo la validità del mese
    if not(1 <= mese <= 12):
        return None
    # Verifichiamo che il codice non sia già presente all'interno dell'album
    for fotoLista in album.values():
        for foto in fotoLista:
            if foto[0] == codice:
                return None

    try:
        # Apriamo il file in modalità 'a' (append/aggiungi in coda)
        with open(file,'a', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([codice,titolo,autore,mese,anno])
    except FileNotFoundError:
        return None

    if anno not in album: # aggiorna la struttura dati in memoria
        album[anno] = []
    album[anno].append((codice, titolo, autore, mese))

    retrun (codice,titolo,autore,mese,anno) # restituiamo il riferimento alla foto (inclusiva di anno)


def cerca_foto(album, codice_richiesto):
    """Cerca una foto nell'album dato il codice"""
    for anno, listaFoto in album.items():
        for foto in listaFoto:
            if foto[0] == codice_richiesto: # restituisce una tupla con tutti i dati
                return f'{foto[0]}, {foto[1]}, {foto[2]}, {foto[3]}, {anno}'

    return None


def elenco_foto_anno_per_titolo(album, anno_richiesto):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    if anno_richiesto in album:
        # ordina la lista di tuple basandosi sul titolo (indice 1)
        fotoOrdinate = sorted(album[anno_richiesto], key=lambda x: x[1])
        return [foto[1] for foto in fotoOrdinate]  # Parentesi quadre per creare una lista
    else:
        return None


def main():
    album = {}
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione: ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
