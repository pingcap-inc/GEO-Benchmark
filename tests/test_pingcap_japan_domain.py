import unittest

from geo_benchmark.scoring import is_product_related_url
from geo_benchmark.source_report import source_type_for_url


class PingCAPJapanDomainTests(unittest.TestCase):
    def test_pingcap_japan_is_tidb_related(self):
        self.assertTrue(
            is_product_related_url("TiDB", "https://pingcap.co.jp/blog/example")
        )

    def test_pingcap_japan_is_pingcap_owned(self):
        self.assertEqual(
            source_type_for_url("https://pingcap.co.jp/blog/example"), "PingCAP"
        )

    def test_neon_com_is_neon_related(self):
        self.assertTrue(
            is_product_related_url("Neon", "https://neon.com/docs/introduction")
        )

    def test_neon_com_is_competitor_owned(self):
        self.assertEqual(
            source_type_for_url("https://neon.com/docs/introduction"), "Competitor"
        )


if __name__ == "__main__":
    unittest.main()
