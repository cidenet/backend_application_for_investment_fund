class SubscriptionNotificationChannel:
    EMAIL = "email"
    SMS = "sms"


class FundStatus:
    ACTIVE = "active"
    INACTIVE = "inactive"


class FundSuccessMessage:
    SUCCESS_FUND_CREATED = "Fondo creado con éxito"


class TransactionAction:
    CREATED = "created"
    CANCELLED = "cancelled"


class SubscriptionError:
    ERROR_NO_AVAILABLE_BALANCE = "No tiene saldo disponible para vincularse al fondo"
    ERROR_NO_MINIMUM_AMOUNT_TO_INVEST = "El fondo no tiene un monto mínimo de inversión"
    ERROR_USER_ALREADY_SUBSCRIBED_TO_FUND = "El usuario ya está suscrito a este fondo"
    ERROR_USER_DOES_NOT_EXIST_TO_SUBSCRIBE_TO_FUND = (
        "No existe el usuario para suscribirse al fondo"
    )
    ERROR_FUND_DOES_NOT_EXIST_TO_SUBSCRIBE = (
        "No existe el fondo para realizar la suscripción"
    )
    ERROR_USER_DOEES_NOT_EXIST = "El usuario no existe"


class DataBaseError:
    ERROR_DB_CONNECTION = "Error de conexión a la base de datos"


class SuccessMessage:
    SUCCESS_SUBSCRIPTION = "Suscripción realizada con éxito"
    SUCCESS_TRANSACTION = "Transacción completada con éxito"
    SUCCESS_SUBSCRIPTION_CANCELLATION = "Suscripción cancelada con éxito"
