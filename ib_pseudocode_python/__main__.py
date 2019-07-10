from ipykernel.kernelbase import Kernel
from ib_pseudocode_python.cli import Transpiler

import sys
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


class PseudocodeKernel(Kernel):
    implementation = 'IB_Pseudocode'
    implementation_version = '0.5'
    language_version = '0.1'
    language_info = {'name': 'ib_pseudocode_python', 'file_extension': '.pseudo', 'mimetype': 'text/python'}
    banner = "IB PseudoCode kernel - tranpiles to Python and executes"
    transpiler = Transpiler()
    collected_code = []

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        pseudo_code_stream = StringIO(code)
        pseudocode, code = self.transpiler.transpile(pseudo_code_stream)
        result, error = self.transpiler.execute_and_capture(code, pseudocode)

        if not silent:
            stream_content = {'name': 'stdout', 'text': result}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }

from IPython.core.magic import cell_magic, magics_class, Magics
from IPython import get_ipython

@magics_class
class PseudocodeMagics(Magics):
    @cell_magic
    def transpile(line='', cell=None):
        transpiler = Transpiler()
        pseudocode, code = transpiler.transpile(cell)
        return psuedocode

def load_ipython_extension(ipython):
    print("here")
    ipython.register_magics(PseudocodeMagics)

from ipykernel.kernelapp import IPKernelApp
IPKernelApp.launch_instance(kernel_class=PseudocodeKernel)

