# ==============================================================================
# UNAD - Universidad Nacional Abierta y a Distancia
# Curso: Programación (Código 213023)
# Fase 4: Prácticas simuladas - Sistema Integral de Gestión (Software FJ)
# Repositorio Colaborativo del Grupo
# ==============================================================================

from abc import ABC, abstractmethod
import datetime
import logging

# CONFIGURACIÓN DE LOGS (Registrado por: Milton Valbuena)
logging.basicConfig(
    filename='registro_eventos.log',
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    encoding='utf-8'
)

# ------------------------------------------------------------------------------
# 1. EXCEPCIONES PERSONALIZADAS (Aporte: Milton Valbuena)
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
# CLASE ABSTRACTA BASE (Entidad General del Sistema)
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

# 2. CLASE CLIENTE - Encapsulación y Validaciones (Aporte: Jhoana Vargas)
class Cliente(EntidadSistema):
    """Representa a un cliente dentro de Software FJ heredando de EntidadSistema."""
    
    # Constructor que inicializa el ID y los datos personales del cliente
    def __init__(self, id_cliente, nombre, correo, telefono):
        super().__init__(id_cliente)  # Llama al constructor de la clase padre
        self.nombre = nombre          # Valida y asigna el nombre
        self.correo = correo          # Valida y asigna el correo electrónico
        self.telefono = telefono      # Valida y asigna el número de teléfono

    # Getter para consultar el nombre encapsulado
    @property
    def nombre(self):
        return self._nombre

    # Setter para validar que el nombre tenga al menos 3 caracteres
    @nombre.setter
    def nombre(self, valor):
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ValidacionError("El nombre del cliente debe contener al menos 3 caracteres alfabéticos.")
        self._nombre = valor.strip()

    # Getter para consultar el correo encapsulado
    @property
    def correo(self):
        return self._correo

    # Setter para validar el formato básico del correo (@ y .)
    @correo.setter
    def correo(self, valor):
        if "@" not in valor or "." not in valor:
            raise ValidacionError(f"El correo electrónico '{valor}' no tiene un formato válido.")
        self._correo = valor.strip()

    # Getter para consultar el teléfono encapsulado
    @property
    def telefono(self):
        return self._telefono

    # Setter para validar que el teléfono sea numérico y de mínimo 7 dígitos
    @telefono.setter
    def telefono(self, valor):
        if not valor.isdigit() or len(valor) < 7:
            raise ValidacionError("El teléfono debe contener únicamente dígitos y una longitud mínima de 7 caracteres.")
        self._telefono = valor

    # Método sobrescrito que devuelve el resumen de datos del cliente
    def obtener_detalles(self):
        return f"Cliente [{self.id_entidad}] - {self.nombre} | Email: {self.correo} | Tel: {self.telefono}"


# ------------------------------------------------------------------------------
# 3. CLASE ABSTRACTA SERVICIO - Polimorfismo (Aporte: Jhoana Vargas)
# ------------------------------------------------------------------------------
class Servicio(EntidadSistema):
    """Clase abstracta base para los servicios ofrecidos por Software FJ."""
    
    # Constructor base para cualquier servicio del catálogo
    def __init__(self, id_servicio, nombre_servicio, tarifa_base):
        super().__init__(id_servicio)           # Asigna el ID del servicio
        self._nombre_servicio = nombre_servicio # Guarda el nombre del servicio
        self.tarifa_base = tarifa_base          # Valida y asigna la tarifa base por hora
        self._disponible = True                 # Inicia el servicio como disponible

    # Getter para obtener la tarifa base
    @property
    def tarifa_base(self):
        return self._tarifa_base

    # Setter para validar que la tarifa sea mayor a cero
    @tarifa_base.setter
    def tarifa_base(self, valor):
        if valor <= 0:
            raise ValidacionError("La tarifa base debe ser un valor monetario mayor a cero.")
        self._tarifa_base = float(valor)

    # Getter para consultar la disponibilidad del servicio
    @property
    def disponible(self):
        return self._disponible

    # Setter para actualizar el estado de disponibilidad
    @disponible.setter
    def disponible(self, estado):
        self._disponible = bool(estado)

    # Método abstracto polimórfico que cada servicio especializado debe implementar
    @abstractmethod
    def calcular_costo(self, horas, descuento=0.0, impuesto=0.19):
        """Calcula el costo total aplicando horas, descuento opcional e IVA."""
        pass

    # Método sobrescrito que muestra los detalles generales del servicio
    def obtener_detalles(self):
        estado_str = "Disponible" if self._disponible else "No Disponible"
        return f"Servicio [{self.id_entidad}] - {self._nombre_servicio} | Tarifa Base/h: ${self._tarifa_base:,.2f} | Estado: {estado_str}"


