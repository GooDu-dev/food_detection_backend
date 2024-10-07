from datetime import datetime
from dataclasses import dataclass
import utils.errors as error

@dataclass
class FruitItem:

    _next_id = 1

    def __init__(self, name: str, date_add: str, status: str ):
        self._id = FruitItem._next_id
        self._name = name
        self._date_add = datetime.strptime(date_add, "%Y-%m-%d").date()
        self._status = status
        FruitItem._next_id += 1
    
    def get_id(self):
        return self._id
    def set_id(self, id: int):
        self._id = id
    def get_name(self):
        return self._name
    def get_date_add(self):
        return self._date_add.strftime('%Y-%m-%d')
    def get_status(self):
        return self._status
    def set_status(self, status: str):
        self._status = status
    
    def get_response(self):
        return {
            "id": self._id,
            "name": self._name,
            "date": self._date_add.strftime('%Y-%m-%d'),
            "status": self._status
        }
    def __str__(self):
        return f"id: {self._id}, name: {self._name}, date: {self._date_add}, status: {self._status}"

class FruitManager:
    _data: list[FruitItem] = [
        FruitItem("apple", "2024-10-07", "Success"),
        FruitItem("banana", "2024-10-09", "Waiting"),
    ]

    def __init__(self, data: list[FruitItem] = None):
        if data is not None :
            self._data = data


    def get_data(self):
        if self._data is not None :
            print(self._data)
            result = [fruit.get_response() for fruit in self._data]
        else:
            result = [fruit.get_response() for fruit in FruitManager._data]
        return result
    def get_by_id(self, id: int):
        if self._data is not None :
            result = [fruit for fruit in self._data if fruit.get_id() == id][0]
        else:
            result = [fruit for fruit in FruitManager._data if fruit.get_id() == id][0]
        return FruitManager([result])
    def get_by_name(self, name: str):
        if self._data is not None :
            result = [fruit for fruit in self._data if fruit.get_name() == name]
        else:
            result = [fruit for fruit in FruitManager._data if fruit.get_name() == name]
        return FruitManager(result)
    def get_by_status(self, status: str):
        if self._data is not None :
            result = [fruit for fruit in self._data if fruit.get_status() == status]
        else:
            result = [fruit for fruit in FruitManager._data if fruit.get_status() == status]
        return FruitManager(result)
    def get_all(self):
        if self._data is not None :
            result = [fruit for fruit in self._data]
        else:
            result = [fruit for fruit in FruitManager._data]
        return FruitManager(result)
    def get_by_date(self, options: object):
        result = FruitManager([])
        operator = "=="
        
        if options.get("date") == None:
            return result
        
        date = datetime.strptime(options.get("date"), "%Y-%m-%d").date()

        operator_func = {
            "==": lambda x, y: x == y,
            "!=": lambda x, y: x != y,
            ">": lambda x, y: x > y,
            "<": lambda x, y: x < y,
            ">=": lambda x, y: x >= y,
            "<=": lambda x, y: x <= y,
        }

        if(options.get("operator") in operator_func):
                operator = options.get("operator")
        
        if self._data is not None:
            result = [fruit for fruit in self._data if operator_func[operator](datetime.strptime(fruit.get_date_add(), "%Y-%m-%d").date(), date)]
        else:
            result = [fruit for fruit in FruitManager._data if operator_func[operator](datetime.strptime(fruit.get_date_add(), "%Y-%m-%d").date(), date)]
        return FruitManager(result)
    def create_item(self, item: FruitItem):

        if item.get_id() and any(fruit.get_id() == item.get_id() for fruit in FruitManager._data):
            return None, error.RequestInvalidError

        FruitManager._data.append(item)

        return item.get_id(), None