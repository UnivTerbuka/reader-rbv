from reader_rbv import Reader, Buku


def test_reader(reader: Reader):
    msim4103: Buku = reader["MSIM4103"]
    assert isinstance(msim4103, Buku)
    assert len(msim4103) == 11
    assert msim4103["DAFIS"].max_page == 6
