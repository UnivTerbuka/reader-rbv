# Reader RBV

[![reader-rbv - PyPi](https://img.shields.io/pypi/v/reader-rbv)](https://pypi.org/project/reader-rbv/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/reader-rbv)](https://pypi.org/project/reader-rbv/)
[![LICENSE](https://img.shields.io/github/license/UnivTerbuka/reader-rbv)](https://github.com/UnivTerbuka/reader-rbv/blob/main/LICENSE)
[![Code Style - Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

SDK / Client python untuk Ruang Baca Virtual.

## Install

Install dengan [python](https://www.python.org/)

```bash
pip install --upgrade reader-rbv
```

## Penggunaan

```python
from reader_rbv import Reader

reader = Reader("username", "Passw0rd")

book1 = reader["BOOK1"]

chapter1_book1 = book1["chapter1"]

page1_chapter1_book1 = chapter1_book1[1]

print(page1_chapter1_book1)
```

Rubah folder cache dengan menyetel env `READER_RBV_HOME` dengan folder yang dituju.

## Legal / Hukum

Kode ini sama sekali tidak berafiliasi dengan, diizinkan, dipelihara, disponsori atau didukung oleh [Universitas Terbuka](https://ut.ac.id/) atau afiliasi atau anak organisasinya. Ini adalah perangkat lunak yang independen dan tidak resmi. Gunakan dengan risiko Anda sendiri.
