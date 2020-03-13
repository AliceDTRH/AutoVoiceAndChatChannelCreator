import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AutoVoiceAndChatChannelCreator-AliceDTRH", # Replace with your own username
    version="0.0.1",
    author="HiddenKnowledge",
    author_email="57547425+AliceDTRH@users.noreply.github.com",
    description="A bot that automatically creates voice and chat channels.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AutoVoiceAndChatChannelCreator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
