"""
    Resposne format to send to client
    @version 1.0
    @author GooDu-Dev <https://github.com/GooDu-dev>
"""

class Response:
    def __init__(self, status: int, code: str, data: dict = {}, next: str = "", text_status: str = ""):
        self._status = status
        self._code = code
        self._data = data
        self._next = next
        self._text_status = text_status
    
    def get_status(self):
        return self._stats
    def get_code(self):
        return self._code
    def get_data(self):
        return self._data
    def set_data(self, data: dict):
        self._data = data
    def get_next(self):
        return self._next
    def set_next(self, next: str):
        self._next = next
    def get_text_status(self):
        return self._text_status
    def set_text_status(self, text_status: str):
        self._text_status = text_status
    def get_response(self):
        return self._status, {
            "code": self._code,
            "status": self._text_status,
            "data": self._data,
            "next": self._next
        }
# shortcut for create a statusOK
def createStatusOK(data: dict, next: str = ""):
    res = StatusOK
    res.set_data(data)
    res.set_next(next)
    res.set_text_status("success")
    return res.get_response()
# shortcut for create a statusCreated
def createStatusCreated(data: dict = {}, next: str = ""):
    res = StatusCreated
    res.set_data(data)
    res.set_next(next)
    res.set_text_status("created")
    return res.get_response()

# simple value status in resposne
StatusOK = Response(200, "30000")
StatusCreated = Response(201, "30001")