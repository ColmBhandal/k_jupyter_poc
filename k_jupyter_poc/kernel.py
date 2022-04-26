from ipykernel.kernelbase import Kernel
import subprocess
import re

# TODO: Inject version in one place only
__version__ = '0.0.0'

k_code_pattern = re.compile("(?s).*module(?s).*endmodule(?s).*")

class KKernel(Kernel):
    implementation = 'k'
    implementation_version = __version__
    language = 'k'
    # TODO: Get the actual K language version somehow and inject it here, or at least hardwire the version being used
    language_version = '0.0.0'
    banner = "K kernel.\n" \
             "Saves K modules in the background and allows them to be Kompiled / KRun"

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
        message = 'No k code detected\n'
        if re.match(k_code_pattern, code):
            message = 'K code detected\n'
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
