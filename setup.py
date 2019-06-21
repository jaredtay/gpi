import setuptools 

setuptools.setup(
    name="gpi",
    version="0.0.0",
    author="Jared Taylor",
    packages=setuptools.find_packages(),
    # include_package_data=True,
    # package_data={
    #         'gpi':['assets/welcome.png', 'ui/*.ui']
    #         },
    entry_points={
        'console_scripts':['gpi = gpi.driver:run'],
    },
    install_requires=['redbaron'],
)
