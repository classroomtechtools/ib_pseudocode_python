from distutils.core import setup
setup(
    name="IB DP Pseudocode to Python",
    version=".5",
    description="Write pseudocode, run it as Python and see results",
    author="Adam Morris",
    author_email="classroomtechtools.ctt@gmail.com",
    keywords=[],
    packages=['ib_pseudocode_python'],
    entry_points={
        'console_scripts': [
            'pseudo = ib_pseudocode_python.cli:cli'
        ]
    },
    install_requires=['click'],
    long_description="""
        Transpile IB Pseudocode specification and execute it as Python
    """
)
