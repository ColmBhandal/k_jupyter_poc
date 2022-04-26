from ipykernel.kernelbase import Kernel
import subprocess
import re
import tempfile
import os

# TODO: Inject version in one place only
__version__ = '0.0.0'

k_code_pattern = re.compile("^//k")

def kompile_and_run(k_buffer, code):
    with tempfile.TemporaryDirectory() as tmpdirname:
        os.chmod(tmpdirname, 0o755) # Starts off as 700, not user readable
    return "K: " + "\n".join(k_buffer) + "\nCode: " + code

class KKernel(Kernel):

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self._k_buffer = []

    implementation = 'k'
    implementation_version = __version__
    language = 'k'
    # TODO: Get the actual K language version somehow and inject it here, or at least hardwire the version being used
    language_version = '0.0.0'
    banner = "K kernel.\n" \
             '''Incrementally build a K-definition via multiple k-fragments and then run these with krun.
                All parts of your K-definition should being with the comment "//k". All other cells will be treated as sh commands.
             '''

    @property
    def language_info(self):
        return {
            'name': 'K',
            'mimetype': 'text/x-k',
            'file_extension': '.k',
            'version': self.language_version
        }

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if re.match(k_code_pattern, code):
            self._k_buffer.append(code)
            message = 'K code fragment buffered.\n'
        else:
            message = kompile_and_run(self._k_buffer, code)
        if not silent:
            message += subprocess.run(['kompile', '--version'], check=True, capture_output=True, text=True).stdout
            stream_content = {'name': 'stdout', 'text': message}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }
