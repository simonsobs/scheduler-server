import setuptools

import versioneer

setuptools.setup(
    name="scheduler_server",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Yilun Guan",
    author_email="yilun.guan@utoronto.ca",
    description="scheduler server",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "scheduler_server": [
            "configs/data/*.txt",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=[
        # List your package dependencies here, e.g.:
        # "numpy>=1.20",
        # "pandas>=1.3",
    ],
)

