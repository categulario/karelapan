# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Perfil.nombre_completo'
        db.add_column(u'usuarios_perfil', 'nombre_completo',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Perfil.nombre_completo'
        db.delete_column(u'usuarios_perfil', 'nombre_completo')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'usuarios.grupo': {
            'Meta': {'object_name': 'Grupo'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '240'}),
            'elegible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'usuarios.olimpiada': {
            'Meta': {'ordering': "['anio']", 'object_name': 'Olimpiada'},
            'anio': ('django.db.models.fields.IntegerField', [], {'default': '2013'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sede': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'})
        },
        u'usuarios.perfil': {
            'Meta': {'object_name': 'Perfil'},
            'apmat': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'appat': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'asesor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'asesorados'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'confirm_token': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'estado': ('django.db.models.fields.CharField', [], {'default': "'veracruz'", 'max_length': '25'}),
            'fecha_nacimiento': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'grado_actual': ('django.db.models.fields.CharField', [], {'default': "'2 bachillerato'", 'max_length': '20'}),
            'grupos': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['usuarios.Grupo']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nivel_estudios': ('django.db.models.fields.CharField', [], {'default': "'secundaria'", 'max_length': '20'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'nombre_completo': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'nombre_escuela': ('django.db.models.fields.CharField', [], {'max_length': "'140'", 'blank': 'True'}),
            'problemas_resueltos': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'puntaje': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sexo': ('django.db.models.fields.CharField', [], {'default': "'M'", 'max_length': '1'}),
            'subsistema': ('django.db.models.fields.CharField', [], {'default': "'OTROS'", 'max_length': '20'}),
            'ultima_omi': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['usuarios.Olimpiada']"}),
            'usuario': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['usuarios']