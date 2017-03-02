from django.apps import AppConfig


class OthConfig(AppConfig):
    name = 'enigma.oth'
    verbose_name = "Oth"

    def ready(self):
        import enigma.oth.signals
