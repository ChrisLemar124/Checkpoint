import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

class EditorCheckpointing:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Editor con Checkpointing")
        self.root.geometry("600x400")

        #Application State
        self.archivo_actual: Path = Path("checkpoint_temporal.txt")
        self.caracteres_escritos: int = 0
        self.LIMITE_AUTOSAVE: int = 5

        self.configurar_interfaz()
        self.cargar_estado_inicial()

    def configurar_interfaz(self):
        #Barra de herramientas
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(fill=tk.X, padx=5, pady=5)

        tk.Button(frame_botones, text="Nuevo", command=self.nuevo_archivo).pack(side=tk.LEFT, padx=2)
        tk.Button(frame_botones, text="Abrir", command=self.abrir_archivo).pack(side=tk.LEFT, padx=2)
        tk.Button(frame_botones, text="Guardar", command=self.guardar_manual).pack(side=tk.LEFT, padx=2)

        #Area de texto principal
        self.area_texto = tk.Text(self.root, wrap=tk.WORD, font=("Consolas", 12))
        self.area_texto.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        self.area_texto.bind("<KeyRelease>", self.verificar_autosave)

    def cargar_estado_inicial(self):
        if self.archivo_actual.exists():
            try:
                contenido = self.archivo_actual.read_text(encoding="utf-8")
                self.area_texto.insert("1.0", contenido)
                logging.info(f"Estado restaurado desde {self.archivo_actual.name}")
            except Exception as e:
                logging.error(f"Error al cargar checkpoint: {e}")

    def verificar_autosave(self, event):
        #Ignoramos teclas de control para contar solo texto real
        if event.char: 
            self.caracteres_escritos += 1
            
            if self.caracteres_escritos >= self.LIMITE_AUTOSAVE:
                self.guardar_estado(es_autosave=True)
                self.caracteres_escritos = 0 #Reiniciamos el contador

    def guardar_estado(self, es_autosave: bool = False):
        try:
            contenido = self.area_texto.get("1.0", tk.END)
            self.archivo_actual.write_text(contenido, encoding="utf-8")
            
            if es_autosave:
                logging.info(f"Autosave ejecutado en {self.archivo_actual.name}")
        except Exception as e:
            logging.error(f"Fallo al guardar: {e}")

    def guardar_manual(self):
        ruta = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if ruta:
            self.archivo_actual = Path(ruta)
            self.guardar_estado(es_autosave=False)
            logging.info("Guardado exitoso")
            messagebox.showinfo("Éxito", "Archivo guardado correctamente")

    def nuevo_archivo(self):
        self.archivo_actual = Path("checkpoint_temporal.txt")
        self.area_texto.delete("1.0", tk.END)
        self.caracteres_escritos = 0
        logging.info("Nuevo archivo iniciado")

    def abrir_archivo(self):
        ruta = filedialog.askopenfilename(
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if ruta:
            self.archivo_actual = Path(ruta)
            self.area_texto.delete("1.0", tk.END)
            self.cargar_estado_inicial()

if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = EditorCheckpointing(ventana_principal)
    ventana_principal.mainloop()