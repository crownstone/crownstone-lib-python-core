from enum import Enum


class EncryptionError(Enum):
    CAN_NOT_FIND_SERVICE              = "CAN_NOT_FIND_SERVICE"
    CAN_NOT_FIND_CHACTERISTIC         = "CAN_NOT_FIND_CHACTERISTIC"
    CAN_NOT_GET_CHARACTERISTIC        = "CAN_NOT_GET_CHARACTERISTIC"
    CAN_NOT_FIND_CCCD                 = "CAN_NOT_FIND_CCCD"
    ABORT_NOTIFICATION_STREAM_W_ERROR = "ABORT_NOTIFICATION_STREAM_W_ERROR"
    NOTIFICATION_STREAM_TIMEOUT       = "NOTIFICATION_STREAM_TIMEOUT"
    NO_NOTIFICATION_DATA_RECEIVED     = "NO_NOTIFICATION_DATA_RECEIVED"
    INVALID_SESSION_NONCE             = "INVALID_SESSION_NONCE"
    INVALID_SESSION_DATA              = "INVALID_SESSION_DATA"
    INVALID_ENCRYPTION_PACKAGE        = "INVALID_ENCRYPTION_PACKAGE"
    INVALID_ENCRYPTION_USER_LEVEL     = "INVALID_ENCRYPTION_USER_LEVEL"
    COULD_NOT_VALIDATE_SESSION_NONCE  = "COULD_NOT_VALIDATE_SESSION_NONCE"
    COULD_NOT_READ_SESSION_NONCE      = "COULD_NOT_READ_SESSION_NONCE"
    NO_SESSION_NONCE_SET              = "NO_SESSION_NONCE_SET"
    NO_ENCRYPTION_KEYS_SET            = "NO_ENCRYPTION_KEYS_SET"
    ENCRYPTION_VALIDATION_FAILED      = "ENCRYPTION_VALIDATION_FAILED"
    SETUP_FAILED                      = "SETUP_FAILED"
    NOT_IN_RECOVERY_MODE              = "NOT_IN_RECOVERY_MODE"
    RECOVERY_MODE_DISABLED            = "RECOVERY_MODE_DISABLED"


