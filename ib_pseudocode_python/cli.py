"""

"""
import re
import os
import pathlib
import click

from ib_pseudocode_python import spec as ib_specification_glue_code

form_group = click.group
make_command = click.command
add_argument = click.argument
add_option = click.option
add_argument = click.argument
pass_pseudo = click.pass_context


class Screen:
    output_to_screen = staticmethod(click.echo)
    stylize_string = staticmethod(click.style)
    prompt_user = staticmethod(click.prompt)
    wait_for_any_key = staticmethod(click.pause)

    def echo_green(self, s, **kwargs):
        self.output_to_screen(self.stylize_string(s, fg='green'), **kwargs)

    def echo_yellow(self, s):
        self.output_to_screen(self.stylize_string(s, fg='yellow'))

    def echo_white(self, s):
        self.output_to_screen(self.stylize_string(s, fg='white'))

    def echo_red(self, s):
        self.output_to_screen(self.stylize_string(s, fg='red'))

    def styled_echo(self, s, **kwargs):
        self.output_to_screen(self.stylize_string(s, **kwargs))

    def stylized_echo(self, s, echo={}, style={}):
        self.output_to_screen(self.stylize_string(s, **style), **echo)

    def new_line(self):
        self.output_to_screen()

    def clear_screen(self):
        click.clear()

    def prompt(self, s, **kwargs):
        return self.prompt_user(s, **kwargs)

    def styled_prompt(self, s, style={}, prompt={}):
        return self.prompt_user(self.stylize_string(s, **style), **prompt)

    def pause(self, **kwargs):
        wait_for_any_key(**kwargs)


class Transpiler:
    """

    """

    def __init__(self):
        """
        """
        self.screen = Screen()

    @staticmethod
    def increment_second_range_param(match):
        groups = match.groups()
        if len(groups) != 3:
            raise("Something wicked this way comes")
        return f"for {groups[0]} in range({groups[1]}, {groups[2]}+1):"

    @staticmethod
    def inverse_while(match):
        operand1, operator, operand2 = match.groups()
        inverse_operator = {
            '>': '<=',
            '<': '>=',
            '<=': '>',
            '>=': '<',
            '=': '!=',
            '==': '!=',
            '!=': '==',
            '≠': '=='
        }.get(operator)
        return f"while {operand1} {inverse_operator} {operand2}:"

    def transpile(self, path: str = None, prepend_spec_code=False, announce=False) -> str:
        """

        """
        if path is None:
            path = pathlib.Path().cwd()


        with open(path) as source:
            # readin from source
            code = source.read()

            if announce:
                # output bold
                code = 'output "\033[1m' + '='*5 + pathlib.Path(path).name + '='*5 + '\033[0m"\n' + code

            # change tabs to four spaces
            code = re.sub(r'\t', "    ", code)

            # remove comments: TODO What if "//"" in string?
            code = re.sub('//.*', "", code)

            # change output keyword to output function (which is exec as print statement)
            code = re.sub(r"\boutput (.*)", r"output(\1)", code)

            # change comparison with one = to ==, keeping "then" (removed in next)
            code = re.sub("if (.*) +={1} +(.*) then", r"if \1 == \2 then", code)

            # change "else if" to "elif"
            code = re.sub(r'\belse if (.*) then', r"elif \1:", code)

            # add colon in else statements
            code = re.sub(r"\belse\b", r"else:", code)

            # change any if statements with "then"
            code = re.sub(r"\bif (.*) then", r"if \1:", code)

            # just remove any "end" statements
            code = re.sub(r"\bend .*", "", code)

            # change "loop while" to just "while"
            code = re.sub(r'\bloop while (.*)', r"while \1:", code)

            # change "loop until" to "while <inverse comparison>"
            code = re.sub(r'\bloop until (.*) ([=><]{1,2}) (.*)', self.inverse_while, code)

            # change loop until <expr>
            code = re.sub(r'\bloop until (.*)', r'while not \1:', code)

            # Python's range second param in non-inclusive, but IB spec is inclusive, so need extra handling here (hence the func)
            code = re.sub("loop ([A-Z]+) from ([0-9]+) to ([A-Z0-9-]+)", self.increment_second_range_param, code)

            # standardize cases; TODO: What if user enters falSe?
            code = re.sub(r"\b((NOT)|(AND)|(OR))\b", lambda m: m.group(1).lower(), code)
            code = re.sub(r'\bfalse\b', 'False', code)
            code = re.sub(r'\btrue\b', 'True', code)
            code = re.sub(r'\bmod\b', '%', code)
            code = re.sub(r'\bdiv\b', '/', code)

            if prepend_spec_code:
                # In case you want to manually add to top of file
                with open(ib_specification_glue_code.__file__) as ib:
                    code = ib.read() + '\n' + code
        return code

    def execute(self, the_string, **kwargs):
        hand_off_globals = {
            'List': ib_specification_glue_code.List,
            'Stack': ib_specification_glue_code.Stack,
            'Collection': ib_specification_glue_code.Collection,
            'output': ib_specification_glue_code.output,
            'Queue': ib_specification_glue_code.Queue,
        }
        exec(the_string, hand_off_globals)


class CliSort(click.Group):

    def list_commands(self, _):
        # only these ones
        return ['transpile', 'execute', 'run']


@form_group(cls=CliSort)
@pass_pseudo
def cli(app, *args, **kwargs):
    app.obj = Transpiler(*args, **kwargs)


@cli.command('interface', hidden=True)
@pass_pseudo
def interface(app):
    res = {}
    for command_name in cli.list_commands(app):
        cmd = cli.get_command(app, command_name)
        obj = {'help': cmd.help}
        obj['params'] = []
        for param in cmd.params:
            if type(param) == click.core.Option and param.required:
                obj['params'].append( (param.name, param.help) )
            elif type(param) == click.core.Command:
                obj['params'].append( (param.name, param.help) )
        res[command_name] = obj
    print(res)  # plainly print it for parsing : BLECHT


@cli.command('transpile')
@add_option('-p', '--path', required=True)
@pass_pseudo
def transpile(app, path):
    """
    Convert pseudocode at path and output
    """
    app.obj.screen.output_to_screen(app.obj.transpile(path))


@cli.command('execute')
@add_option('-p', '--path', default=None)
@pass_pseudo
def execute(app, *args, **kwargs):
    """
    Executes Python code from pseudocode at path
    """
    code = app.obj.transpile(*args, **kwargs)
    app.obj.execute(code)


@cli.command('run')
@add_option('-d', '--directory', default=None)
@pass_pseudo
def run(app, directory):
    """
    Concatenates in all .pseudo files, executes all
    """
    if directory is None:
        directory = os.getcwd()

    enclosing = pathlib.Path(directory)
    paths = list([str(e) for e in enclosing.glob("*.pseudo")])
    paths.sort()

    code = [app.obj.transpile(c, announce=True, prepend_spec_code=i == 0) for i, c in enumerate(paths)]

    app.obj.execute("\n".join(code))
