# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Envio.codigo_archivo'
        db.alter_column(u'evaluador_envio', 'codigo_archivo', self.gf('django.db.models.fields.CharField')(max_length=140))

    def backwards(self, orm):

        # Changing field 'Envio.codigo_archivo'
        db.alter_column(u'evaluador_envio', 'codigo_archivo', self.gf('django.db.models.fields.FilePathField')(path='/home/abraham/Desarrollo/django/KarelapanDjango/codigos', max_length=100))

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
        u'evaluador.concurso': {
            'Meta': {'ordering': "['-fecha_inicio']", 'object_name': 'Concurso'},
            'activo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'administradores': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['usuarios.Grupo']"}),
            'autor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'concursos'", 'to': u"orm['auth.User']"}),
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'duracion_preguntas': ('django.db.models.fields.IntegerField', [], {'default': '90'}),
            'fecha_fin': ('django.db.models.fields.DateTimeField', [], {}),
            'fecha_inicio': ('django.db.models.fields.DateTimeField', [], {}),
            'grupos': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'+'", 'symmetrical': 'False', 'to': u"orm['usuarios.Grupo']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'problemas': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['evaluador.Problema']", 'symmetrical': 'False'}),
            'ranking_publico': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'evaluador.consideracion': {
            'Meta': {'object_name': 'Consideracion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'problema': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'consideraciones'", 'to': u"orm['evaluador.Problema']"}),
            'texto': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        },
        u'evaluador.consulta': {
            'Meta': {'ordering': "['-hora']", 'object_name': 'Consulta'},
            'concurso': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'consultas'", 'to': u"orm['evaluador.Concurso']"}),
            'descartado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hora': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'leido': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mensaje': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'problema': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'consultas'", 'to': u"orm['evaluador.Problema']"}),
            'respuesta': ('django.db.models.fields.TextField', [], {}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'consultas'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'evaluador.envio': {
            'Meta': {'ordering': "['-hora']", 'object_name': 'Envio'},
            'casos': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'codigo': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'codigo_archivo': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'concurso': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'envios'", 'null': 'True', 'to': u"orm['evaluador.Concurso']"}),
            'estatus': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1'}),
            'hora': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'default': "'0.0.0.0'", 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'mensaje': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'problema': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['evaluador.Problema']"}),
            'puntaje': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'resultado': ('django.db.models.fields.CharField', [], {'default': "'OK'", 'max_length': '17'}),
            'tiempo_ejecucion': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'envios'", 'to': u"orm['auth.User']"})
        },
        u'evaluador.nivel': {
            'Meta': {'ordering': "['nivel']", 'object_name': 'Nivel'},
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nivel': ('django.db.models.fields.IntegerField', [], {}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'evaluador.participacion': {
            'Meta': {'unique_together': "(('usuario', 'concurso'),)", 'object_name': 'Participacion'},
            'concurso': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'participaciones'", 'to': u"orm['evaluador.Concurso']"}),
            'hora_entrada': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'primera_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'puntaje': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'participaciones'", 'to': u"orm['auth.User']"})
        },
        u'evaluador.problema': {
            'Meta': {'object_name': 'Problema'},
            'agradecimiento': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'autor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'casos_de_evaluacion': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'descripcion': ('tinymce.models.HTMLField', [], {}),
            'fecha_publicacion': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'futuro': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limite_ejecucion': ('django.db.models.fields.IntegerField', [], {'default': '200000'}),
            'limite_iteracion': ('django.db.models.fields.IntegerField', [], {'default': '65000'}),
            'limite_recursion': ('django.db.models.fields.IntegerField', [], {'default': '65000'}),
            'logica_fuerte': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mejor_tiempo': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'mundo': ('django.db.models.fields.TextField', [], {}),
            'mundo_resuelto': ('django.db.models.fields.TextField', [], {}),
            'nivel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['evaluador.Nivel']"}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '140'}),
            'nombre_administrativo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '140'}),
            'problema': ('tinymce.models.HTMLField', [], {}),
            'publico': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'veces_intentado': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'veces_resuelto': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'usuarios.grupo': {
            'Meta': {'object_name': 'Grupo'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '240'}),
            'elegible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['evaluador']