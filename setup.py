from setuptools import setup, find_packages
import pathlib
import re


with open(pathlib.Path.cwd() / "README.md", encoding="utf-8") as file:
    long_description = file.read()


def get_property(property: str, path_to_init_file: pathlib.Path) -> str:
    """
    Reads a property from the project's __init__.py
    e.g. get_property("__version__") -> "1.2.3"
    """
    regex = re.compile(r"{}\s*=\s*[\"'](?P<value>[^\"']*)[\"']".format(property))
    try:
        with open(path_to_init_file) as initfh:
            try:
                result = regex.search(initfh.read()).group("value")
            except AttributeError:
                result = None
    except FileNotFoundError:
        result = None
    return result


project_name = "absolutris"
package_dir = "src"
path_to_init_file = pathlib.Path.cwd() / package_dir / project_name / "__init__.py"


setup(
        name=project_name,
        version=get_property("__version__", path_to_init_file),
        description="The absolute tetris",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author=get_property("__author__", path_to_init_file),
        author_email=get_property("__author_email__", path_to_init_file),
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Topic :: Game Development :: Machine Learning"
            "License :: Unclear",
            "Programming Language :: Python :: 3.8",
            "Operating System :: Microsoft :: Windows",
            ],
        keywords="tetris game machine-learning",
        package_dir={"": package_dir},
        packages=find_packages(where=package_dir),
        package_data={
            project_name: []
            },
        python_requires=">=3.8",
        install_requires=["pygame", "pandas"],
        entry_points={
            "console_scripts": ["absolutris = absolutris.__main__:main"],
            },
        platforms=["Windows"],
     )
