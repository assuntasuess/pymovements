<p style="text-align:center;">
<img width="110%" height="110%" alt="pymovements"
 src="https://raw.githubusercontent.com/aeye-lab/pymovements/main/docs/source/_static/logo.svg"
 onerror="this.onerror=null;this.src='./docs/source/_static/logo.svg';"/>
</p>

---

[![PyPI Latest Release](https://img.shields.io/pypi/v/pymovements.svg)](https://pypi.python.org/pypi/pymovements/)
[![Conda Latest Release](https://img.shields.io/conda/vn/conda-forge/pymovements)](https://anaconda.org/conda-forge/pymovements)
[![PyPI status](https://img.shields.io/pypi/status/pymovements.svg)](https://pypi.python.org/pypi/pymovements/)
[![Python version](https://img.shields.io/pypi/pyversions/pymovements.svg)](https://pypi.python.org/pypi/pymovements/)
![Operating System](https://img.shields.io/badge/os-linux%20%7C%20macOS%20%7C%20windows-blue)
[![License](https://img.shields.io/pypi/l/pymovements.svg)](https://github.com/aeye-lab/pymovements/blob/master/LICENSE.txt)
[![Test Status](https://img.shields.io/github/actions/workflow/status/aeye-lab/pymovements/tests.yml?label=tests)](https://github.com/aeye-lab/pymovements/actions/workflows/tests.yml)
[![Documentation Status](https://readthedocs.org/projects/pymovements/badge/?version=latest)](https://pymovements.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/github/aeye-lab/pymovements/branch/main/graph/badge.svg?token=QY3NDHAT2C)](https://app.codecov.io/gh/aeye-lab/pymovements)
[![PyPI downloads/month](https://img.shields.io/pypi/dm/pymovements.svg)](https://pypistats.org/packages/pymovements)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/aeye-lab/pymovements/HEAD?labpath=docs%2Fsource%2Ftutorials)


pymovements is an open-source python package for processing eye movement data. It provides a simple
interface to download publicly available datasets, preprocess gaze data, detect oculomotoric events
and render plots to visually analyze your results.

- **Website:** https://github.com/aeye-lab/pymovements
- **Documentation:** https://pymovements.readthedocs.io
- **Source code:** https://github.com/aeye-lab/pymovements
- **Mailing list:** pymovements-list@uni-potsdam.de
- **Contributing:** https://github.com/aeye-lab/pymovements/blob/main/CONTRIBUTING.md
- **Bug reports:** https://github.com/aeye-lab/pymovements/issues
- **PyPI package:** https://pypi.org/project/pymovements
- **Conda package:** https://anaconda.org/conda-forge/pymovements


## Installation

#### Using pip

pymovements can be installed directly from the PyPI repositories:

```bash
pip install pymovements
```

#### Using conda

pymovements can be installed from the conda-forge repositories.

If not already done, you will need to add conda-forge to your available channels:

```bash
conda config --add channels conda-forge
conda config --set channel_priority strict
```

You can then install pymovements into you conda environment:

```bash
conda install -c conda-forge pymovements
```

#### Development installation

To use the latest development version or to try out tutorials, pymovements may be alternatively
cloned and installed with

```bash
git clone https://github.com/aeye-lab/pymovements.git
pip install --upgrade pip
pip install -e ./pymovements
```


## Contributing

We welcome any sort of contribution to pymovements!

For a detailed guide, please refer to our [CONTRIBUTING.md](CONTRIBUTING.md) first.

If you have any questions, please [open an issue](
https://github.com/aeye-lab/pymovements/issues/new/choose) or write us at
[pymovements-list@uni-potsdam.de](mailto:pymovements-list@uni-potsdam.de)


## Citing

If you are using pymovements in your research, we would be happy if you cite our work by using the
following BibTex entry:

```bibtex
@misc{pymovements,
  author = {Krakowczyk, Daniel and Reich, David R. and Chwastek, Jakob, Prasse, Paul and Jäger, Lena},
  title = {pymovements: A Python Package for Processing Eye Movement Data},
  year = {2023},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/aeye-lab/pymovements}},
}
```
