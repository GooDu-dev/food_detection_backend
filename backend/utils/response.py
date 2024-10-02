class Response:
    def __init__(self, status: int, code: str, data: dict = {}, next: str = ""):
        self._status = status
        self._code = code
        self._data = data
        self._next = next
    
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
    def get_response(self):
        return self._status, {
            "code": self._code,
            "status": self._status,
            "data": self._data,
            "next": self._next
        }
def createStatusOK(data: dict, next: str = ""):
    res = StatusOK
    res.set_data(data)
    res.set_next(next)
    return res.get_response()
def createStatusCreated(data: dict = {}, next: str = ""):
    res = StatusCreated
    res.set_data()

StatusOK = Response(200, "30000")
StatusCreated = Response(201, "30001")