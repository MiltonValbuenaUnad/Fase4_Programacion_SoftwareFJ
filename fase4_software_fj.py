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
