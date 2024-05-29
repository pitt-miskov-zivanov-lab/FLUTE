from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='FLUTE',
    version='Latest',

    author='Emilee Holtzapple, Miskov-Zivanov Lab (MeLoDy lab)',
    author_email='nmzivanov@pitt.edu',
    description='The FiLter for Understanding True Events',
    long_description="The FiLter for Understanding True Events (FLUTE) tool seeks to identify high-confidence "
                     "signaling events from biomedical NLP output by comparing with existing biological databases. As "
                     "such, FLUTE can reliably determine the confidence in the biomolecular events extracted by NLP "
                     "methods and at the same time provide a speedup in event filtering by three orders of magnitude.",
    license='MIT',
    keywords='NLP, filter, knowledge-base, biomedical',

    packages=['src'],
    include_package_data=True,

    install_requires=[
        'networkx>=2.5',
        'mysql-connector-python',
        'numpy',
        'pandas',
        'setuptools',
        'matplotlib'
    ],
    zip_safe=False  # install as directory
    )
