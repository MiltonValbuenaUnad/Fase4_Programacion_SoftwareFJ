# ==============================================================================
# UNAD - Universidad Nacional Abierta y a Distancia
# Curso: Programación (Código 213023)
# Fase 4: Prácticas simuladas - Sistema Integral de Gestión (Software FJ)
# ==============================================================================

from abc import ABC, abstractmethod
import datetime
import logging

# ------------------------------------------------------------------------------
# 1. CONFIGURACIÓN DEL SISTEMA DE LOGS (Registro de eventos y errores en archivo) (Aporte: Milton)
# ------------------------------------------------------------------------------
logging.basicConfig(
    filename='registro_eventos.log',
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    encoding='utf-8'
)

# ------------------------------------------------------------------------------
# 2. EXCEPCIONES PERSONALIZADAS (Aporte: Milton)
# ------------------------------------------------------------------------------
class SoftwareFJError(Exception):
    """Excepción base para el sistema Software FJ."""
    pass

class ValidacionError(SoftwareFJError):
    """Excepción lanzada cuando los datos de entrada son inválidos."""
    pass

class ServicioNoDisponibleError(SoftwareFJError):
    """Excepción lanzada cuando un servicio no se encuentra disponible."""
    pass

class ReservaInvalidaError(SoftwareFJError):
    """Excepción para errores lógicos en el proceso de reserva."""
    pass

# ------------------------------------------------------------------------------
# 3. CLASE ABSTRACTA BASE (Entidad General del Sistema) (Aporte:Jhoana Vargas)
# ------------------------------------------------------------------------------
class EntidadSistema(ABC):
    """Clase abstracta que define el comportamiento básico de las entidades del sistema."""
    def __init__(self, id_entidad):
        self._id_entidad = id_entidad

    @property
    def id_entidad(self):
        return self._id_entidad

    @abstractmethod
    def obtener_detalles(self):
        """Método abstracto que obliga a devolver la representación en texto de la entidad."""
        pass

# ------------------------------------------------------------------------------
# 4. CLASE CLIENTE (Encapsulación y Validaciones) (Aporte:Jhoana Vargas)
# ------------------------------------------------------------------------------
class Cliente(EntidadSistema):
    """Representa a un cliente dentro de Software FJ."""
    def __init__(self, id_cliente, nombre, correo, telefono):
        super().__init__(id_cliente)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ValidacionError("El nombre del cliente debe contener al menos 3 caracteres alfabéticos.")
        self._nombre = valor.strip()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if "@" not in valor or "." not in valor:
            raise ValidacionError(f"El correo electrónico '{valor}' no tiene un formato válido.")
        self._correo = valor.strip()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if not valor.isdigit() or len(valor) < 7:
            raise ValidacionError("El teléfono debe contener únicamente dígitos y una longitud mínima de 7 caracteres.")
        self._telefono = valor

    def obtener_detalles(self):
        return f"Cliente [{self.id_entidad}] - {self.nombre} | Email: {self.correo} | Tel: {self.telefono}"

# ------------------------------------------------------------------------------
# 5. CLASE ABSTRACTA SERVICIO (Polimorfismo) (Aporte:Jhoana Vargas)
# ------------------------------------------------------------------------------
class Servicio(EntidadSistema):
    """Clase abstracta base para los servicios ofrecidos por Software FJ."""
    def __init__(self, id_servicio, nombre_servicio, tarifa_base):
        super().__init__(id_servicio)
        self._nombre_servicio = nombre_servicio
        self.tarifa_base = tarifa_base
        self._disponible = True

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor):
        if valor <= 0:
            raise ValidacionError("La tarifa base debe ser un valor monetario mayor a cero.")
        self._tarifa_base = float(valor)

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, estado):
        self._disponible = bool(estado)

    @abstractmethod
    def calcular_costo(self, horas, descuento=0.0, impuesto=0.19):
        """Método abstracto polimórfico para el cálculo de costos con parámetros opcionales/sobrecargados."""
        pass

    def obtener_detalles(self):
        estado_str = "Disponible" if self._disponible else "No Disponible"
        return f"Servicio [{self.id_entidad}] - {self._nombre_servicio} | Tarifa Base/h: ${self._tarifa_base:,.2f} | Estado: {estado_str}"

