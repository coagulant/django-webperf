from django import template

register = template.Library()

class GlobalVariable(object):
    def __init__(self, varname, varval):
        self.varname = varname
        self.varval = varval.strip()

    def name(self):
        return self.varname

    def value(self):
        return self.varval

    def push(self, newval):
        self.varval = self.varval.strip() + newval.strip()


@register.tag(name='collect_assets')
def do_collect_assets(parser, token):
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("'collect_assets' node requires a variable name.")
    nodelist = parser.parse(('endcollect_assets',))
    parser.delete_first_token()
    return CollectAssetsNode(nodelist, args)

class CollectAssetsNode(template.Node):
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        gv = context.get(self.varname, None)
        output = self.nodelist.render(context)
        if gv:
            gv.push(output)
        else:
            gv = context[self.varname] = GlobalVariable(self.varname, output)
        return ''


@register.tag(name='get_assets')
def getglobal(parser, token):
    try:
        tag_name, varname = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires arguments" % token.contents.split()[0])
    return GlobalVariableGetNode(varname)


class GlobalVariableGetNode(template.Node):
    def __init__(self, varname):
        self.varname = varname

    def render(self, context):
        try:
            return context[self.varname].value()
        except AttributeError:
            return ''
