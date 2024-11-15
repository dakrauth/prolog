import os
from invoke import task

PYWARN = "python -Wd"


@task
def clean(ctx):
    """Remove build artifacts"""
    ctx.run("rm -rf .cache build prolog.egg-info .coverage htmlcov")


@task
def develop(ctx):
    """Install development requirements"""
    ctx.run("pip install -U pip", pty=True)
    ctx.run("pip install -e .", pty=True)
    ctx.run("pip install -r test-requirements.txt", pty=True)


@task
def test(ctx, show=False, test=None):
    """Run tests and coverage"""
    ctx.run(
        "pytest --cov-config .coveragerc --cov-report html --cov-report term --cov=prolog",
        pty=True,
    )

    if show:
        cov(ctx)


@task
def cov(ctx):
    """Open the coverage reports"""
    if os.path.exists("build/coverage/index.html"):
        ctx.run("open build/coverage/index.html", pty=True)