# ------------------------------------------------------------------------------
# 6. SERVICIOS ESPECIALIZADOS (Herencia y Sobrescritura) (Aporte: Jhonatan)
# ------------------------------------------------------------------------------
class ReservaSalas(Servicio):
    """Servicio de alquiler de salas de estudio/reuniones."""
    def __init__(self, id_servicio, capacidad_personas, incluye_proyector=True):
        super().__init__(id_servicio, "Reserva de Salas de Estudio", tarifa_base=25000)
        self.capacidad_personas = capacidad_personas
        self.incluye_proyector = incluye_proyector

    def calcular_costo(self, horas, descuento=0.0, impuesto=0.19):
        if horas <= 0:
            raise ValidacionError("Las horas solicitadas para la sala deben ser mayores a 0.")
        costo_subtotal = (self.tarifa_base * horas) * (1 - descuento)
        if self.incluye_proyector:
            costo_subtotal += 10000 * horas  # Recargo por equipo audiovisual
        return costo_subtotal * (1 + impuesto)

class AlquilerEquipos(Servicio):
    """Servicio de alquiler de equipos de cómputo."""
    def __init__(self, id_servicio, tipo_equipo, deposito_garantia=50000):
        super().__init__(id_servicio, f"Alquiler de Equipo ({tipo_equipo})", tarifa_base=15000)
        self.tipo_equipo = tipo_equipo
        self.deposito_garantia = deposito_garantia

    def calcular_costo(self, horas, descuento=0.0, impuesto=0.19):
        if horas <= 0:
            raise ValidacionError("Las horas de alquiler de equipo deben ser superiores a 0.")
        costo_horas = (self.tarifa_base * horas) * (1 - descuento)
        costo_total = (costo_horas * (1 + impuesto)) + self.deposito_garantia
        return costo_total

class AsesoriaEspecializada(Servicio):
    """Servicio de consultoría y asesoría técnica en desarrollo."""
    def __init__(self, id_servicio, especialista, nivel_seniority="Senior"):
        super().__init__(id_servicio, f"Asesoría Especializada con {especialista}", tarifa_base=60000)
        self.especialista = especialista
        self.nivel_seniority = nivel_seniority

    def calcular_costo(self, horas, descuento=0.0, impuesto=0.19):
        if horas <= 0:
            raise ValidacionError("La duración de la asesoría debe ser de al menos 1 hora.")
        factor_seniority = 1.3 if self.nivel_seniority == "Senior" else 1.0
        tarifa_ajustada = self.tarifa_base * factor_seniority
        subtotal = (tarifa_ajustada * horas) * (1 - descuento)
        return subtotal * (1 + impuesto)

# ------------------------------------------------------------------------------
# 7. CLASE RESERVA (Gestión del Proceso y Control de Estado)
# ------------------------------------------------------------------------------
class Reserva(EntidadSistema):
    """Clase que integra Cliente, Servicio, Duración y Estado de la reserva."""
    def __init__(self, id_reserva, cliente, servicio, horas_solicitadas):
        super().__init__(id_reserva)
        if not isinstance(cliente, Cliente):
            raise ValidacionError("El objeto asignado debe ser una instancia válida de Cliente.")
        if not isinstance(servicio, Servicio):
            raise ValidacionError("El objeto asignado debe ser una instancia válida de Servicio.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio._nombre_servicio}' no está disponible actualmente.")

        self.cliente = cliente
        self.servicio = servicio
        self.horas_solicitadas = horas_solicitadas
        self.estado = "Pendiente"
        self.costo_total = 0.0

    def procesar_reserva(self, descuento=0.0):
        """Procesa y confirma la reserva aplicando el cálculo de costos con excepciones avanzadas."""
        try:
            if self.estado == "Confirmada":
                raise ReservaInvalidaError("La reserva ya ha sido confirmada anteriormente.")

            # Cálculo polimórfico
            self.costo_total = self.servicio.calcular_costo(self.horas_solicitadas, descuento=descuento)
            self.estado = "Confirmada"
            logging.info(f"ÉXITO: Reserva [{self.id_entidad}] confirmada para {self.cliente.nombre}. Costo: ${self.costo_total:,.2f}")

        except ValidacionError as ve:
            self.estado = "Fallida"
            logging.error(f"FALLO VALIDACIÓN en Reserva [{self.id_entidad}]: {str(ve)}")
            raise ReservaInvalidaError(f"No se pudo procesar la reserva por un error de validación: {str(ve)}") from ve

        except Exception as e:
            self.estado = "Error"
            logging.critical(f"ERROR CRÍTICO INESPERADO en Reserva [{self.id_entidad}]: {str(e)}")
            raise SoftwareFJError(f"Error inesperado procesando reserva: {str(e)}") from e

        else:
            print(f"  [+] Reserva [{self.id_entidad}] procesada con éxito. Total a pagar: ${self.costo_total:,.2f}")

        finally:
            print(f"  [*] Auditoría: Finalizó el intento de procesamiento para la Reserva [{self.id_entidad}] (Estado actual: {self.estado}).")

    def cancelar_reserva(self):
        if self.estado == "Cancelada":
            raise ReservaInvalidaError("La reserva ya se encuentra cancelada.")
        self.estado = "Cancelada"
        logging.info(f"EVENTO: Reserva [{self.id_entidad}] fue cancelada por el cliente.")
        print(f"  [-] Reserva [{self.id_entidad}] cancelada correctamente.")

    def obtener_detalles(self):
        return f"Reserva [{self.id_entidad}] | Cliente: {self.cliente.nombre} | Servicio: {self.servicio._nombre_servicio} | Horas: {self.horas_solicitadas} | Estado: {self.estado}"

