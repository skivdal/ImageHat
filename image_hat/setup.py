from setuptools import setup, find_packages 

setup(
    name="ImageHat",
    version="0.1.0",
    description="A sample Python package",
    author="Sindre Sæter",
    author_email=["saeter.sindre@gmail.com", "fij016@uib.no"],
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[],       # List dependencies, if any
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
