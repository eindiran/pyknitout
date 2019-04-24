"""
pyknitout/tasks.py
invoke tasks for pyknitout, a simple wrapper for generating Knitout
instructions in Python scripts.
"""
from invoke import task, run


@task
def clean(ctx):
    """Clean up the .pyc files."""
    print('Cleaning up cached .pyc files.\n')
    run('rm -rf src/__pycache__/')
    run('rm -rf __pycache__/')
    print('Done!\n')


@task
def main_test(ctx):
    """Run the unit tests."""
    print('Running main unit tests.\n')
    run('export PYTHONPATH=$(pwd)/src; python3 test/test_wrapper.py')
    print('Main tests complete!\n')


@task
def extension_test(ctx):
    print('Running extension unit tests.\n')
    run('export PYTHONPATH=$(pwd)/src; python3 test/test_extensions.py')
    print('Extension tests complete!\n')


@task(pre=[main_test, extension_test])
def test(ctx):
    print('All tests complete!\n')


@task
def example(ctx):
    """Build the examples."""
    print('Building examples.\n')
    run('export PYTHONPATH=$(pwd)/src; python3 examples/example.py')
    print('Done!\n')
