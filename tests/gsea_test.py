"""Verifies the 'gsea.py' module"""

from nose.tools import ok_, raises
from nose.tools import eq_

from termlink.gsea import validate_path, _to_json
import json

@raises(ValueError)
def test_validate_path_fails_on_extension():
    """
     Tests to ensure that the validate_path methods fails when the extension is not .gmt
    """
    validate_path('file://msigdb.v6.2.symbols.com')


@raises(ValueError)
def test_validate_path_fails_on_type():
    """
     Tests to ensure that the validate_path methods fails when the first filename segment is not 'msigdb'
    """
    validate_path('file://msigdb.v6.2.foo.gmt')


@raises(ValueError)
def test_validate_path_fails_on_content():
    """
    Tests to ensure that the validate_path methods fails when the content type portion of the filename is not 'symbols'
    """
    validate_path('file://effect.v6.2.symbols.gmt')


def test_to_json():
    """
    Tests to ensure that a tsv record can used to generate the expected json output for the given positons
    """
    gsea_record = ['MYOD_01', 'http://www.broadinstitute.org/gsea/msigdb/cards/MYOD_01', 'KCNE1L', 'FAM126A', 'HMGN2', 'EIF2C1']
    actual = _to_json(gsea_record, 2)
    expected = json.dumps({"equivalence": "subsumes", "target": {"version": None, "code": "MYOD_01", "display": "MYOD_01", "system": "http://www.broadinstitute.org/gsea/msigdb", "type": "coding"}, "source": {"version": None, "code": "KCNE1L", "display": "KCNE1L", "system": "http://www.broadinstitute.org/gsea/msigdb", "type": "coding"}}, sort_keys=True)
    eq_(actual, expected)
    expected = json.dumps({"target": {"type": "coding", "display": "MYOD_01", "system": "http://www.broadinstitute.org/gsea/msigdb", "version": None, "code": "MYOD_01"}, "equivalence": "subsumes", "source": {"type": "coding", "display": "HMGN2", "system": "http://www.broadinstitute.org/gsea/msigdb", "version": None, "code": "HMGN2"}}, sort_keys=True)
    actual = _to_json(gsea_record, 4)
    eq_(actual, expected)
