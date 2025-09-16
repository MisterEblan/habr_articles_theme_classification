class Singleton(object):
    """Паттерн Singleton для предиктора

    Нужен, чтобы не загружать модель каждый раз.
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance
