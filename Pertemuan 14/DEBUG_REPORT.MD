# DEBUG_REPORT.md

## Log Debugging: Penemuan Bug PPN 10% Ganda

**Tujuan:** Menggunakan `pdb` untuk menemukan mengapa hasil dari `hitung_diskon(1000, 10)` menghasilkan 990.0 (padahal seharusnya 900.0).

### Langkah-langkah Penelusuran (Tracing)

1.  Mengaktifkan `pdb.set_trace()` di awal fungsi `hitung_diskon()`.
2.  Menjalankan skrip `python diskon_service.py`. Program berhenti di prompt `(Pdb)`.
3.  Menggunakan perintah `n` untuk maju hingga baris perhitungan PPN:

| Perintah Pdb | Hasil 'p' (Variabel) | Analisis |
| :--- | :--- | :--- |
| `n` | `p harga_akhir` = 900.0 | Harga setelah diskon 10% adalah 900.0 (Benar). |
| `n` | `p ppn` = 90.0 | **Bug Ditemukan:** Variabel `ppn` dihitung sebagai 10% dari 900.0, yaitu 90.0. Ini adalah penambahan PPN yang tidak disengaja. |
| `n` | `p harga_akhir_setelah_ppn` = 990.0 | Nilai 90.0 ditambahkan ke 900.0. |

### Rekomendasi Perbaikan

Menghapus blok kode yang tidak perlu yang menambahkan PPN ganda:

```python
# Hapus baris-baris ini:
# ppn = harga_akhir * 0.10
# harga_akhir_setelah_ppn = harga_akhir + ppn 

# Dan pastikan return statement adalah:
return harga_akhir