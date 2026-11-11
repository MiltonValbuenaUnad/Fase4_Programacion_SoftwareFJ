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
# 2. CLASE ABSTRACTA BASE (Pendiente por integrante del equipo)
# ------------------------------------------------------------------------------
class EntidadSistema(ABC):
    """Clase abstracta general del sistema."""
    def __init__(self, id_entidad):
        self._id_entidad = id_entidad

    @abstractmethod
    def obtener_detalles(self):
        pass

# ------------------------------------------------------------------------------
# 3. ESPACIO PARA APORTES DE LOS DEMÁS INTEGRANTES
# Integrante 2: Clase Cliente y validaciones de datos personales
# Integrante 3: Clase Abstracta Servicio y Servicios Especializados
# Integrante 4: Clase Reserva y métodos de confirmación/cancelación
# Integrante 5: Módulo de Simulación con las 10 operaciones de prueba
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    logging.info("Inicio del proyecto colaborativo Software FJ.")
    print("Repositorio inicializado correctamente. Listo para recibir aportes del equipo.")