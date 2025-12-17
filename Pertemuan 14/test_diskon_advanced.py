# test_diskon_advanced.py

import unittest
from diskon_service import DiskonCalculator

class TestDiskonLanjut(unittest.TestCase):
    
    def setUp(self):
        """Arrange: Siapkan Instance Calculator."""
        self.calc = DiskonCalculator()

    # --- Tes 5: Uji nilai float (Boundary Condition) ---
    def test_diskon_float_33_persen(self):
        """Tes 5: Menguji diskon non-bulat (33%) pada harga non-bulat (999)."""
        # Input: 999.0 dikurangi 33% = 669.33
        hasil = self.calc.hitung_diskon(999.0, 33)
        self.assertAlmostEqual(hasil, 669.33, delta=0.0001)

    # --- Tes 6: Uji Edge Case (Harga Awal 0) ---
    def test_edge_case_harga_nol(self):
        """Tes 6: Menguji kasus tepi di mana harga awal adalah 0."""
        # Input: 0 diskon 50%. Hasil yang diharapkan: 0.0
        hasil = self.calc.hitung_diskon(0, 50)
        self.assertEqual(hasil, 0.0)
        
if __name__ == '__main__':
    unittest.main()