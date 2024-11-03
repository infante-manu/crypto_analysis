from setuptools import setup, find_packages

setup(
    name="crypto_analysis",
    version="0.1.0",
    packages=find_packages(include=["crypto_analysis", "crypto_analysis.*"]),
    install_requires=[line.strip() for line in open("requirements.txt").readlines()],
    description="Crypto analysis tool with data fetching and signal generation",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/crypto_analysis",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
