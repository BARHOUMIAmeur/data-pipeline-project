
from setuptools import setup, find_packages

setup(
    name='projet_pipeline_donnees',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'lancer_pipeline=pipeline_donnees.generer_sortie:generer_sortie'
        ]
    },
)
