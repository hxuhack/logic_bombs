import os

from shutil import rmtree


dirs_gonna_remove = ['tmp', 'angr', 'triton', 'klee', 'build']
list(map(lambda x: rmtree(x, True), dirs_gonna_remove))

files_gonna_remove = ['core', 'tmp.covpro']
list(map(lambda x: os.remove(x) if os.path.exists(x) else None, files_gonna_remove))
