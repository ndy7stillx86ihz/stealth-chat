from setuptools import setup, find_packages

setup(
    name='cli-socket-chat',
    version='0.1.0',
    description='Chat implementation using python socket library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Carlos Manuel Fernández Pérez',
    author_email='klyman047@gmail.com',
    url='https://github.com/duckraper/cli-socket-chat',
    packages=find_packages(),
    install_requires=[
        # dpndcs
    ],
    entry_points={
        # 'console_scripts': [
        #     'mi_comando=mi_paquete.main:main',  # 'mi_comando' será el comando que se ejecuta
        # ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)