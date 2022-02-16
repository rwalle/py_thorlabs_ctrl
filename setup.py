iport setuptools

setuptools.setup(name='py_thorlabs_ctrl',
    version='0.1',
    description='Python package as thorlabs .NET control wrapper',
    url='http://github.com/rwalle/py_thorlabs_ctrl',
    author='Zhe Li',
    author_email='lizhe05@gmail.com',
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=['pythonnet'],
    test_suite='tests',
    )
