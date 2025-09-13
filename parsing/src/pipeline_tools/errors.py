class LinksNotFound(Exception):
    """Исключение, вызываемое, когда на
    странице не найжено ссылок"""
    pass

class LinkTagError(Exception):
    """Исключение, вызываемое, когда на странице ленты
    не найдено тегов ссылок"""
    pass

class EmptyBodyError(Exception):
    pass

class HubNotFound(Exception):
    pass

class InvalidUrlError(Exception):
    pass

class ZeroOffsetError(Exception):
    pass