# ------------------------------------------------------------------------------
# 4. SERVICIOS ESPECIALIZADOS - Herencia y Sobrescritura (Aporte: Jhoana Vargas)
# ------------------------------------------------------------------------------
class ReservaSalas(Servicio):
    """Servicio especializado de alquiler de salas de estudio o reuniones."""
    
    # Constructor con tarifa fija de $25,000/h y opción de proyector
    def __init__(self, id_servicio, capacidad_personas, incluye_proyector=True):
        super().__init__(id_servicio, "Reserva de Salas de Estudio", tarifa_base=25000)
        self.capacidad_personas = capacidad_personas  # Capacidad máxima de personas
        self.incluye_proyector = incluye_proyector    # Indica si incluye equipo audiovisual

    # Cálculo polimórfico del costo total de la sala
    def calcular_costo(self, horas, descuento=0.0, impuesto=0.19):
        if horas <= 0:
            raise ValidacionError("Las horas solicitadas para la sala deben ser mayores a 0.")
        costo_subtotal = (self.tarifa_base * horas) * (1 - descuento)
        if self.incluye_proyector:
            costo_subtotal += 10000 * horas  # Recargo adicional por proyector
        return costo_subtotal * (1 + impuesto)


class AlquilerEquipos(Servicio):
    """Servicio especializado de alquiler de equipos de cómputo."""
    
    # Constructor con tarifa fija de $15,000/h y depósito de garantía
    def __init__(self, id_servicio, tipo_equipo, deposito_garantia=50000):
        super().__init__(id_servicio, f"Alquiler de Equipo ({tipo_equipo})", tarifa_base=15000)
        self.tipo_equipo = tipo_equipo              # Tipo o modelo del equipo
        self.deposito_garantia = deposito_garantia  # Depósito fijo de garantía

    # Cálculo polimórfico del costo total del alquiler
    def calcular_costo(self, horas, descuento=0.0, impuesto=0.19):
        if horas <= 0:
            raise ValidacionError("Las horas de alquiler de equipo deben ser superiores a 0.")
        costo_horas = (self.tarifa_base * horas) * (1 - descuento)
        costo_total = (costo_horas * (1 + impuesto)) + self.deposito_garantia
        return costo_total


class AsesoriaEspecializada(Servicio):
    """Servicio especializado de consultoría técnica en desarrollo."""
    
    # Constructor con tarifa base de $60,000/h y nivel del especialista
    def __init__(self, id_servicio, especialista, nivel_seniority="Senior"):
        super().__init__(id_servicio, f"Asesoría Especializada con {especialista}", tarifa_base=60000)
        self.especialista = especialista        # Nombre del asesor asignado
        self.nivel_seniority = nivel_seniority  # Nivel de experiencia (Senior o Junior)

    # Cálculo polimórfico del costo aplicando recargo si el asesor es Senior
    def calcular_costo(self, horas, descuento=0.0, impuesto=0.19):
        if horas <= 0:
            raise ValidacionError("La duración de la asesoría debe ser de al menos 1 hora.")
        factor_seniority = 1.3 if self.nivel_seniority == "Senior" else 1.0
        tarifa_ajustada = self.tarifa_base * factor_seniority
        subtotal = (tarifa_ajustada * horas) * (1 - descuento)
        return subtotal * (1 + impuesto)


# ------------------------------------------------------------------------------
# ESPACIO PARA LOS SIGUIENTES APORTES (Clase Reserva y Simulación de 10 pruebas)
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
# SIMULACIÓN INTEGRAL (DEMOSTRACIÓN DE 10 OPERACIONES - PUNTOS NATIVOS A PRUEBA)
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
            raise ValidacionError("Las horas de alquiler de equipo deben ser superiores a 0.")
        # Calcula el costo por hora aplicando el porcentaje de descuento
        costo_horas = (self.tarifa_base * horas) * (1 - descuento)
        # Suma el impuesto (IVA) y adiciona el depósito de garantía fijo
        costo_total = (costo_horas * (1 + impuesto)) + self.deposito_garantia
        return costo_total


class AsesoriaEspecializada(Servicio):
    """Servicio especializado de consultoría y asesoría técnica en desarrollo."""

    # Constructor con tarifa fija de $60,000/h y nivel de experiencia del especialista
    def __init__(self, id_servicio, especialista, nivel_seniority="Senior"):
        super().__init__(id_servicio, f"Asesoría Especializada con {especialista}", tarifa_base=60000)
        self.especialista = especialista          # Nombre del profesional asignado
        self.nivel_seniority = nivel_seniority    # Nivel técnico (ej. Senior o Junior)

    # Cálculo polimórfico del costo total de la asesoría
    def calcular_costo(self, horas, descuento=0.0, impuesto=0.19):
        if horas <= 0:
            raise ValidacionError("La duración de la asesoría debe ser de al menos 1 hora.")
        # Aplica un incremento del 30% si el especialista es nivel Senior
        factor_seniority = 1.3 if self.nivel_seniority == "Senior" else 1.0
        # Calcula la tarifa por hora ajustada según el nivel
        tarifa_ajustada = self.tarifa_base * factor_seniority
        # Calcula el subtotal descontando promociones
        subtotal = (tarifa_ajustada * horas) * (1 - descuento)
        # Retorna el valor final con impuestos incluidos
        return subtotal * (1 + impuesto)


