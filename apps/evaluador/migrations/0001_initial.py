# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Nivel'
        db.create_table(u'evaluador_nivel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('descripcion', self.gf('django.db.models.fields.TextField')()),
            ('nivel', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'evaluador', ['Nivel'])

        # Adding model 'Problema'
        db.create_table(u'evaluador_problema', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=140)),
            ('nombre_administrativo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=140)),
            ('descripcion', self.gf('tinymce.models.HTMLField')()),
            ('problema', self.gf('tinymce.models.HTMLField')()),
            ('agradecimiento', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('veces_resuelto', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('veces_intentado', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('mejor_tiempo', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('mejor_puntaje', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('autor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('fecha_publicacion', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('nivel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['evaluador.Nivel'])),
            ('publico', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('futuro', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('logica_fuerte', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('limite_recursion', self.gf('django.db.models.fields.IntegerField')(default=65000)),
            ('limite_iteracion', self.gf('django.db.models.fields.IntegerField')(default=65000)),
            ('limite_ejecucion', self.gf('django.db.models.fields.IntegerField')(default=200000)),
            ('mundo', self.gf('django.db.models.fields.TextField')()),
            ('mundo_resuelto', self.gf('django.db.models.fields.TextField')()),
            ('casos_de_evaluacion', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'evaluador', ['Problema'])

        # Adding model 'Consideracion'
        db.create_table(u'evaluador_consideracion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('problema', self.gf('django.db.models.fields.related.ForeignKey')(related_name='consideraciones', to=orm['evaluador.Problema'])),
            ('texto', self.gf('django.db.models.fields.CharField')(max_length=254)),
        ))
        db.send_create_signal(u'evaluador', ['Consideracion'])

        # Adding model 'Concurso'
        db.create_table(u'evaluador_concurso', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fecha_inicio', self.gf('django.db.models.fields.DateTimeField')()),
            ('fecha_fin', self.gf('django.db.models.fields.DateTimeField')()),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('descripcion', self.gf('django.db.models.fields.TextField')()),
            ('activo', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('autor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='concursos', to=orm['auth.User'])),
            ('administradores', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['usuarios.Grupo'])),
            ('duracion_preguntas', self.gf('django.db.models.fields.IntegerField')(default=90)),
            ('ranking_publico', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'evaluador', ['Concurso'])

        # Adding M2M table for field problemas on 'Concurso'
        m2m_table_name = db.shorten_name(u'evaluador_concurso_problemas')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('concurso', models.ForeignKey(orm[u'evaluador.concurso'], null=False)),
            ('problema', models.ForeignKey(orm[u'evaluador.problema'], null=False))
        ))
        db.create_unique(m2m_table_name, ['concurso_id', 'problema_id'])

        # Adding M2M table for field grupos on 'Concurso'
        m2m_table_name = db.shorten_name(u'evaluador_concurso_grupos')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('concurso', models.ForeignKey(orm[u'evaluador.concurso'], null=False)),
            ('grupo', models.ForeignKey(orm[u'usuarios.grupo'], null=False))
        ))
        db.create_unique(m2m_table_name, ['concurso_id', 'grupo_id'])

        # Adding model 'Participacion'
        db.create_table(u'evaluador_participacion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(related_name='participaciones', to=orm['auth.User'])),
            ('concurso', self.gf('django.db.models.fields.related.ForeignKey')(related_name='participaciones', to=orm['evaluador.Concurso'])),
            ('puntaje', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hora_entrada', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('primera_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
        ))
        db.send_create_signal(u'evaluador', ['Participacion'])

        # Adding unique constraint on 'Participacion', fields ['usuario', 'concurso']
        db.create_unique(u'evaluador_participacion', ['usuario_id', 'concurso_id'])

        # Adding model 'Envio'
        db.create_table(u'evaluador_envio', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(related_name='envios', to=orm['auth.User'])),
            ('problema', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['evaluador.Problema'])),
            ('hora', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('estatus', self.gf('django.db.models.fields.CharField')(default='P', max_length=1)),
            ('puntaje', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('codigo', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('codigo_archivo', self.gf('django.db.models.fields.FilePathField')(path='/home/abraham/Desarrollo/django/KarelapanDjango/codigos', max_length=100)),
            ('tiempo_ejecucion', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('resultado', self.gf('django.db.models.fields.CharField')(default='OK', max_length=17)),
            ('mensaje', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('concurso', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='envios', null=True, to=orm['evaluador.Concurso'])),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(default='0.0.0.0', max_length=15, null=True, blank=True)),
            ('casos', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'evaluador', ['Envio'])

        # Adding model 'Consulta'
        db.create_table(u'evaluador_consulta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('concurso', self.gf('django.db.models.fields.related.ForeignKey')(related_name='consultas', to=orm['evaluador.Concurso'])),
            ('problema', self.gf('django.db.models.fields.related.ForeignKey')(related_name='consultas', to=orm['evaluador.Problema'])),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(related_name='consultas', null=True, to=orm['auth.User'])),
            ('mensaje', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('respuesta', self.gf('django.db.models.fields.TextField')()),
            ('leido', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('descartado', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hora', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
        ))
        db.send_create_signal(u'evaluador', ['Consulta'])


    def backwards(self, orm):
        # Removing unique constraint on 'Participacion', fields ['usuario', 'concurso']
        db.delete_unique(u'evaluador_participacion', ['usuario_id', 'concurso_id'])

        # Deleting model 'Nivel'
        db.delete_table(u'evaluador_nivel')

        # Deleting model 'Problema'
        db.delete_table(u'evaluador_problema')

        # Deleting model 'Consideracion'
        db.delete_table(u'evaluador_consideracion')

        # Deleting model 'Concurso'
        db.delete_table(u'evaluador_concurso')

        # Removing M2M table for field problemas on 'Concurso'
        db.delete_table(db.shorten_name(u'evaluador_concurso_problemas'))

        # Removing M2M table for field grupos on 'Concurso'
        db.delete_table(db.shorten_name(u'evaluador_concurso_grupos'))

        # Deleting model 'Participacion'
        db.delete_table(u'evaluador_participacion')

        # Deleting model 'Envio'
        db.delete_table(u'evaluador_envio')

        # Deleting model 'Consulta'
        db.delete_table(u'evaluador_consulta')


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
            'codigo_archivo': ('django.db.models.fields.FilePathField', [], {'path': "'/home/abraham/Desarrollo/django/KarelapanDjango/codigos'", 'max_length': '100'}),
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
            'mejor_puntaje': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
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