import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import os


# =============================
#  SERVIDOR HTTP PARA EL PROXY
# =============================
class PS3UpdateHandler(BaseHTTPRequestHandler):
    pup_path = ""
    report_version = "4.90"

    def do_GET(self):
        if self.path.endswith("/update/ps3/list"):
            # Respuesta simulando un firmware oficial
            xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<update>
    <version>{self.report_version}</version>
    <url>http://{self.server.server_address[0]}:{self.server.server_address[1]}/update/ps3/patch.pup</url>
</update>
"""
            self.send_response(200)
            self.send_header("Content-Type", "text/xml")
            self.end_headers()
            self.wfile.write(xml_response.encode())
        elif self.path.endswith("patch.pup"):
            if os.path.exists(self.pup_path):
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                self.end_headers()
                with open(self.pup_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "Archivo PUP no encontrado.")
        else:
            self.send_error(404, "Recurso no encontrado.")

    def log_message(self, format, *args):
        return  # Silenciar consola del servidor


# =============================
#       INTERFAZ GRÁFICA
# =============================
class PS3ProxyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🛰️ PS3 HFW Proxy - GUI Mejorado")
        self.server_thread = None
        self.httpd = None

        # 🔒 DESACTIVAR MAXIMIZAR
        self.root.resizable(False, False)

        # -------------------------
        #      TÍTULO
        # -------------------------
        title = ttk.Label(
            root,
            text="🛠️ PS3 HFW Proxy Controller",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)

        # Marco de entrada
        frame = ttk.Frame(root, padding=10)
        frame.pack()

        # -------------------------
        #   CAMPOS DE CONFIG
        # -------------------------
        ttk.Label(frame, text="📁 Archivo PUP:").grid(row=0, column=0, sticky="w")
        self.pup_entry = ttk.Entry(frame, width=50)
        self.pup_entry.grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="Buscar", command=self.select_pup).grid(row=0, column=2)

        ttk.Label(frame, text="🔢 Versión Reportada:").grid(row=1, column=0, sticky="w")
        self.version_entry = ttk.Entry(frame)
        self.version_entry.insert(0, "4.90")
        self.version_entry.grid(row=1, column=1, padx=5)

        ttk.Label(frame, text="🌐 Host (0.0.0.0 = todas las interfaces):").grid(row=2, column=0, sticky="w")
        self.host_entry = ttk.Entry(frame)
        self.host_entry.insert(0, "0.0.0.0")
        self.host_entry.grid(row=2, column=1, padx=5)

        ttk.Label(frame, text="🔌 Puerto:").grid(row=3, column=0, sticky="w")
        self.port_entry = ttk.Entry(frame)
        self.port_entry.insert(0, "8080")
        self.port_entry.grid(row=3, column=1, padx=5)

        # -------------------------
        #   BOTONES DE CONTROL
        # -------------------------
        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=10)

        self.start_button = ttk.Button(btn_frame, text="▶️ Iniciar Proxy", command=self.start_proxy)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = ttk.Button(btn_frame, text="⏹️ Detener Proxy", command=self.stop_proxy, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=5)

        # -------------------------
        #     INDICADOR DE ESTADO
        # -------------------------
        self.status_label = ttk.Label(root, text="🔴 Estado: Inactivo", foreground="red")
        self.status_label.pack()

        # -------------------------
        #        LOGS
        # -------------------------
        log_label = ttk.Label(root, text="📜 Registro de Logs:")
        log_label.pack()

        self.log_text = tk.Text(root, height=8, state="disabled")
        self.log_text.pack(padx=10, pady=5)

    # =============================
    #         FUNCIONES GUI
    # =============================

    def select_pup(self):
        path = filedialog.askopenfilename(filetypes=[("PS3 Update File", "*.PUP")])
        if path:
            self.pup_entry.delete(0, tk.END)
            self.pup_entry.insert(0, path)

    def log(self, text):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.config(state="disabled")

    def start_proxy(self):
        pup_path = self.pup_entry.get().strip()
        version = self.version_entry.get().strip()
        host = self.host_entry.get().strip()
        port = int(self.port_entry.get().strip())

        if not os.path.exists(pup_path):
            messagebox.showerror("Error", "El archivo PUP seleccionado no existe.")
            return

        PS3UpdateHandler.pup_path = pup_path
        PS3UpdateHandler.report_version = version

        self.httpd = HTTPServer((host, port), PS3UpdateHandler)

        self.server_thread = threading.Thread(target=self.httpd.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

        self.log(f"🟢 Proxy iniciado en {host}:{port}")
        self.status_label.config(text=f"🟢 Estado: Ejecutando en {host}:{port}", foreground="green")

        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

    def stop_proxy(self):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
            self.log("🔴 Proxy detenido")

        self.status_label.config(text="🔴 Estado: Inactivo", foreground="red")

        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")


# =============================
#         EJECUCIÓN
# =============================
if __name__ == "__main__":
    root = tk.Tk()
    PS3ProxyGUI(root)
    root.mainloop()
