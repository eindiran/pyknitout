"""
Project tasks for the Python Knitout generator.
"""
from invoke import task, run


@task
def clean():
    """Clean up the .pyc files."""
    print("Cleaning up cached .pyc files.\n")
    run("rm -f src/__pycache__/*.pyc")
    run("rm -f __pycache__/*.pyc")
    print("Done!\n")


@task
def test():
    """Run the unit tests."""
    print("Running unit tests.\n")
    run("export PYTHONPATH=$(pwd)/src; python3 test/test_knitout.py")
    print("Tests complete!\n")


@task
def example():
    """Build the examples."""
    print("Building examples.\n")
    run("export PYTHONPATH=$(pwd)/src; python3 examples/example.py")
    print("Done!\n")
