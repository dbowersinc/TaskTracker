from setuptools import setup, find_packages

setup(
    name='task_tracker_cli',
    version='0.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'tasks = task_tracker_cli.cli:tasks',
        ],
    },
)
