class DataBase:
    def __init__(self):
        raise NotImplementedError("Инициализация не переопределена!")
    def get(self):
        raise NotImplementedError("Метод get не переопределен!")    

    def exists_in_database(self):
        raise NotImplementedError("Метод exists_in_database не переопределен!")    
 
    def associate_url_with_cache_key(self):
        raise NotImplementedError("Метод associate_url_with_cache_key не переопределен!")    

    def get_cache_key_for_url(self):
        raise NotImplementedError("Метод get_cache_key_for_url не переопределен!")                   
    def delete_cache_for_url(self):
        raise NotImplementedError("Метод delete_cache_for_url не переопределен!")    
    def set(self):
        raise NotImplementedError("Метод set не переопределен!")    
    def clear(self):
        raise NotImplementedError("Метод clear не переопределен!")            
