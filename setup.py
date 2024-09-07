from setuptools import setup

setup(
    name='task-cli',
    version='1.0',
    py_modules=['main'],
    entry_points={
        'console_scripts': [
            'task-cli = main:main',
        ],
    },
    install_requires=[],
    python_requires='>=3.6',  # Adjust according to your Python version requirements
)