class CrownstoneError(Enum):
    ADMIN_KEY_REQUIRED                                  = "ADMIN_KEY_REQUIRED"
    MEMBER_KEY_REQUIRED                                 = "MEMBER_KEY_REQUIRED"
    BASIC_KEY_REQUIRED                                  = "BASIC_KEY_REQUIRED"
    SERVICE_DATA_KEY_REQUIRED                           = "SERVICE_DATA_KEY_REQUIRED"
    LOCALIZATION_KEY_REQUIRED                           = "LOCALIZATION_KEY_REQUIRED"
    MESH_APP_KEY                                        = "MESH_APP_KEY"
    MESH_NETWORK_KEY                                    = "MESH_NETWORK_KEY"
    INVALID_ADDRESS                                     = "INVALID_ADDRESS"

    NOT_IMPLEMENTED_YET                                 = "NOT_IMPLEMENTED_YET"

    DISCONNECTED                                        = "DISCONNECTED"
    CONNECTION_CANCELLED                                = "CONNECTION_CANCELLED"
    CONNECTION_FAILED                                   = "CONNECTION_FAILED"
    NOT_CONNECTED                                       = "NOT_CONNECTED"
    NO_SERVICES                                         = "NO_SERVICES"
    NO_CHARACTERISTICS                                  = "NO_CHARACTERISTICS"
    SERVICE_DOES_NOT_EXIST                              = "SERVICE_DOES_NOT_EXIST"
    CHARACTERISTIC_DOES_NOT_EXIST                       = "CHARACTERISTIC_DOES_NOT_EXIST"
    WRONG_TYPE_OF_PROMISE                               = "WRONG_TYPE_OF_PROMISE"
    INVALID_UUID                                        = "INVALID_UUID"
    NOT_INITIALIZED                                     = "NOT_INITIALIZED"
    CANNOT_SET_TIMEOUT_WITH_THIS_TYPE_OF_PROMISE        = "CANNOT_SET_TIMEOUT_WITH_THIS_TYPE_OF_PROMISE"
    TIMEOUT                                             = "TIMEOUT"
    DISCONNECT_TIMEOUT                                  = "DISCONNECT_TIMEOUT"
    ERROR_DISCONNECT_TIMEOUT                            = "ERROR_DISCONNECT_TIMEOUT"
    AWAIT_DISCONNECT_TIMEOUT                            = "AWAIT_DISCONNECT_TIMEOUT"
    CANCEL_PENDING_CONNECTION_TIMEOUT                   = "CANCEL_PENDING_CONNECTION_TIMEOUT"
    CONNECT_TIMEOUT                                     = "CONNECT_TIMEOUT"
    GET_SERVICES_TIMEOUT                                = "GET_SERVICES_TIMEOUT"
    GET_CHARACTERISTICS_TIMEOUT                         = "GET_CHARACTERISTICS_TIMEOUT"
    READ_CHARACTERISTIC_TIMEOUT                         = "READ_CHARACTERISTIC_TIMEOUT"
    WRITE_CHARACTERISTIC_TIMEOUT                        = "WRITE_CHARACTERISTIC_TIMEOUT"
    ENABLE_NOTIFICATIONS_TIMEOUT                        = "ENABLE_NOTIFICATIONS_TIMEOUT"
    NOTIFICATION_STREAM_TIMEOUT                         = "NOTIFICATION_STREAM_TIMEOUT"
    DISABLE_NOTIFICATIONS_TIMEOUT                       = "DISABLE_NOTIFICATIONS_TIMEOUT"
    CANNOT_WRITE_AND_VERIFY                             = "CANNOT_WRITE_AND_VERIFY"
    CAN_NOT_CONNECT_TO_UUID                             = "CAN_NOT_CONNECT_TO_UUID"
    COULD_NOT_FACTORY_RESET                             = "COULD_NOT_FACTORY_RESET"
    INCORRECT_RESPONSE_LENGTH                           = "INCORRECT_RESPONSE_LENGTH"
    UNKNOWN_TYPE                                        = "UNKNOWN_TYPE"
    COULD_NOT_GET_LOCATION                              = "COULD_NOT_GET_LOCATION"
    INVALID_SESSION_REFERENCE_ID                        = "INVALID_SESSION_REFERENCE_ID"
    INVALID_SESSION_DATA                                = "INVALID_SESSION_DATA"
    NO_SESSION_NONCE_SET                                = "NO_SESSION_NONCE_SET"
    COULD_NOT_VALIDATE_SESSION_NONCE                    = "COULD_NOT_VALIDATE_SESSION_NONCE"
    INVALID_SIZE_FOR_ENCRYPTED_PAYLOAD                  = "INVALID_SIZE_FOR_ENCRYPTED_PAYLOAD"
    INVALID_SIZE_FOR_SESSION_NONCE_PACKET               = "INVALID_SIZE_FOR_SESSION_NONCE_PACKET"
    INVALID_PACKAGE_FOR_ENCRYPTION_TOO_SHORT            = "INVALID_PACKAGE_FOR_ENCRYPTION_TOO_SHORT"
    INVALID_KEY_FOR_ENCRYPTION                          = "INVALID_KEY_FOR_ENCRYPTION"
    DO_NOT_HAVE_ENCRYPTION_KEY                          = "DO_NOT_HAVE_ENCRYPTION_KEY"
    COULD_NOT_ENCRYPT                                   = "COULD_NOT_ENCRYPT"
    COULD_NOT_ENCRYPT_KEYS_NOT_SET                      = "COULD_NOT_ENCRYPT_KEYS_NOT_SET"
    COULD_NOT_DECRYPT_KEYS_NOT_SET                      = "COULD_NOT_DECRYPT_KEYS_NOT_SET"
    COULD_NOT_DECRYPT                                   = "COULD_NOT_DECRYPT"
    CAN_NOT_GET_PAYLOAD                                 = "CAN_NOT_GET_PAYLOAD"
    USERLEVEL_IN_READ_PACKET_INVALID                    = "USERLEVEL_IN_READ_PACKET_INVALID"
    READ_SESSION_NONCE_ZERO_MAYBE_ENCRYPTION_DISABLED   = "READ_SESSION_NONCE_ZERO_MAYBE_ENCRYPTION_DISABLED"
    SETUP_FAILED                                        = "SETUP_FAILED"
    NOT_IN_RECOVERY_MODE                                = "NOT_IN_RECOVERY_MODE"
    CANNOT_READ_FACTORY_RESET_CHARACTERISTIC            = "CANNOT_READ_FACTORY_RESET_CHARACTERISTIC"
    RECOVER_MODE_DISABLED                               = "RECOVER_MODE_DISABLED"
    INVALID_TX_POWER_VALUE                              = "INVALID_TX_POWER_VALUE"
    NO_KEEPALIVE_STATE_ITEMS                            = "NO_KEEPALIVE_STATE_ITEMS"
    NO_SWITCH_STATE_ITEMS                               = "NO_SWITCH_STATE_ITEMS"
    DFU_OVERRULED                                       = "DFU_OVERRULED"
    DFU_ABORTED                                         = "DFU_ABORTED"
    DFU_ERROR                                           = "DFU_ERROR"
    COULD_NOT_FIND_PERIPHERAL                           = "COULD_NOT_FIND_PERIPHERAL"
    PACKETS_DO_NOT_MATCH                                = "PACKETS_DO_NOT_MATCH"
    NOT_IN_DFU_MODE                                     = "NOT_IN_DFU_MODE"
    REPLACED_WITH_OTHER_PROMISE                         = "REPLACED_WITH_OTHER_PROMISE"
    BLE_RESET                                           = "BLE_RESET"
    INCORRECT_SCHEDULE_ENTRY_INDEX                      = "INCORRECT_SCHEDULE_ENTRY_INDEX"
    INCORRECT_DATA_COUNT_FOR_ALL_TIMERS                 = "INCORRECT_DATA_COUNT_FOR_ALL_TIMERS"
    NO_SCHEDULE_ENTRIES_AVAILABLE                       = "NO_SCHEDULE_ENTRIES_AVAILABLE"
    NO_TIMER_FOUND                                      = "NO_TIMER_FOUND"
    PROCESS_ABORTED_WITH_ERROR                          = "PROCESS_ABORTED_WITH_ERROR"
    UNKNOWN_PROCESS_TYPE                                = "UNKNOWN_PROCESS_TYPE"
    INVALID_INPUT                                       = "INVALID_INPUT"
    INVALID_BROADCAST_ACCESS_LEVEL                      = "INVALID_BROADCAST_ACCESS_LEVEL"
    INVALID_BROADCAST_LOCATION_ID                       = "INVALID_BROADCAST_LOCATION_ID"
    INVALID_BROADCAST_PROFILE_INDEX                     = "INVALID_BROADCAST_PROFILE_INDEX"
    INVALID_BROADCAST_PAYLOAD_SIZE                      = "INVALID_BROADCAST_PAYLOAD_SIZE"
    BROADCAST_ERROR                                     = "BROADCAST_ERROR"
    BROADCAST_ABORTED                                   = "BROADCAST_ABORTED"
    BEHAVIOUR_INDEX_OUT_OF_RANGE                        = "BEHAVIOUR_INDEX_OUT_OF_RANGE"
    BEHAVIOUR_INVALID                                   = "BEHAVIOUR_INVALID"
    BEHAVIOUR_INVALID_RESPONSE                          = "BEHAVIOUR_INVALID_RESPONSE"
    BEHAVIOUR_NOT_FOUND_AT_INDEX                        = "BEHAVIOUR_NOT_FOUND_AT_INDEX"
    PROFILE_INDEX_MISSING                               = "PROFILE_INDEX_MISSING"
    TYPE_MISSING                                        = "TYPE_MISSING"
    DATA_MISSING                                        = "DATA_MISSING"
    ACTIVE_DAYS_MISSING                                 = "ACTIVE_DAYS_MISSING"
    ACTIVE_DAYS_INVALID                                 = "ACTIVE_DAYS_INVALID"
    NO_ACTIVE_DAYS                                      = "NO_ACTIVE_DAYS"
    BEHAVIOUR_ACTION_MISSING                            = "BEHAVIOUR_ACTION_MISSING"
    BEHAVIOUR_TIME_MISSING                              = "BEHAVIOUR_TIME_MISSING"
    BEHAVIOUR_INTENSITY_MISSING                         = "BEHAVIOUR_INTENSITY_MISSING"
    TWILIGHT_CANT_HAVE_PRESENCE                         = "TWILIGHT_CANT_HAVE_PRESENCE"
    TWILIGHT_CANT_HAVE_END_CONDITION                    = "TWILIGHT_CANT_HAVE_END_CONDITION"
    NO_TIME_TYPE                                        = "NO_TIME_TYPE"
    INVALID_TIME_TYPE                                   = "INVALID_TIME_TYPE"
    MISSING_TO_TIME                                     = "MISSING_TO_TIME"
    MISSING_FROM_TIME                                   = "MISSING_FROM_TIME"
    MISSING_TO_TIME_TYPE                                = "MISSING_TO_TIME_TYPE"
    MISSING_FROM_TIME_DATA                              = "MISSING_FROM_TIME_DATA"
    MISSING_TO_TIME_DATA                                = "MISSING_TO_TIME_DATA"
    MISSING_FROM_TIME_TYPE                              = "MISSING_FROM_TIME_TYPE"
    INVALID_TIME_FROM_TYPE                              = "INVALID_TIME_FROM_TYPE"
    INVALID_TIME_TO_TYPE                                = "INVALID_TIME_TO_TYPE"
    INVALID_FROM_DATA                                   = "INVALID_FROM_DATA"
    INVALID_TO_DATA                                     = "INVALID_TO_DATA"
    INVALID_PRESENCE_TYPE                               = "INVALID_PRESENCE_TYPE"
    NO_PRESENCE_TYPE                                    = "NO_PRESENCE_TYPE"
    NO_PRESENCE_DATA                                    = "NO_PRESENCE_DATA"
    NO_PRESENCE_DELAY                                   = "NO_PRESENCE_DELAY"
    NO_PRESENCE_LOCATION_IDS                            = "NO_PRESENCE_LOCATION_IDS"
    NO_END_CONDITION_TYPE                               = "NO_END_CONDITION_TYPE"
    NO_END_CONDITION_PRESENCE                           = "NO_END_CONDITION_PRESENCE"
    NO_END_CONDITION_DURATION                           = "NO_END_CONDITION_DURATION"
    PROTOCOL_NOT_SUPPORTED                              = "PROTOCOL_NOT_SUPPORTED"
    RESULT_NOT_SUCCESS                                  = "RESULT_NOT_SUCCESS"

    INVALID_SERVICE_DATA                                = "INVALID_SERVICE_DATA"
    UNKNOWN_SERVICE_DATA                                = "UNKNOWN_SERVICE_DATA"


# BART: Why is there a BLE exception in the core lib? How is it different?
# ALEX: This should not be here. It's a remnant from the initial split. I'd argue we can move away from this one and just use the CrownstoneException.
# This would however be breaking. We can do this in the next breaking release.
class CrownstoneBleException(Exception):
    code    = None
    type    = None
    message = None

    def __init__(self, type, message="", code=0):
        """
        Type is an enum,
        """
        self.type = type
        self.message = message
        self.code = code
        

class CrownstoneException(Exception):
    code    = None
    type    = None
    message = None
    
    def __init__(self, type, message, code=0):
        # TODO: what is type, and code?
        self.type = type
        self.message = message
        self.code = code
