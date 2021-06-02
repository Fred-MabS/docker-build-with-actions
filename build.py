#!env python3

"""Build.

Usage:
  build.py --dev [--recreate] [--dry-run]
  build.py --ci [--dry-run] <branch> <sha1> [URL]
  build.py (-h | --help)

Options:
  -h --help         Show this screen.
  --dry-run         Only print commands, do not execute them
Developer specific purpose:
  --dev             Build for development environment
  --dev --recreate  + recreates mabx_mabtope_dev container
CI specific purpose:
  --ci <branch> <sha1> [URL]
                    Build containers for a given <branch> name, at a given <sha1>
                    and optionaly push them to the [URL]-registry
"""
import os
import pwd
import platform
import subprocess
from docopt import docopt


class C:
    END = '\33[0m'
    RED = '\33[91m'
    GREEN = '\33[92m'
    YELLOW = '\33[93m'
    BLUE = '\33[34m'


class FormatDict(dict):
    def __missing__(self, key):
        return 'N/A'


def getCompleteArguments(arguments):
    arguments = FormatDict({k: v for k, v in arguments.items() if v is not None})
    if arguments['<branch>'] == 'master':
        arguments['floatingTag'] = 'stable'
    elif arguments['<branch>'] == 'dev':
        arguments['floatingTag'] = 'latest'
    else:
        arguments['floatingTag'] = 'wip'
    arguments['fullRepoUrl'] = '{URL}/mabtope'.format_map(arguments)
    arguments['devImage'] = 'mabx/mabtope/dev'
    arguments['devContainer'] = arguments['devImage'].replace('/', '_')
    arguments['p'] = '--platform=linux/amd64'

    if platform.system() == 'Darwin':
        uid = 1000
        gid = 1000
    else:
        uid = os.getuid()
        gid = os.getgid()

    arguments['user'] = pwd.getpwuid(os.getuid())[0]
    arguments['pwd'] = os.getcwd()
    arguments['uid'] = uid
    arguments['gid'] = gid
    return arguments


def build(arguments):
    isDev = arguments['--dev']
    isRecreate = arguments['--recreate']
    isCI = arguments['--ci']
    isPush = arguments['URL'] != 'N/A'
    commands = [
        (True, 'BASE', 'docker build -f new_docker/builders/Dockerfile.base {p} -t builder/base .'),
        (True, 'ANARCI', 'docker build -f new_docker/builders/Dockerfile.anarci {p} -t builder/anarci .'),
        (True, 'MODELLER', 'docker build -f new_docker/builders/Dockerfile.modeller {p} -t builder/modeller .'),
        (True, 'PYMOL', 'docker build -f new_docker/builders/Dockerfile.pymol {p} -t builder/pymol .'),
        (True, 'BLASTDB', 'docker build -f new_docker/builders/Dockerfile.blastdb {p} -t builder/blastdb .'),
        (True, 'MABTOPE-DEPS', 'docker build -f new_docker/builders/Dockerfile.mabtope-deps {p} -t builder/mabtope-deps .'),
        (True, 'RUNNER ({user}:{uid}:{gid})', 'docker build --build-arg USER="{user}" --build-arg UID="{uid}" --build-arg GID="{gid}" -f new_docker/runners/Dockerfile.mabtope {p} -t mabx/mabtope .'),
        # DEV-ONLY stuff
        (isDev, 'DEV RUNNER', 'docker build --build-arg USER="{user}" -f new_docker/runners/Dockerfile.mabtope.dev {p} -t "{devImage}" .'),
        (isDev and isRecreate, 'REMOVE DEV CONTAINER ({devContainer})', 'docker rm -f "{devContainer}"'),
        (isDev and isRecreate, 'CREATE DEV CONTAINER ({devContainer})', 'docker create --name "{devContainer}" -p7071:8080 -v "{pwd}/:/app/MAbX/" --entrypoint "/bin/bash" {p} -it "{devImage}"'),
        # CI-ONLY stuff
        (isCI and isPush, 'TAG ({fullRepoUrl}:{<branch>}-{<sha1>})', 'docker tag mabx/mabtope "{fullRepoUrl}:{<branch>}-{<sha1>}"'),
        (isCI and isPush, 'TAG ({fullRepoUrl}:{floatingTag}-{<sha1>})', 'docker tag mabx/mabtope "{fullRepoUrl}:{floatingTag}-{<sha1>}"'),
        (isCI and isPush, 'PUSH ({fullRepoUrl}:{<branch>}-{<sha1>})', 'docker push "{fullRepoUrl}:{<branch>}-{<sha1>}"'),
        (isCI and isPush, 'PUSH ({fullRepoUrl}:{floatingTag}-{<sha1>})', 'docker push "{fullRepoUrl}:{floatingTag}-{<sha1>}"')
    ]
    dryRun = arguments['--dry-run']
    for command in commands:
        description = command[1].format_map(arguments)
        if command[0]:
            cmd = command[2].format_map(arguments)
            if dryRun:
                print(f'{C.BLUE}DRY RUN: {description}{C.END}\n{C.BLUE}$ {cmd}{C.END}')
            else:
                print(f'{C.GREEN}PROCEED: {description}{C.END}\n{C.BLUE}$ {cmd}{C.END}')
                subprocess.run(cmd, shell=True, check=True)
        else:
            print(f'{C.YELLOW}SKIP: {description}{C.END}')


if __name__ == '__main__':
    arguments = docopt(__doc__)
    arguments = getCompleteArguments(arguments)
    build(arguments)
