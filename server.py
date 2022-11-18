import os
import socket
import threading
IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data" 
def handle_client(conn, addr):
    print(f"[NUEVA CONEXION] {addr} Conectado.")
    conn.send("OK@Bienvenido al servidor de archivos.".encode(FORMAT))
    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]
        if cmd == "LISTAR":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"
            if len(files) == 0:
               send_data += "El servidor está vacío"
            else:
                send_data += "\n".join(f for f in files)
            conn.send(send_data.encode(FORMAT))
        elif cmd == "CARGAR":
            name, text = data[1], data[2]
            filepath = os.path.join(SERVER_DATA_PATH, name)
            with open(filepath, "w") as f:
                f.write(text)
            send_data = "OK@Archivo cargado exitosamente."
            conn.send(send_data.encode(FORMAT))
        elif cmd == "BORRAR":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"
            filename = data[1]
            if len(files) == 0:
                send_data += "El servidor está vacío"
            else:   
                if filename in files:
                    os.system(f"rm {SERVER_DATA_PATH}/{filename}")
                    send_data += "Archivo borrado exitosamente."
                else:
                    send_data += "Archivo no encontrado."

            conn.send(send_data.encode(FORMAT))
        elif cmd == "SALIR":
            break
        elif cmd == "AYUDA":
            data = "OK@"
            data += "LISTAR: Listar todos los archivos del servidor.\n"
            data += "CARGAR <path>: Cargar un archivo al servidor.\n"
            data += "BORRAR <filename>: Borrar archivo del servidor.\n"
            data += "SALIR: Disconnect from the server.\n"
            data += "AYUDA: Listar los comandos."

            conn.send(data.encode(FORMAT))
    print(f"[DESCONECTADO] {addr} se a desconectado")
    conn.close()

def main():
    print("[INICIANDO] el servidor está iniciando")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[ESCUCHANDO] Servidor escuchando en  {IP}:{PORT}.")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[CONEXIONES ACTIVAS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()
