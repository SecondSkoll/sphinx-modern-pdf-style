"""Sphinx configuration for sphinx-modern-pdf-style"""

import ast
from pathlib import Path
from typing import Any

from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.util import logging

import yaml


class SphinxConfig(Config):
    """Expanded class for linting config options."""

    modern_pdf_options: dict[str: str]

    def __init__(self) -> None:
        pass

def config_inited(app: Sphinx, config: SphinxConfig) -> None:  # noqa: PLR0915, PLR0912
    """Read user-provided values and setup defaults."""
    logger = logging.getLogger(__name__)

    if not config.set_modern_pdf_config:
        return

    def update_latex_elements(element_keys: list, pre_value: str, post_value: str):
        """Update latex_elements file with replaced values"""
        for item in element_keys:
            config.latex_elements[item] = config.latex_elements[item].replace(pre_value, post_value)

    assets_dir = Path(__file__).parent / "assets"

    replacement_keys = ["preamble", "maketitle"]

    # Set variable default

    pdf_values = {
        "author": config.author,
    }

    # Update defaults with other defaults defined in YAML replacements file

    with open(str(Path(__file__).parent) + "/replacements.yaml", "rt") as file:
        pdf_values.update(yaml.safe_load(file))

    # Set pdf values input from project

    pdf_values.update(config.modern_pdf_options)

    # Update pdf values replacement values for existing content

    pdf_values["copyright_content"] = pdf_values["copyright_content"].replace("<<author>>", pdf_values["author"]) 

    # set config options

    for key, value in pdf_values.items():
        try:
            config.modern_pdf_options.setdefault(key, value)
        except:
            raise Exception("yes this one")
        
    # set options for general Sphinx config

    if config.set_modern_pdf_config:
        config.latex_engine = "xelatex"
        config.latex_show_pagerefs = True
        config.latex_show_urls = "footnote"
        config.latex_table_style = ["standard", "colorrows", "booktabs"]

        with Path.open(assets_dir / "latex_elements_template.txt", "r+") as file:
            config.latex_config = file.read()

        if (
            config.latex_elements == {}
        ):  # pyright: ignore [reportUnnecessaryComparison] type: # ignore[comparison-overlap]
            config.latex_elements = ast.literal_eval(config.latex_config)

            for key, value in pdf_values.items():
                update_latex_elements(replacement_keys, f"<<{key}>>", value)

def setup(app: Sphinx) -> dict[str, Any]:
    """Perform the main configuration"""
    # These are options that the user can set on their "conf.py"
    # (many options are still missing).
    app.add_config_value(  # pyright: ignore [reportUnknownMemberType]
        "set_modern_pdf_config",
        default=False,
        rebuild="env",
        types=bool,
    )
    app.add_config_value(  # pyright: ignore [reportUnknownMemberType]
        "modern_pdf_options",
        default={},
        rebuild="env",
        types={str: str},
    )

    # Hook into config-inited so we can do more work after "conf.py" is parsed.
    app.connect(  # pyright: ignore [reportUnknownMemberType]
        "config-inited",
        config_inited,
    )

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }