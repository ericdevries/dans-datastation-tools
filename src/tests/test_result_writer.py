from io import StringIO

import pytest

from datastation.common.result_writer import JsonResultWriter, YamlResultWriter, CsvResultWriter


class TestJsonResultWriter:

    def test_writes_empty_object_for_empty_result(self):
        out_stream = StringIO()
        writer = JsonResultWriter(out_stream)
        writer.write({}, True)
        assert out_stream.getvalue() == "[{}"

    def test_writes_result(self):
        out_stream = StringIO()
        writer = JsonResultWriter(out_stream)
        writer.write({"a": 1, "b": 2}, True)
        assert out_stream.getvalue() == '[{"a": 1, "b": 2}'

    def test_prepends_comma_if_not_first(self):
        out_stream = StringIO()
        writer = JsonResultWriter(out_stream)
        writer.write({"a": 1, "b": 2}, False)
        assert out_stream.getvalue() == ', {"a": 1, "b": 2}'

    def test_writes_multiple_rows(self):
        out_stream = StringIO()
        writer = JsonResultWriter(out_stream)
        writer.write({"a": 1, "b": 2}, True)
        writer.write({"a": 3, "b": 4}, False)
        assert out_stream.getvalue() == '[{"a": 1, "b": 2}, {"a": 3, "b": 4}'

    def test_closes_array(self):
        out_stream = StringIO()
        writer = JsonResultWriter(out_stream)
        writer.write({"a": 1, "b": 2}, True)
        writer.close()
        assert out_stream.getvalue() == '[{"a": 1, "b": 2}]'

    def test_closes_array_if_no_results(self):
        out_stream = StringIO()
        writer = JsonResultWriter(out_stream)
        writer.close()
        assert out_stream.getvalue() == '[]'


class TestYamlResultWriter:

    def test_writes_empty_object_for_empty_result(self):
        out_stream = StringIO()
        writer = YamlResultWriter(out_stream)
        writer.write({}, True)
        assert out_stream.getvalue() == "{}\n"

    def test_writes_result(self):
        out_stream = StringIO()
        writer = YamlResultWriter(out_stream)
        writer.write({"a": 1, "b": 2}, True)
        assert out_stream.getvalue() == "a: 1\nb: 2\n"

    def test_does_not_prepend_comma_if_not_first(self):
        out_stream = StringIO()
        writer = YamlResultWriter(out_stream)
        writer.write({"a": 1, "b": 2}, False)
        assert out_stream.getvalue() == "a: 1\nb: 2\n"


class TestCsvResultWriter:

    def test_writes_only_headers_for_empty_result(self):
        out_stream = StringIO()
        writer = CsvResultWriter(["a", "b"], out_stream)
        writer.write({}, True)
        assert out_stream.getvalue() == "a,b\n"

    def test_writes_result(self):
        out_stream = StringIO()
        writer = CsvResultWriter(["a", "b"], out_stream)
        writer.write({"a": 1, "b": 2}, True)
        assert out_stream.getvalue() == "a,b\n1,2\n"

    def test_writes_multiple_rows(self):
        out_stream = StringIO()
        writer = CsvResultWriter(["a", "b"], out_stream)
        writer.write({"a": 1, "b": 2}, True)
        writer.write({"a": 3, "b": 4}, False)
        assert out_stream.getvalue() == "a,b\n1,2\n3,4\n"

    def test_raises_error_if_result_keys_do_not_match_headers(self):
        out_stream = StringIO()
        writer = CsvResultWriter(["a", "b"], out_stream)
        with pytest.raises(ValueError):
            writer.write({"a": 1, "c": 2}, True)

    def test_does_not_prepend_comma_if_not_first(self):
        out_stream = StringIO()
        writer = CsvResultWriter(["a", "b"], out_stream)
        writer.write({"a": 1, "b": 2}, False)
        assert out_stream.getvalue() == "a,b\n1,2\n"

