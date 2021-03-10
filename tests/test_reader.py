from reader_rbv import Reader, Book


def test_reader(reader: Reader):
    msim4103: Book = reader["MSIM4103"]
    assert isinstance(msim4103, Book)
    assert len(msim4103) == 11
    assert msim4103["DAFIS"].max_page == 6
