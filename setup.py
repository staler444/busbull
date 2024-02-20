from setuptools import setup, find_packages

setup(
    name='busbull',
    version='0.1',
    author='Bartosz Kucypera',
    author_email='bartek.kucypera@gazeta.pl',
    description='Tool for fetaching Warsaw\'s public buses data.',
    long_description='todo',
    long_description_content_type='text/markdown',
    url='https://github.com/staler444/busbull',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='keyword1 keyword2',
    install_requires=[
        'dependency1>=1.0',
        'dependency2>=2.0',
    ],
)
