# -*- coding: utf-8 -*-
from django import template

register = template.Library()

def form_inline(parser, token):
    """
    {% form_inline formulario %}
    """
    try:
        tag_name, formulario = token.split_contents()
    except:
        raise template.TemplateSyntaxError, "%r tag requires exactly two argument" % token.contents.split()[0]
    return FormInlineObject(formulario)

def form_horizontal(parser, token):
    """
    {% form_inline formulario %}
    """
    try:
        tag_name, formulario = token.split_contents()
    except:
        raise template.TemplateSyntaxError, "%r tag requires exactly two argument" % token.contents.split()[0]
    return FormHorizontalObject(formulario)

def form_br(parser, token):
    """
    {% form_br formulario %}
    """
    try:
        tag_name, formulario = token.split_contents()
    except:
        raise template.TemplateSyntaxError, "%r tag requires exactly two argument" % token.contents.split()[0]
    return FormBrObject(formulario)

class FormInlineObject(template.Node):
    def __init__(self, formulario):
        self.formulario = formulario

    def render(self, context):
        salida = ''
        script = '''
        <script type="text/javascript" language="javascript">
        '''
        for elemento in context[self.formulario]:
            salida += elemento.as_widget()+'\n'
            script += '$("input[name=\''+elemento.html_name+'\'], select[name=\''+elemento.html_name+'\']").addClass("input-small");\n'
            script += '$("input[name=\''+elemento.html_name+'\']").attr("placeholder", "'+elemento.label+'");\n'
        script += '</script>'
        return salida+script


class FormHorizontalObject(template.Node):
    def __init__(self, formulario):
        self.formulario = formulario

    def render(self, context):
        salida = ''
        for elemento in context[self.formulario]:
            salida += '''
            <div class="control-group">
                <label class="control-label" for="'''+elemento.auto_id+'''" id="'''+elemento.html_name+'''_label">'''+elemento.label+'''</label>
                <div class="controls">
                  '''+elemento.as_widget()

            if elemento.errors:
                salida += '<ul class="unstyled errorlist">'
                for error in elemento.errors:
                  salida += '<li>'+error+'</li>'
                salida += '</ul>'
            salida += '</div></div>'
        return salida

class FormBrObject(template.Node):
    def __init__(self, formulario):
        self.formulario = formulario

    def render(self, context):
        salida = ''
        for elemento in context[self.formulario]:
            salida += elemento.label+'<br>'+elemento.as_widget()+'<br>'

            if elemento.errors:
                salida += '<ul class="unstyled errorlist">'
                for error in elemento.errors:
                  salida += '<li>'+error+'</li>'
                salida += '</ul>'
        return salida

@register.simple_tag
def progressbar(valor, valor_maximo):
    print valor, valor_maximo
    print type(valor), type(valor_maximo)
    if valor == valor_maximo:
        tipo = 'success'
    elif valor/float(valor_maximo) > .66:
        tipo = 'info'
    elif valor/float(valor_maximo) > .33:
        tipo = 'warning'
    else:
        tipo = 'danger'
    div = int(valor*100/float(valor_maximo))
    return '<div class="progress progress-'+tipo+' progress-striped active" data-title="'+str(valor)+' puntos de '+str(valor_maximo)+' en total"><div class="bar" style="width: '+str(div)+'%"></div></div>'

register.tag('form_inline', form_inline)
register.tag('form_horizontal', form_horizontal)
register.tag('form_br', form_br)
