from django.apps import AppConfig


class FrazzetobookreviewConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'frazzetoBookReview'

    def ready(self):
        import frazzetoBookReview.signals
