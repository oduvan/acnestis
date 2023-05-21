import nox


@nox.session(python=["3.8", "3.9", "3.10", "3.11"])
def tests(session):
    session.install("pytest==7.3.1", "poetry==1.5.0")
    session.run("poetry", "install", external=True)
    session.run("pytest")
