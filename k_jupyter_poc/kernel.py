from ipykernel.kernelbase import Kernel
from datetime import datetime
import subprocess
import re
import tempfile
import os
import shlex

# TODO: Inject version in one place only
__version__ = '0.0.0'

kompile_pattern = re.compile(r"^kompile\s*([\-\w\d]+\.\w+)")
command_pattern = re.compile("^(krun|kparse)")

class KKernel(Kernel):

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self._k_buffer = []
        self._workdir = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        os.mkdir(self._workdir)

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
        if re.match(command_pattern, code):
            self.maybe_send_simple_message("Running command...\n", silent)
            message = self._run_command(code).stdout
        elif match := re.search(kompile_pattern, code):
            self.maybe_send_simple_message("Kompiling code...\n", silent)
            k_def = "\n".join(self._k_buffer)
            # We've already done the work of joining - so store the joined string in the buffer
            self._k_buffer = [k_def]
            k_filename = match.group(1)
            with open(os.path.join(self._workdir, k_filename), 'w') as k_file:
                k_file.write(k_def)
            result = self._run_command(code)
            ret_code = result.returncode
            output = result.stdout
            if(ret_code != 0):
                message = f"ERROR. Kompile failed. Exit code: {ret_code}"
            else:
                message = "Kompile complete."
            if(output.strip()):
                message += "\n" + output
        else:
            self._k_buffer.append(code)
            message = 'K code fragment buffered.\n'

        self.maybe_send_simple_message(message, silent)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }

    def maybe_send_simple_message(self, message, silent):
        if not silent:
            stream_content = {'name': 'stdout', 'text': message}
            self.send_response(self.iopub_socket, 'stream', stream_content)

    def _run_command(self, k_command):
        return subprocess.run(shlex.split(k_command), check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=self._workdir)
