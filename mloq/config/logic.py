"""This module contains the functionality for parsing ad modifying the project configuration."""
from pathlib import Path
from typing import Optional, Union

from omegaconf import OmegaConf

from mloq.config import Config
from mloq.directories import copy_file
from mloq.files import file as new_file, mloq_yml
from mloq.requirements import require_cuda


def get_docker_python_version(template: Config) -> str:
    """Return the highest python version defined for the project."""
    max_version = list(sorted(template["python_versions"]))[-1]
    version = max_version.replace(".", "")
    return f"py{version}"


def get_docker_image(
    template: Config,
    project_config: Optional[Config] = None,
) -> Union[str, None]:
    """
    Add to params the base docker container that will be used to define the project's container.

    If the dependencies require cuda the base image will be gpu friendly.
    """
    project_config = project_config or {}
    docker_is_false = project_config.get("docker") is not None and not project_config.get("docker")
    if docker_is_false:  # Project does not require Docker
        return "empty"
    # If docker image is defined, return current value even if it's an empty image
    if template.get("docker_image") is not None:
        return template["docker_image"]
    # Define the appropriate FragileTech docker container as base image
    v = get_docker_python_version(template)
    ubuntu_v = "ubuntu20.04" if v == "py38" else "ubuntu18.04"
    image = (
        f"fragiletech/{ubuntu_v}-cuda-11.0-{v}"
        if require_cuda(project_config)
        else f"fragiletech/{ubuntu_v}-base-{v}"
    )
    return image


def write_config(config: Config, path: Union[Path, str], safe: bool = False):
    """Write config in a yaml file."""
    if safe:
        path = Path(path)
        path = path / mloq_yml.name if path.is_dir() else path
    with open(path, "w") as f:
        OmegaConf.save(config, f)


def load_empty_config() -> Config:
    """Return a dictionary containing all the MLOQ config values set to None."""
    empty_config = OmegaConf.load(mloq_yml.src)
    return empty_config


def write_empty_config(path: Union[str, Path], override: bool = False, filename: str = None):
    """Write an empty config file to the target path."""
    repo_file = (
        mloq_yml if filename is None else new_file(mloq_yml.src, mloq_yml.src.parent, filename)
    )
    copy_file(repo_file, Path(path), override)