# ------------------------------------------------------------------------------
# 5. CLASE RESERVA - Gestión del Proceso y Control de Estado (Aporte: Jhoana Vargas)
# ------------------------------------------------------------------------------
class Reserva(EntidadSistema):
    """Clase que integra Cliente, Servicio, Duración y Estado de la reserva."""

    # Constructor que valida las instancias y la disponibilidad del servicio
    def __init__(self, id_reserva, cliente, servicio, horas_solicitadas):
        super().__init__(id_reserva)  # Asigna el identificador único de la reserva
        # Verifica que el objeto recibido sea una instancia válida de Cliente
        if not isinstance(cliente, Cliente):
            raise ValidacionError("El objeto asignado debe ser una instancia válida de Cliente.")
        # Verifica que el objeto recibido sea una instancia válida de Servicio
        if not isinstance(servicio, Servicio):
            raise ValidacionError("El objeto asignado debe ser una instancia válida de Servicio.")
        # Verifica que el servicio se encuentre activo/disponible antes de reservar
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio._nombre_servicio}' no está disponible actualmente.")

        self.cliente = cliente                    # Asocia el objeto Cliente
        self.servicio = servicio                  # Asocia el objeto Servicio
        self.horas_solicitadas = horas_solicitadas  # Guarda la duración en horas
        self.estado = "Pendiente"                 # Estado inicial por defecto
        self.costo_total = 0.0                    # Inicializa el costo en cero

    # Procesa y confirma la reserva usando try/except/else/finally y encadenamiento
    def procesar_reserva(self, descuento=0.0):
        """Procesa y confirma la reserva aplicando el cálculo de costos con excepciones avanzadas."""
        try:
            # Evita confirmar dos veces una misma reserva
            if self.estado == "Confirmada":
                raise ReservaInvalidaError("La reserva ya ha sido confirmada anteriormente.")

            # Llama de forma polimórfica al cálculo de costo según el tipo de servicio
            self.costo_total = self.servicio.calcular_costo(self.horas_solicitadas, descuento=descuento)
            # Cambia el estado de la reserva a Confirmada
            self.estado = "Confirmada"
            # Registra la operación exitosa en el archivo de logs
            logging.info(f"ÉXITO: Reserva [{self.id_entidad}] confirmada para {self.cliente.nombre}. Costo: ${self.costo_total:,.2f}")

        except ValidacionError as ve:
            # Marca la reserva como fallida si hay errores de parámetros (ej. horas <= 0)
            self.estado = "Fallida"
            logging.error(f"FALLO VALIDACIÓN en Reserva [{self.id_entidad}]: {str(ve)}")
            # Encadena la excepción original hacia una excepción lógica de reserva
            raise ReservaInvalidaError(f"No se pudo procesar la reserva por un error de validación: {str(ve)}") from ve

        except Exception as e:
            # Captura cualquier error inesperado para evitar que el programa se detenga
            self.estado = "Error"
            logging.critical(f"ERROR CRÍTICO INESPERADO en Reserva [{self.id_entidad}]: {str(e)}")
            raise SoftwareFJError(f"Error inesperado procesando reserva: {str(e)}") from e

        else:
            # Se ejecuta únicamente si el bloque try finalizó sin lanzar excepciones
            print(f"  [+] Reserva [{self.id_entidad}] procesada con éxito. Total a pagar: ${self.costo_total:,.2f}")

        finally:
            # Se ejecuta siempre, haya ocurrido error o no, para dejar traza en consola
            print(f"  [*] Auditoría: Finalizó el intento de procesamiento para la Reserva [{self.id_entidad}] (Estado actual: {self.estado}).")

    # Permite cancelar una reserva activa verificando que no esté ya cancelada
    def cancelar_reserva(self):
        if self.estado == "Cancelada":
            raise ReservaInvalidaError("La reserva ya se encuentra cancelada.")
        self.estado = "Cancelada"  # Actualiza el estado a Cancelada
        logging.info(f"EVENTO: Reserva [{self.id_entidad}] fue cancelada por el cliente.")
        print(f"  [-] Reserva [{self.id_entidad}] cancelada correctamente.")

    # Método sobrescrito que devuelve el estado completo de la reserva
    def obtener_detalles(self):
        return f"Reserva [{self.id_entidad}] | Cliente: {self.cliente.nombre} | Servicio: {self.servicio._nombre_servicio} | Horas: {self.horas_solicitadas} | Estado: {self.estado}"
