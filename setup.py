from setuptools import setup, find_packages

setup(
    name='question_answering',
    version='1.0.0',
    description='Question Answering Trainer',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'google-api-python-client==1.8.3',
        'google-cloud-storage==1.29.0',
        'simpletransformers==0.51.3',
    ],
)
