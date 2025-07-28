# secure-password-manager

🔐 Gestor de contraseñas con GUI y cifrado en Python.

## ¿Qué hace?

- Genera contraseñas seguras con opciones personalizadas
- Guarda las contraseñas cifradas en una base de datos SQLite
- Muestra las contraseñas almacenadas en una ventana
- Tiene una interfaz gráfica minimalista hecha con `tkinter`

## Tecnologías utilizadas

- Python 🐍
- `tkinter` (interfaz gráfica)
- `sqlite3` (base de datos local)
- `cryptography` (para cifrado seguro)

## Instalación

```bash
pip install -r requirements.txt
```
> Asegúrate de estar usando **Python 3.7 o superior**

🧪 Uso
------

`python password_manager.py`

1.  ✏️ Introduce una descripción (por ejemplo: `"Correo Gmail"`)
    
2.  🎛️ Ajusta las opciones de seguridad (mayúsculas, dígitos, símbolos)
    
3.  🔁 Pulsa **Generar** para crear una contraseña segura
    
4.  💾 Pulsa **Guardar** para almacenarla cifrada
    
5.  📋 Pulsa **Mostrar Contraseñas** para ver lo guardado
