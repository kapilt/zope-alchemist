

from zope.app.pagetemplate import ViewPageTemplateFile
from zope.formlib import namedtemplate


FormTemplate = namedtemplate.NamedTemplateImplementation(
    ViewPageTemplateFile('templates/form.pt')
    )

SubFormTemplate = namedtemplate.NamedTemplateImplementation(
    ViewPageTemplateFile('templates/subform.pt')
    )
