from django.db.models.signals import post_save, pre_save
from django.contrib import auth
from apps.usuarios.models import Perfil, Grupo

def crea_perfil(sender, instance, created, raw, using, update_fields, **kwargs):
    """Crea el perfil relacionado al crearse un nuevo usuario"""
    if created:
        nuevo_perfil = Perfil(
            usuario   = instance,
        )
        nuevo_perfil.save()

def prepara_perfil(sender, instance, raw, using, **kwargs):
    """Prepara un perfil para ser guardado"""
    instance.nombre_completo = "%s %s %s"%(instance.nombre, instance.appat, instance.apmat)

def add_default_group(sender, instance, created, raw, using, update_fields, **kwargs):
    """Add the 'users' group to this profile"""
    if created:
        instance.grupos.add(Grupo.objects.get_or_create(nombre='usuarios')[0])

post_save.connect(crea_perfil, sender = auth.get_user_model())
post_save.connect(add_default_group, sender = Perfil)
pre_save.connect(prepara_perfil, sender = Perfil)
