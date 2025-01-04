from __future__ import absolute_import, unicode_literals

# این خط باعث می‌شود Celery با Django کار کند
from .celery import app as celery_app

__all__ = ['celery_app']
