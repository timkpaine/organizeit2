# organizeit2

[![Build Status](https://github.com/timkpaine/organizeit2/actions/workflows/build.yml/badge.svg?branch=main&event=push)](https://github.com/timkpaine/organizeit2/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/timkpaine/organizeit2/branch/main/graph/badge.svg)](https://codecov.io/gh/timkpaine/organizeit2)
[![License](https://img.shields.io/github/license/timkpaine/organizeit2)](https://github.com/timkpaine/organizeit2)
[![PyPI](https://img.shields.io/pypi/v/organizeit2.svg)](https://pypi.python.org/pypi/organizeit2)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/timkpaine/organizeit2/main?urlpath=lab)

> This morning at dawn, you will take a new form - that of a fleshless, chattering skeleton when Zorp the Surveyor arrives and burns your flesh off with his volcano mouth

`OrganizeIt2` is a python library for managing large numbers of files and directories. It is type- and configuration-driven with [pydantic](https://docs.pydantic.dev/latest/).

## Overview

`OrganizeIt2` has the following models and types:

- `FileSystem`: `pydantic` wrapper of an `fsspec` `AbstractFileSystem`
- `Path`: wrapper of an `fsspec` path
- `FilePath`: specialization of a `Path` for files
- `DirectoryPath`: specialization of a `Path` for directories
- `OrganizeIt`: Top-level `pydantic` model representiing an `fsspec` directory
- `Directory`: `pydantic` model representing an `fsspec` directory
- `File`: `pydantic` model representing an `fsspec` file



