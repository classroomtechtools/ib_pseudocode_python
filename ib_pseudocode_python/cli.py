"""

"""
import re
import os
import random  # for exec function
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

    def __init__(self, verbose):
        """
        """
        self.verbose = verbose
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
            '!=': '=='
        }.get(operator)
        return f"while {operand1} {inverse_operator} {operand2}:"

    def transpile(self, path: str = None, prepend_spec_code=True) -> str:
        """

        """

        with open(path) as source:
            # readin from source
            code = source.read()

            # replace comments: TODO What if "//"" in string?
            code = code.replace('//', "#")

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

            # change "loop while" to "while <inverse comparison>"
            code = re.sub(r'\bloop until (.*) ([=><]{1,2}) (.*)', self.inverse_while, code)

            # Python's range second param in non-inclusive, but IB spec is inclusive, so need extra handling here (hence the func)
            code = re.sub("loop ([A-Z]+) from ([0-9]+) to ([A-Z0-9-]+)", self.increment_second_range_param, code)

            # standardize cases; TODO: What if user enters falSe?
            code = re.sub(r"\bNOT\b", "not", code)
            code = re.sub(r'\bfalse\b', 'False', code)
            code = re.sub(r'\btrue\b', 'True', code)
            code = re.sub(r'\bmod\b', '%', code)
            code = re.sub(r'\bdiv\b', '/', code)

            if prepend_spec_code:
                with open(ib_specification_glue_code.__file__) as ib:
                    code = "".join(ib.readlines()) + '\n' + code

        return code

    def execute(self, the_string, **kwargs):
        exec(the_string, globals())


@form_group()
@add_option('-v', '--verbose', default=0, count=True, help="Help to debug your program, add more for more output")
@pass_pseudo
def cli(ctx, *args, **kwargs):
    ctx.obj = Transpiler(*args, **kwargs)


@cli.command('transpile')
@add_option('-p', '--path', default=None)
@pass_pseudo
def transpile(app, path):
    """
    Outputs Python code from pseudocode at path
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
    Read in all .pseudo files inside dir, joins them up, transpiles and executes
    """
    if directory is None:
        directory = os.getcwd()

    enclosing = pathlib.Path(directory)
    paths = list([str(e) for e in enclosing.glob("*.pseudo")])
    paths.sort()

    code = [app.obj.transpile(c, prepend_spec_code=i == 0) for i, c in enumerate(paths)]

    app.obj.execute("\n".join(code))
