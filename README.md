# Editor de Texto con Checkpointing

Aplicación de escritorio desarrollada en Python utilizando `tkinter`. Permite crear, abrir y guardar archivos de texto, además de realizar guardados automáticos mediante un sistema de **checkpointing**.

## Características

* Crear archivos nuevos.
* Abrir archivos `.txt`.
* Guardar archivos manualmente.
* Guardar automáticamente el estado del editor.
* Recuperar el último checkpoint al iniciar.
* Registrar eventos y errores mediante `logging`.

## Tecnologías utilizadas

* **Python**
* **Tkinter** — creación de la interfaz gráfica.
* **Pathlib** — manejo de rutas y archivos.
* **Logging** — registro de eventos y errores.

---

## 1. Importación de módulos

```python
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import logging
```

`tkinter` se utiliza para la interfaz gráfica, `filedialog` para seleccionar archivos, `messagebox` para mostrar mensajes, `Path` para trabajar con rutas y `logging` para registrar eventos.

La configuración del registro se realiza con:

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)
```

---

## 2. Clase principal

La aplicación se encuentra dentro de la clase:

```python
class EditorCheckpointing:
```

Su constructor configura la ventana y define el estado inicial:

```python
def __init__(self, root: tk.Tk):
    self.root = root
    self.root.title("Editor con Checkpointing")
    self.root.geometry("600x400")

    self.archivo_actual: Path = Path("checkpoint_temporal.txt")
    self.caracteres_escritos: int = 0
    self.LIMITE_AUTOSAVE: int = 5

    self.configurar_interfaz()
    self.cargar_estado_inicial()
```

`archivo_actual` representa el archivo utilizado actualmente, `caracteres_escritos` lleva el conteo para el autosave y `LIMITE_AUTOSAVE` establece cada cuántos caracteres se guarda el estado.

---

## 3. Interfaz gráfica

La función `configurar_interfaz` crea los botones y el área de texto:

```python
def configurar_interfaz(self):
    frame_botones = tk.Frame(self.root)
    frame_botones.pack(fill=tk.X, padx=5, pady=5)

    tk.Button(
        frame_botones,
        text="Nuevo",
        command=self.nuevo_archivo
    ).pack(side=tk.LEFT, padx=2)

    tk.Button(
        frame_botones,
        text="Abrir",
        command=self.abrir_archivo
    ).pack(side=tk.LEFT, padx=2)

    tk.Button(
        frame_botones,
        text="Guardar",
        command=self.guardar_manual
    ).pack(side=tk.LEFT, padx=2)
```

El área principal utiliza `tk.Text`:

```python
self.area_texto = tk.Text(
    self.root,
    wrap=tk.WORD,
    font=("Consolas", 12)
)
self.area_texto.pack(
    expand=True,
    fill=tk.BOTH,
    padx=5,
    pady=5
)
```

También se registra el evento de liberación de una tecla:

```python
self.area_texto.bind(
    "<KeyRelease>",
    self.verificar_autosave
)
```

Esto permite detectar la escritura del usuario.

---

## 4. Restauración del checkpoint

Al iniciar, el programa comprueba si existe el archivo temporal:

```python
if self.archivo_actual.exists():
```

Si existe, se lee su contenido:

```python
contenido = self.archivo_actual.read_text(
    encoding="utf-8"
)
self.area_texto.insert("1.0", contenido)
```

De esta forma, el contenido almacenado anteriormente puede recuperarse al iniciar la aplicación.

Los errores durante la lectura se registran mediante:

```python
except Exception as e:
    logging.error(f"Error al cargar checkpoint: {e}")
```

---

## 5. Guardado automático

El autosave se controla mediante `verificar_autosave`:

```python
def verificar_autosave(self, event):
    if event.char:
        self.caracteres_escritos += 1

        if self.caracteres_escritos >= self.LIMITE_AUTOSAVE:
            self.guardar_estado(es_autosave=True)
            self.caracteres_escritos = 0
```

Cada carácter detectado incrementa el contador. Cuando alcanza el límite establecido:

```python
self.LIMITE_AUTOSAVE = 5
```

se ejecuta `guardar_estado` y posteriormente se reinicia el contador.

---

## 6. Guardado del estado

La función que almacena el contenido es:

```python
def guardar_estado(self, es_autosave: bool = False):
    try:
        contenido = self.area_texto.get("1.0", tk.END)
        self.archivo_actual.write_text(
            contenido,
            encoding="utf-8"
        )

        if es_autosave:
            logging.info(
                f"Autosave ejecutado en {self.archivo_actual.name}"
            )
    except Exception as e:
        logging.error(f"Fallo al guardar: {e}")
```

Primero obtiene el contenido del editor y después lo escribe en `archivo_actual`.

El parámetro `es_autosave` permite distinguir entre un guardado automático y otros tipos de guardado.

---

## 7. Guardado manual

El botón `Guardar` utiliza un cuadro de diálogo:

```python
ruta = filedialog.asksaveasfilename(
    defaultextension=".txt",
    filetypes=[
        ("Archivos de texto", "*.txt"),
        ("Todos los archivos", "*.*")
    ]
)
```

Cuando el usuario selecciona una ruta, esta se convierte en un objeto `Path` y se guarda el contenido:

```python
if ruta:
    self.archivo_actual = Path(ruta)
    self.guardar_estado(es_autosave=False)
```

Finalmente se muestra un mensaje de confirmación:

```python
messagebox.showinfo(
    "Éxito",
    "Archivo guardado correctamente"
)
```

---

## 8. Crear y abrir archivos

Para crear un archivo nuevo se limpia el editor y se reinicia el estado:

```python
def nuevo_archivo(self):
    self.archivo_actual = Path("checkpoint_temporal.txt")
    self.area_texto.delete("1.0", tk.END)
    self.caracteres_escritos = 0
```

Para abrir un archivo existente se utiliza:

```python
ruta = filedialog.askopenfilename(
    filetypes=[
        ("Archivos de texto", "*.txt"),
        ("Todos los archivos", "*.*")
    ]
)
```

Después se establece la ruta seleccionada y se carga su contenido.

---

## 9. Ejecución del programa

El punto de entrada se encuentra al final:

```python
if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = EditorCheckpointing(ventana_principal)
    ventana_principal.mainloop()
```

Se crea la ventana principal, se inicializa la clase `EditorCheckpointing` y finalmente `mainloop` mantiene activa la interfaz gráfica y permite responder a los eventos del usuario.

---

# Resultados

### Interfaz de la aplicación

<img width="607" height="427" alt="image" src="https://github.com/user-attachments/assets/cfa39ef3-455c-4a26-9165-44c693b3d0c6" />

### Prueba de restauración del checkpoint

Aquí se muestra como se guarda en un archivo temporal lo que el usuario escribe cada 5 caracteres.
<img width="680" height="95" alt="image" src="https://github.com/user-attachments/assets/d881f583-9989-4213-bae0-a41c761d0537" />

# Conclusión

El programa implementa un editor de texto básico con una interfaz gráfica y un mecanismo de checkpointing. El estado del editor se guarda periódicamente y puede recuperarse posteriormente mediante el archivo temporal.

El proyecto integra manejo de archivos, eventos de teclado, interfaz gráfica y registro de eventos mediante `logging`.