# ------------------------------------------------------------------------------
# 8. SIMULACIÓN INTEGRAL (DEMOSTRACIÓN DE 10 OPERACIONES - PUNTOS NATIVOS A PRUEBA)
# ------------------------------------------------------------------------------
def ejecutar_simulacion():
    print("="*80)
    print("         SOFTWARE FJ - SISTEMA INTEGRAL DE GESTIÓN (DEMOSTRACIÓN DE PRUEBAS)")
    print("="*80 + "\n")

    logging.info("INICIO DE SESIÓN DE SIMULACIÓN - SOFTWARE FJ")

    # Bancos de almacenamiento en memoria
    clientes_db = []
    servicios_db = []
    reservas_db = []

    # --------------------------------------------------------------------------
    # OPERACIÓN 1: Creación correcta de un Cliente
    # --------------------------------------------------------------------------
    print("Operación 1: Registro correcto de Cliente")
    try:
        c1 = Cliente("CLI-01", "Milton Valbuena", "milton@unad.edu.co", "3101234567")
        clientes_db.append(c1)
        logging.info(f"ÉXITO: Cliente registrado correctamente -> {c1.obtener_detalles()}")
        print(f"  [OK] {c1.obtener_detalles()}")
    except ValidacionError as e:
        print(f"  [ERROR CAPTURADO]: {e}")

    # --------------------------------------------------------------------------
    # OPERACIÓN 2: Intento de creación de Cliente con datos inválidos (Error de Validación) (Aporte: Jhoana Vargas)
    # --------------------------------------------------------------------------
    print("\nOperación 2: Registro de Cliente con correo inválido (Detección de Error)")
    try:
        c2 = Cliente("CLI-02", "Juan Perez", "correo_sin_arroba.com", "3000000000")
        clientes_db.append(c2)
    except ValidacionError as e:
        logging.warning(f"CONTROLADO: Error de validación al crear cliente CLI-02 -> {str(e)}")
        print(f"  [OK - CAPTURADO Y REGISTRADO EN LOG]: {e}")

    # --------------------------------------------------------------------------
    # OPERACIÓN 3: Creación de Servicios Válidos (Polimorfismo / Herencia)
    # --------------------------------------------------------------------------
    print("\nOperación 3: Creación de catálogo de Servicios (Salas, Equipos, Asesorías)")
    try:
        s1 = ReservaSalas("SERV-01", capacidad_personas=6, incluye_proyector=True)
        s2 = AlquilerEquipos("SERV-02", tipo_equipo="Laptop Core i7")
        s3 = AsesoriaEspecializada("SERV-03", especialista="Ing. Alejandro", nivel_seniority="Senior")
        servicios_db.extend([s1, s2, s3])
        logging.info("ÉXITO: Servicios creados e ingresados al catálogo.")
        for s in servicios_db:
            print(f"  [OK] {s.obtener_detalles()}")
    except ValidacionError as e:
        print(f"  [ERROR]: {e}")

    # --------------------------------------------------------------------------
    # OPERACIÓN 4: Creación de Servicio con tarifa negativa (Invalidez)
    # --------------------------------------------------------------------------
    print("\nOperación 4: Intento de creación de Servicio con tarifa negativa")
    try:
        s_invalido = AlquilerEquipos("SERV-04", tipo_equipo="Monitor 4K")
        s_invalido.tarifa_base = -5000
    except ValidacionError as e:
        logging.warning(f"CONTROLADO: Tarifa inválida rechazada -> {str(e)}")
        print(f"  [OK - CAPTURADO Y REGISTRADO EN LOG]: {e}")

    # --------------------------------------------------------------------------
    # OPERACIÓN 5: Procesar Reserva 1 Exitosa (Reserva de Sala por 3 horas)
    # --------------------------------------------------------------------------
    print("\nOperación 5: Procesamiento de Reserva 1 Exitosa (Sala de estudio)")
    try:
        r1 = Reserva("RES-01", clientes_db[0], servicios_db[0], horas_solicitadas=3)
        reservas_db.append(r1)
        r1.procesar_reserva(descuento=0.10) # 10% descuento por ser estudiante
    except (SoftwareFJError, ValidacionError) as e:
        print(f"  [ERROR]: {e}")
