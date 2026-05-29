import json
from pathlib import Path

ARCHIVO_DATOS = Path("salon_belleza_datos.json")


class Persona:
    def __init__(self, nombre, telefono):
        self.nombre = nombre
        self.telefono = telefono

    def mostrar_info(self):
        return f"Nombre: {self.nombre} | Teléfono: {self.telefono}"


class Cliente(Persona):
    def __init__(self, nombre, telefono, correo):
        super().__init__(nombre, telefono)
        self.correo = correo

    def mostrar_info(self):
        return f"Cliente: {self.nombre} | Teléfono: {self.telefono} | Correo: {self.correo}"

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "telefono": self.telefono,
            "correo": self.correo
        }


class Empleado(Persona):
    def __init__(self, nombre, telefono, cargo):
        super().__init__(nombre, telefono)
        self.cargo = cargo

    def mostrar_info(self):
        return f"Empleado: {self.nombre} | Teléfono: {self.telefono} | Cargo: {self.cargo}"

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "telefono": self.telefono,
            "cargo": self.cargo
        }


class Servicio:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def calcular_precio(self):
        return self.precio

    def mostrar_servicio(self):
        return f"{self.nombre} - ${self.calcular_precio():,.0f}"

    def to_dict(self):
        return {
            "tipo": self.__class__.__name__,
            "nombre": self.nombre,
            "precio": self.precio
        }


class ServicioBasico(Servicio):
    def calcular_precio(self):
        return self.precio


class ServicioPremium(Servicio):
    def calcular_precio(self):
        return self.precio * 1.20


class Cita:
    def __init__(self, cliente, empleado, servicio, fecha, hora):
        self.cliente = cliente
        self.empleado = empleado
        self.servicio = servicio
        self.fecha = fecha
        self.hora = hora

    def mostrar_cita(self):
        return (
            f"Fecha: {self.fecha} | Hora: {self.hora}\n"
            f"{self.cliente.mostrar_info()}\n"
            f"{self.empleado.mostrar_info()}\n"
            f"Servicio: {self.servicio.mostrar_servicio()}"
        )

    def to_dict(self):
        return {
            "cliente": self.cliente.to_dict(),
            "empleado": self.empleado.to_dict(),
            "servicio": self.servicio.to_dict(),
            "fecha": self.fecha,
            "hora": self.hora
        }


class SalonBelleza:
    def __init__(self, nombre):
        self.nombre = nombre
        self.clientes = []
        self.empleados = []
        self.servicios = []
        self.citas = []
        self.cargar_datos()

    def agregar_cliente(self, cliente):
        self.clientes.append(cliente)
        self.guardar_datos()

    def agregar_empleado(self, empleado):
        self.empleados.append(empleado)
        self.guardar_datos()

    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)
        self.guardar_datos()

    def agendar_cita(self, cita):
        self.citas.append(cita)
        self.guardar_datos()

    def listar_clientes(self):
        if not self.clientes:
            print("No hay clientes registrados.")
            return

        print("\n=== CLIENTES REGISTRADOS ===")
        for i, cliente in enumerate(self.clientes, start=1):
            print(f"{i}. {cliente.mostrar_info()}")

    def listar_empleados(self):
        if not self.empleados:
            print("No hay empleados registrados.")
            return

        print("\n=== EMPLEADOS REGISTRADOS ===")
        for i, empleado in enumerate(self.empleados, start=1):
            print(f"{i}. {empleado.mostrar_info()}")

    def listar_servicios(self):
        if not self.servicios:
            print("No hay servicios registrados.")
            return

        print("\n=== SERVICIOS REGISTRADOS ===")
        for i, servicio in enumerate(self.servicios, start=1):
            print(f"{i}. {servicio.mostrar_servicio()}")

    def listar_citas(self):
        if not self.citas:
            print("No hay citas registradas.")
            return

        print("\n=== CITAS AGENDADAS ===")
        for i, cita in enumerate(self.citas, start=1):
            print(f"\nCita #{i}")
            print(cita.mostrar_cita())

    def guardar_datos(self):
        datos = {
            "clientes": [cliente.to_dict() for cliente in self.clientes],
            "empleados": [empleado.to_dict() for empleado in self.empleados],
            "servicios": [servicio.to_dict() for servicio in self.servicios],
            "citas": [cita.to_dict() for cita in self.citas]
        }

        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

    def cargar_datos(self):
        if not ARCHIVO_DATOS.exists():
            return

        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        self.clientes = [
            Cliente(c["nombre"], c["telefono"], c["correo"])
            for c in datos.get("clientes", [])
        ]

        self.empleados = [
            Empleado(e["nombre"], e["telefono"], e["cargo"])
            for e in datos.get("empleados", [])
        ]

        self.servicios = []
        for s in datos.get("servicios", []):
            if s["tipo"] == "ServicioPremium":
                servicio = ServicioPremium(s["nombre"], s["precio"])
            else:
                servicio = ServicioBasico(s["nombre"], s["precio"])
            self.servicios.append(servicio)

        self.citas = []
        for c in datos.get("citas", []):
            cliente_data = c["cliente"]
            empleado_data = c["empleado"]
            servicio_data = c["servicio"]

            cliente = Cliente(
                cliente_data["nombre"],
                cliente_data["telefono"],
                cliente_data["correo"]
            )

            empleado = Empleado(
                empleado_data["nombre"],
                empleado_data["telefono"],
                empleado_data["cargo"]
            )

            if servicio_data["tipo"] == "ServicioPremium":
                servicio = ServicioPremium(servicio_data["nombre"], servicio_data["precio"])
            else:
                servicio = ServicioBasico(servicio_data["nombre"], servicio_data["precio"])

            cita = Cita(cliente, empleado, servicio, c["fecha"], c["hora"])
            self.citas.append(cita)


