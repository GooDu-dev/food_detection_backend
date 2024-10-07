"""
    Error response to send to client
    @version 1.0
    @author GooDu-Dev <https://github.com/GooDu-dev>
"""

class Error:
    def __init__(self, status: int, code: str, th_message: str, en_message: str, next: str, error_message: str = ""):
        self._status = status
        self._code = code
        self._th_message = th_message
        self._en_message = en_message
        self._error = error_message
        self._next = next
    
    def get_status(self):
        return self._status
    def get_code(self):
        return self._code
    def get_th_message(self):
        return self._th_message
    def get_en_message(self):
        return self._en_message
    def get_next(self):
        return self._next
    def get_error_message(self):
        return self._error
    def set_error_message(self, error_message: str):
        self._error = error_message
    def get_error_resposne(self):
        return self._status, {
            "code": self._code,
            "th_message": self._th_message,
            "en_message": self._en_message,
            "nextURL": self._next
        }
    
def new_server_error(message):
    err = InternalServerError
    err.set_error_message(message)
    return err
def new_client_error(message):
    err = ClientError
    err.set_error_message(message)
    return err

# simple error value
InternalServerError = Error(500, "10000", "เกิดบางอย่าผิดผลาด กรุณาลองใหม่อีกครั้งภายหลัง", "Something went wrong, please try again later", "", "")
CannotPredictError = Error(500, "ไม่สามารถทำนายได้ กรุณาลองใหม่อีกครั้ง", "Cannot predict, please try again later", "", "")
ClientError = Error(400, "20000", "คำขอไม่ถูกต้อง กรุณาลองใหม่อีกครั้งภายหลัง", "Invalid request, please try again later", "", "")
RequestMissingFieldError = Error(400, "20001", "คำขอไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง", "Invalid request, please try again later", "", "")
RequestInvalidError = Error(400, "20002", "คำขอไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง", "Invalid request, please try again later", "", "")
PageNotFoundError = Error(404, "20003", "ไม่พบข้อมูลปลายทาง, กรุณาตรวจสอบคำขอและลองใหม่อีกครั้ง", "Page not found, please re-check and try again later", "", "")
