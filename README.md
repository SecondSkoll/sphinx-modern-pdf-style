# sphinx-modern-pdf-style

This project provides a default configuration for generating PDFs using Sphinx and Xetex. It is currently in development.

## Usage

With the package installed, simply add the following configuration to your Sphinx configuration file:

```
set_modern_pdf_config = True
```

This will set default values for most latex elements.

Certain values can be overwritten to provide additional customisation. For example:

```
modern_pdf_options = {
    "author": "Mr. Author",
}
```

Instead of pulling the author from the `author` key in your configuration, this will set the author (visible on the title page) to this value.

### Advanced usage

Certain values require some additional configuration. For example the logo requires you to add an asset to the build:

```
modern_pdf_options = {
    "logo": "test_logo.png",
}

latex_additional_files = [
    "_static/pdf/test_logo.png"
]
```

This is to ensure the asset is available when the PDF is compiled. The same can be done for fonts and other images.

Note: Read the Docs will only allow a single PDF file to exist in your output directory after a build. If you add additional image files as PDFs to your build, ensure they are removed before the end of Read the Docs' build process.

### Reference

The following values can be overwritten:

```
author:
mainfont_options:
mainfont:
monofont_options:
monofont:
logo_width:
logo:
additional_latex_pagkages:
additional_colors:
additional_environments:
terminal_config: 
copyright_content:
```