def pedir_numero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Debes ingresar un número válido.")


def seleccionar_elemento(lista, mensaje):
    while True:
        opcion = pedir_numero(mensaje)

        if 1 <= opcion <= len(lista):
            return lista[opcion - 1]

        print("Opción inválida. Intenta nuevamente.")


def registrar_cliente(salon):
    print("\n=== REGISTRAR CLIENTE ===")
    nombre = input("Nombre del cliente: ")
    telefono = input("Teléfono: ")
    correo = input("Correo: ")

    cliente = Cliente(nombre, telefono, correo)
    salon.agregar_cliente(cliente)

    print("Cliente registrado y guardado correctamente.")


def registrar_empleado(salon):
    print("\n=== REGISTRAR EMPLEADO ===")
    nombre = input("Nombre del empleado: ")
    telefono = input("Teléfono: ")
    cargo = input("Cargo: ")

    empleado = Empleado(nombre, telefono, cargo)
    salon.agregar_empleado(empleado)

    print("Empleado registrado y guardado correctamente.")


def registrar_servicio(salon):
    print("\n=== REGISTRAR SERVICIO ===")
    nombre = input("Nombre del servicio: ")
    precio = pedir_numero("Precio base: ")

    print("Tipo de servicio:")
    print("1. Básico")
    print("2. Premium")

    tipo = input("Selecciona una opción: ")

    if tipo == "2":
        servicio = ServicioPremium(nombre, precio)
    else:
        servicio = ServicioBasico(nombre, precio)

    salon.agregar_servicio(servicio)

    print("Servicio registrado y guardado correctamente.")


def agendar_cita(salon):
    print("\n=== AGENDAR CITA ===")

    if not salon.clientes:
        print("Primero debes registrar al menos un cliente.")
        return

    if not salon.empleados:
        print("Primero debes registrar al menos un empleado.")
        return

    if not salon.servicios:
        print("Primero debes registrar al menos un servicio.")
        return

    salon.listar_clientes()
    cliente = seleccionar_elemento(salon.clientes, "Selecciona el número del cliente: ")

    salon.listar_empleados()
    empleado = seleccionar_elemento(salon.empleados, "Selecciona el número del empleado: ")

    salon.listar_servicios()
    servicio = seleccionar_elemento(salon.servicios, "Selecciona el número del servicio: ")

    fecha = input("Fecha de la cita (dd/mm/aaaa): ")
    hora = input("Hora de la cita: ")

    cita = Cita(cliente, empleado, servicio, fecha, hora)
    salon.agendar_cita(cita)

    print("\nCita agendada y guardada correctamente.")
    print("\nResumen de la cita:")
    print(cita.mostrar_cita())


def cargar_datos_prueba(salon):
    cliente1 = Cliente("Laura Martínez", "3001234567", "laura@email.com")
    cliente2 = Cliente("Camila Torres", "3019876543", "camila@email.com")

    empleado1 = Empleado("Valentina Rojas", "3104567890", "Estilista")
    empleado2 = Empleado("Daniela Pérez", "3152223344", "Manicurista")

    servicio1 = ServicioBasico("Corte de cabello", 35000)
    servicio2 = ServicioPremium("Coloración premium", 90000)
    servicio3 = ServicioBasico("Manicure", 30000)

    salon.clientes = [cliente1, cliente2]
    salon.empleados = [empleado1, empleado2]
    salon.servicios = [servicio1, servicio2, servicio3]
    salon.citas = [
        Cita(cliente1, empleado1, servicio2, "21/05/2026", "3:00 PM"),
        Cita(cliente2, empleado2, servicio3, "22/05/2026", "10:00 AM")
    ]

    salon.guardar_datos()
    print("Datos de prueba cargados y guardados correctamente.")


def menu():
    salon = SalonBelleza("Salón de Belleza Glam")

    print("Sistema iniciado.")
    print("Los datos guardados anteriormente se cargan automáticamente.")

    while True:
        print("\n==============================")
        print(" SISTEMA DE SALÓN DE BELLEZA")
        print("==============================")
        print("1. Registrar cliente")
        print("2. Registrar empleado")
        print("3. Registrar servicio")
        print("4. Agendar cita")
        print("5. Ver clientes")
        print("6. Ver empleados")
        print("7. Ver servicios")
        print("8. Ver citas")
        print("9. Cargar datos de prueba")
        print("0. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            registrar_cliente(salon)
        elif opcion == "2":
            registrar_empleado(salon)
        elif opcion == "3":
            registrar_servicio(salon)
        elif opcion == "4":
            agendar_cita(salon)
        elif opcion == "5":
            salon.listar_clientes()
        elif opcion == "6":
            salon.listar_empleados()
        elif opcion == "7":
            salon.listar_servicios()
        elif opcion == "8":
            salon.listar_citas()
        elif opcion == "9":
            cargar_datos_prueba(salon)
        elif opcion == "0":
            salon.guardar_datos()
            print("Datos guardados. Gracias por usar el sistema.")
            break
        else:
            print("Opción inválida. Intenta nuevamente.")


if __name__ == "__main__":
    menu()
''
