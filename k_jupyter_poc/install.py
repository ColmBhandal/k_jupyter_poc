import json
import os
import sys
import argparse

from jupyter_client.kernelspec import KernelSpecManager
from IPython.utils.tempdir import TemporaryDirectory

kernel_json = {
    "argv": [
        "python3",
        "-m",
        "jupyter_k_kernel",
        "-f",
        "{connection_file}"
    ],
    "display_name": "K",
    "language": "k"
}


def install_K_kernel_spec(user=True, prefix=None):
    with TemporaryDirectory() as tempDir:
        os.chmod(tempDir, 0o755)  # Need to make the file user-readable
        with open(os.path.join(tempDir, 'kernel.json'), 'w') as jsonFile:
            json.dump(kernel_json, jsonFile, sort_keys=True)        

        print('Installing the K IPython kernel')
        KernelSpecManager().install_kernel_spec(tempDir, 'k', user=user, replace=True, prefix=prefix)


def _is_root():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False  # This could happen if the platform is non-Unix. In any case, assume non-root.


def main(argv=[]):
    parser = argparse.ArgumentParser(
        description='Install KernelSpec for K Kernel'
    )
	
	# Ensure that only 1 installation location is specifies
    locationsGroup = parser.add_mutually_exclusive_group()

    locationsGroup.add_argument(
        '--user',
        help='Install KernelSpec in user homedirectory',
        action='store_true'
    )
    locationsGroup.add_argument(
        '--sys-prefix',
        help='Install KernelSpec in sys.prefix. Useful in conda / virtualenv',
        action='store_true',
        dest='sys_prefix'
    )
    locationsGroup.add_argument(
        '--prefix',
        help='Install KernelSpec in this prefix',
        default=None
    )

    args = parser.parse_args(argv)

    if args.sys_prefix:
        prefix = sys.prefix
        user = None
    elif args.user:
        prefix = None
        user = True
    else:
        prefix = args.prefix
        user = None

    install_K_kernel_spec(user=user, prefix=prefix)


if __name__ == '__main__':
    main(argv=sys.argv)
