import sys
import os
import urllib
import xml.sax.saxutils

from paste.script import templates
from paste.script.templates import NoDefault

import utils

BOOTSTRAP = 'http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py'

class AlchemistProject(templates.Template):
    _template_dir = 'alchemist-template'
    summary = "An Alchemist Project"
    required_templates = []

    vars = [
        utils.ask_var('user', 'Name of an initial administrator user',
                default=NoDefault),
        utils.ask_var('db_uri', 'Database URI',
                default=NoDefault),
        utils.ask_var('passwd', 'Password for the initial administrator user',
                default=NoDefault, should_echo=False),
        utils.ask_var('newest', 'Check for newer versions of packages',
                default='false', should_ask=False,
                getter=utils.get_boolean_value_for_option),
        utils.ask_var('run_buildout',
                "After creating the project area, run the buildout.",
                default=True, should_ask=False,
                getter=utils.get_boolean_value_for_option),
        utils.ask_var('eggs_dir',
                'Location where zc.buildout will look for and place packages',
                default='', should_ask=False),
        ]

    def check_vars(self, vars, cmd):
        if vars['package'] in ('grok', 'zope'):
            print
            print "Error: The chosen project name results in an invalid " \
                  "package name: %s." % vars['package']
            print "Please choose a different project name."
            sys.exit(1)

        explicit_eggs_dir = vars.get('eggs_dir')

        skipped_vars = {}
        for var in list(self.vars):
            if not var.should_ask:
                skipped_vars[var.name] = var.getter(vars, var)
                self.vars.remove(var)

        vars = super(AlchemistProject, self).check_vars(vars, cmd)
        for name in skipped_vars:
            vars[name] = skipped_vars[name]

        for var_name in ['user', 'passwd']:
            # Escape values that go in site.zcml.
            vars[var_name] = xml.sax.saxutils.quoteattr(vars[var_name])
        vars['app_class_name'] = vars['project'].capitalize()

        # Handling the bootstrap.py file.
        bootstrap_contents = urllib.urlopen(BOOTSTRAP).read()
        vars['bootstrap_contents'] = bootstrap_contents

        buildout_default = utils.exist_buildout_default_file()
        if explicit_eggs_dir:
            # Put explicit_eggs_dir in the vars; used by the post command.
            vars['explicit_eggs_dir'] = explicit_eggs_dir
            vars['eggs_dir'] = (
                '# Warning: when you share this buildout.cfg with friends\n'
                '# please remove the eggs-directory line as it is hardcoded.\n'
                'eggs-directory = %s') % explicit_eggs_dir
        elif buildout_default:
            vars['eggs-dir'] = ''
        else:
            utils.create_buildout_default_file()

        return vars

    def post(self, command, output_dir, vars):
        if not vars['run_buildout']:
            return
        os.chdir(vars['project'])
        eggs_dir = vars.get('explicit_eggs_dir',
                            utils.get_buildout_default_eggs_dir())
        if not os.path.isdir(eggs_dir):
            os.mkdir(eggs_dir)

        utils.run_buildout(command.options.verbose)
