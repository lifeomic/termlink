"""Verifies the 'gsea.py' module"""

from nose.tools import ok_, raises
from termlink.gsea import validate_path
from termlink.gsea import generate_row

@raises(ValueError)
def test_validate_path_fails_on_extension():
    validate_path('file://msigdb.v6.2.symbols.com')


@raises(ValueError)
def test_validate_path_fails_on_type():
    validate_path('file://msigdb.v6.2.foo.gmt')


@raises(ValueError)
def test_validate_path_fails_on_content():
    validate_path('file://effect.v6.2.symbols.gmt')


def test_to_json():
    gsea_record = ['MYOD_01', 'http://www.broadinstitute.org/gsea/msigdb/cards/MYOD_01', 'KCNE1L', 'FAM126A', 'HMGN2', 'EIF2C1']
    row = generate_row(gsea_record, 2)
    ok_(row == {"target": {"type": "coding", "display": "MYOD_01", "system": "http://www.broadinstitute.org/gsea/msigdb", "version": "null", "code": "MYOD_01"}, "equivalence": "subsumes", "source": {"type": "coding", "display": "KCNE1L", "system": "http://www.broadinstitute.org/gsea/msigdb", "version": "null", "code": "KCNE1L"}})
    row = generate_row(gsea_record, 4)
    ok_(row == {"target": {"type": "coding", "display": "MYOD_01", "system": "http://www.broadinstitute.org/gsea/msigdb", "version": "null", "code": "MYOD_01"}, "equivalence": "subsumes", "source": {"type": "coding", "display": "HMGN2", "system": "http://www.broadinstitute.org/gsea/msigdb", "version": "null", "code": "HMGN2"}})
