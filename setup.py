import os
from setuptools import setup, find_packages

setup(
    name='DAmon',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click>=8.1.7,<9.0',
        'litellm>=1.34.2,<2.0',
        'python-dotenv>=1.0.1,<2.0',
        'PyPDF2>=3.0.1,<4.0',
        'python-docx>=1.1.0,<2.0',
        'python-pptx>=0.6.23,<1.0',
        'pandas>=2.2.2,<3.0',
        
        'loguru>=0.7.2,<1.0',
        'tenacity>=8.2.3,<9.0',
        'tqdm>=4.66.4,<5.0',
        'openpyxl>=3.1.2,<4.0', # For .xlsx support if needed, though not explicitly requested for .doc/.ppt
    ],
    entry_points={
        'console_scripts': [
            'damon=DAmon.cli:cli',
        ],
    },
    author='Simon Liu',
    author_email='simonliuyuwei@gmail.com',
    description='A CLI tool to extract structured Q&A from documents using LLMs.',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    url='https://github.com/simonliuyuwei/DataArragimon',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Text Processing',
    ],
    python_requires='>=3.8',
)