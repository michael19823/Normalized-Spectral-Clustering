from invoke import task
import importlib


@task
def build(c):
    c.run("python3.8.5 setup.py build_ext --inplace")


@task(aliases=['del'])
def delete(c):
    if importlib.util.find_spec("mykmeanssp") is not None:
        c.run("rm *mykmeanssp*.so")


@task
def run(c, k=0, n=0, Random=True):
    delete(c)
    build(c)
    import main
    main.run_code(k, n, Random)
