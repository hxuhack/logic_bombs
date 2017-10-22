import os

from shutil import rmtree


gonna_remove = ['tmp', 'angr', 'triton', 'klee', 'core', 'tmp.covpro']
list(map(lambda x: rmtree(x, True), gonna_remove))
