"""

"""
import re
import os
import pathlib
import click
import traceback
import sys
from io import StringIO
import contextlib

from ib_pseudocode_python import spec as ib_specification_glue_code

form_group = click.group
make_command = click.command
add_argument = click.argument
add_option = click.option
add_argument = click.argument
pass_pseudo = click.pass_context

on_repl = pathlib.Path('/home/runner/.local/').exists()

from io import StringIO
import contextlib

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old



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
    def if_statement(match):
        return re.sub(r'={1}', r'==', match.group(0))

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

    def transpile(self, file, prepend_spec_code=False) -> str:
        """

        """
        try:
            path = pathlib.Path(file)

            if not path.exists():
                path = path.with_suffix('.pseudo')

            if not path.exists():
                raise FileNotFoundError(f"You need to create a file called {path}")

            with open(path) as source:
                # readin from source
                pseudocode = source.read()

        except TypeError:
            # probably a StringIO or file object
            pseudocode = file.read()

        code = pseudocode[:]  # copy

        # change tabs to four spaces
        code = code.replace(r'\t', "    ")

        # remove comments: TODO What if "//"" in string?
        code = re.sub(r'//.*', '', code)

        # change output keyword to output function (which is exec as print statement)
        code = re.sub(r"\boutput (.*)", r"output(\1)", code)

        # change comparison with one = to ==, keeping "then" (removed in next)
        code = re.sub("if (.*) ={1} (.*)", self.if_statement, code)

        # change "else if" to "elif"
        code = re.sub(r'\belse if (.*) then', r"elif \1:", code)

        # add colon in else statements
        code = re.sub(r"\belse\b", r"else:", code)

        # change any if statements with "then"
        code = re.sub(r"\bif (.*) then", r"if \1:", code)

        # just remove any "end" statements
        code = re.sub(r"\bend .*", "", code)

        # change loop with single = to ==
        code = re.sub(r'\bloop\b.*', self.if_statement, code)

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
        return pseudocode, code

    def execute_and_capture(self, code, pseudocode, **kwargs):
        """
        Execute code but capture stdout and return that
        """
        with stdoutIO() as captured:
            error = self.execute(code, pseudocode, **kwargs)
        return captured.getvalue(), error

    def execute(self, code, pseudocode, lineoffset=0):
        """
        Executes and outputs results to stdout
        return true if error occurred and false if not
        """
        ret = False
        hand_off_globals = {
            'Array': ib_specification_glue_code.Array,
            'Stack': ib_specification_glue_code.Stack,
            'Collection': ib_specification_glue_code.Collection,
            'output': ib_specification_glue_code.output,
            'Queue': ib_specification_glue_code.Queue,
        }

        try:
            exec(code, hand_off_globals)

        except SyntaxError as err:
            ret = True
            pseudocode_lines = pseudocode.split('\n')
            code_lines = code.split('\n')

            error_class = err.__class__.__name__
            detail = err.args[0]
            line_number = err.lineno
            pseudo_line = pseudocode_lines[line_number-1].strip()
            transpiled_line = code_lines[line_number-1].strip()

            # determine some common sytnax errors
            if re.match(r'\b(while)|(until)\b', pseudo_line) and not re.match(r'\bloop\b', pseudo_line):
                detail = "'loop' keyword expected, but not found"
            if pseudo_line.lstrip().startswith('if ') and not pseudo_line.rstrip().endswith('then'):
                detail = "'then' expected to end if statement, but not found"
            if transpiled_line.rstrip().endswith('::'):
                detail = "extra ':' found"

            self.screen.output_to_screen(
                self.screen.stylize_string(
                    f"Programming error on line {err.lineno+lineoffset}:",
                    fg='red')
            )
            self.screen.output_to_screen(
                '\t' + self.screen.stylize_string(
                    pseudo_line,
                    fg="green"
                ) + " (pseudocode)"
            )
            self.screen.output_to_screen(
                '\t' + self.screen.stylize_string(
                    transpiled_line,
                    fg="yellow"
                ) + " (python)"
            )
            self.screen.output_to_screen(
                self.screen.stylize_string(
                    f"{error_class}: {detail}",
                    fg='red'
                )
            )

        except Exception as err:
            ret = True
            pseudocode_lines = pseudocode.split('\n')
            code_lines = code.split('\n')

            error_class = err.__class__.__name__
            detail = err.args[0]
            cl, exc, tb = sys.exc_info()

            line_number = traceback.extract_tb(tb)[-1][1]
            pseudo_line = pseudocode_lines[line_number-1].strip()
            transpiled_line = code_lines[line_number-1].strip()

            click.echo(click.style(f"Execution error on line {line_number+lineoffset}:", fg='red'))
            click.echo('\t' + click.style(pseudo_line, fg="green") + " (pseudocode)")
            click.echo('\t' + click.style(transpiled_line, fg="yellow") + " (python)")
            click.echo(click.style(f"{error_class}: {detail}", fg='red'))

        return ret

class CliGroup(click.Group):

    def list_commands(self, _):
        # only these ones
        return ['transpile', 'execute', 'run']


class CliGroupRepl(CliGroup):

    def collect_usage_pieces(self, ctx):
        more = super().collect_usage_pieces(ctx)
        return ['\b' * len('pseudo  '), "cli('pseudo"] + more + ["')"]


@form_group(cls=CliGroupRepl if on_repl else CliGroup)
@pass_pseudo
def cli(app, *args, **kwargs):
    app.obj = Transpiler(*args, **kwargs)


class CliCommandRepl(click.Command):

    def collect_usage_pieces(self, ctx):
        more = super().collect_usage_pieces(ctx)
        return ['\b' * (len('psuedo  ') + len(ctx.command.name + ' ')), "cli('pseudo " + ctx.command.name] + more + ["')"]


@cli.command('interface', cls=CliCommandRepl if on_repl else None, hidden=True)
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


@cli.command('transpile', cls=CliCommandRepl if on_repl else None)
@add_argument('file')
@pass_pseudo
def transpile(app, file):
    """
    Convert pseudocode in file and output
    """
    _, code = app.obj.transpile(file)
    app.obj.screen.output_to_screen(code)


@cli.command('execute', cls=CliCommandRepl if on_repl else None)
@add_argument('file', default=None)
@pass_pseudo
def execute(app, *args, file=None, **kwargs):
    """
    Executes Python code from pseudocode in file
    """
    pseudocode, code = app.obj.transpile(*args, file=file, **kwargs)
    app.obj.execute(code, pseudocode)


@cli.command('capture', cls=CliCommandRepl if on_repl else None)
@add_argument('file', default=None)
@pass_pseudo
def capture(app, *args, file=None, **kwargs):
    pseudocode, code = app.obj.transpile(*args, file=file, **kwargs)
    result = app.obj.execute_and_capture(code, pseudocode)


@cli.command('run', cls=CliCommandRepl if on_repl else None)
@add_option('-d', '--directory', default=None)
@pass_pseudo
def run(app, directory):
    """
    Executes all, one by one
    """
    if directory is None:
        directory = os.getcwd()

    enclosing = pathlib.Path(directory)
    paths = list([str(e) for e in enclosing.glob("*.pseudo")])
    paths.sort()

    for i, c in enumerate(paths):
        click.secho("=" * 5 + c.split("/")[-1] + "="*5, fg="green")
        app.invoke(
            execute,
            file=c
        )
