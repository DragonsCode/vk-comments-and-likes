from .group_msg import group_msg_labeler
from .admin import admin_labeler
# Если использовать глобальный лейблер, то все хендлеры будут зарегистрированы в том же порядке, в котором они были импортированы

__all__ = ("group_msg_labeler", "admin_labeler")