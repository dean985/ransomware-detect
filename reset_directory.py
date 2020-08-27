import shutil
import os

home = os.getcwd()
try:
    os.mkdir('archived')
except FileExistsError:
    shutil.rmtree('archived')
    try:
        os.mkdir('archived')
    except ...:
        pass
except PermissionError:
    pass

path_archived = os.path.join(home, 'archived')


def start():
    os.chdir('data')
    for file in os.listdir("."):
        if file.endswith(".bu"):
            p = os.path.join(home, 'data', file)
            try:
                shutil.move(p, path_archived)
            except ...:
                os.remove(os.path.join(path_archived, file))
                shutil.move(p, path_archived)


start()
