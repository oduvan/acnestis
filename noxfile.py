import nox
import os


@nox.session(python=["3.8", "3.9", "3.10", "3.11"])
def tests(session):
    original_cwd = os.getcwd()
    os.chdir("tests/docker_svgo")
    session.run("make", "build")
    os.chdir(original_cwd)

    session.install("pytest==7.3.1", "poetry==1.5.0")
    session.run("poetry", "install", external=True)
    session.run("pytest")
