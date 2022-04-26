from ipykernel.kernelbase import Kernel

# TODO: Inject version in one place only
__version__ = '0.0.0'

class KKernel(Kernel):
    implementation = 'k'
    implementation_version = __version__
    language = 'k'
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
        if not silent:
            stream_content = {'name': 'stdout', 'text': code}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }
