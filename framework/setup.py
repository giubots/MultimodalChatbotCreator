import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='mmcc-framework',
    version='0.1',
    author='Giulio Antonio Abbo',
    author_email='giulioantonio.abbo@gmail.com',
    description='Create a multimodal chatbot modeled on a process',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/giubots/MultimodalChatbotCreator',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        "Operating System :: OS Independent",
    ],
)
