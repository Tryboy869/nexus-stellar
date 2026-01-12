from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nexus-stellar",
    version="0.1.0",
    author="Daouda Abdoul Anzize",
    author_email="nexusstudio100@gmail.com",
    description="Moteur de calcul émergent polyglotte auto-compilant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tryboy869/nexus-stellar",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Rust",
        "Programming Language :: C++",
    ],
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.24.0",
    ],
    extras_require={
        "dev": ["pytest>=7.0.0"],
    },
    entry_points={
        "console_scripts": [
            "nexus-stellar=nexus_stellar:demo",
        ],
    },
)