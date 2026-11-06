import unittest
from io import BytesIO

from beam import (
    bulatkan_ke_atas_50_mm,
    buat_alternatif_lebar,
    hitung_lebar_manual,
    hitung_tinggi_minimum,
)
from slab import (
    bulatkan_ke_atas_10_mm,
    hitung_pelat_dua_arah,
    hitung_pelat_satu_arah,
    periksa_ketebalan_pilihan,
)
from navigation import initialize_state, navigate
from slab import hitung_tebal_minimum_tabel
from column import (
    calculate_square_column_slenderness,
    convert_unbraced_height_to_mm,
    recommend_square_column,
    validate_column_code,
)
from recap import (
    beam_recap_warnings, clear_etabs_beam_recap, column_recap_summary,
    save_etabs_beam_recap, slab_recap_summary,
)
from etabs_beam import hitung_tulangan_balok, read_etabs_beam_summary, status_kebutuhan


class BeamTests(unittest.TestCase):
    def test_height_and_rounding(self):
        self.assertEqual(hitung_tinggi_minimum(6000, "Tumpuan sederhana"), 375)
        self.assertEqual(bulatkan_ke_atas_50_mm(376), 400)
        self.assertEqual(bulatkan_ke_atas_50_mm(400), 400)

    def test_widths_and_area(self):
        choices = buat_alternatif_lebar(600)
        self.assertEqual([c["Lebar (mm)"] for c in choices], [300, 400])
        self.assertEqual(hitung_lebar_manual(600, .5)["Luas penampang (mm²)"], 180000)

    def test_validation(self):
        with self.assertRaises(ValueError):
            hitung_tinggi_minimum(0, "Kantilever")
        with self.assertRaises(ValueError):
            hitung_lebar_manual(300, .7)


class SlabTests(unittest.TestCase):
    def test_user_supplied_table_ratios_all_supports(self):
        conditions = {
            "Tumpuan sederhana": (20, 16),
            "Satu ujung menerus": (24, 18.5),
            "Kedua ujung menerus": (28, 21),
            "Kantilever": (10, 8),
        }
        for support, (one_way, two_way) in conditions.items():
            with self.subTest(support=support):
                self.assertAlmostEqual(hitung_tebal_minimum_tabel(4000, "Pelat satu arah", support)["h_min_mm"], 4000 / one_way)
                self.assertAlmostEqual(hitung_tebal_minimum_tabel(4000, "Pelat dua arah (pelat rusuk)", support)["h_min_mm"], 4000 / two_way)

    def test_user_supplied_table_validation(self):
        with self.assertRaises(ValueError):
            hitung_tebal_minimum_tabel(0, "Pelat satu arah", "Tumpuan sederhana")
        with self.assertRaises(ValueError):
            hitung_tebal_minimum_tabel(4000, "Pelat langsung ke kolom", "Tumpuan sederhana")

    def test_one_way_support_and_fy_adjustment(self):
        result = hitung_pelat_satu_arah(4000, "Tumpuan sederhana", 420)
        self.assertEqual(result["h_min_mm"], 200)
        high_fy = hitung_pelat_satu_arah(4000, "Tumpuan sederhana", 500)
        self.assertAlmostEqual(high_fy["h_min_mm"], 200 * (0.4 + 500 / 700))

    def test_lightweight_and_validation(self):
        result = hitung_pelat_satu_arah(4000, "Kedua ujung menerus", 420, 1700)
        self.assertGreater(result["weight_factor"], 1)
        with self.assertRaises(ValueError):
            hitung_pelat_satu_arah(4000, "Kedua ujung menerus", 420, 2000)
        with self.assertRaises(ValueError):
            hitung_pelat_satu_arah(0, "Tumpuan sederhana")

    def test_two_way_formula_branch_and_edge_adjustment(self):
        basic = hitung_pelat_dua_arah(5000, 6000, 420, [1, 1, 1, 1])
        expected = max(6000 * (0.8 + 420 / 1400) / (36 + 5 * 1.2 * (1 - .2)), 125)
        self.assertAlmostEqual(basic["h_min_mm"], expected)
        stiff = hitung_pelat_dua_arah(5000, 6000, 420, [3, 3, 3, 3])
        self.assertAlmostEqual(stiff["h_min_mm"], max(6000 * (0.8 + 420 / 1400) / (36 + 9 * 1.2), 90))
        edge = hitung_pelat_dua_arah(5000, 6000, 420, [1, 1, .5, .5], panel="Eksterior", edge_cont="Tidak menerus", edge_alpha=.5)
        self.assertTrue(edge["edge_adjustment"])

    def test_two_way_referenced_8311_and_unsupported_inputs(self):
        referred = hitung_pelat_dua_arah(5000, 6000, 420, [.1, .1, .1, .1], tanpa_balok_interior=True)
        self.assertAlmostEqual(referred["h_min_mm"], max(6000 / 33, 125))
        with self.assertRaisesRegex(ValueError, "tanpa balok interior"):
            hitung_pelat_dua_arah(5000, 6000, 420, [.1, .1, .1, .1])
        with self.assertRaises(ValueError):
            hitung_pelat_dua_arah(3000, 7000, 420, [1, 1, 1, 1])
        with self.assertRaises(ValueError):
            hitung_pelat_dua_arah(5000, 6000, 600, [0, 0, 0, 0])

    def test_rounding_and_selected_thickness(self):
        self.assertEqual(bulatkan_ke_atas_10_mm(151), 160)
        self.assertIn("Tidak memenuhi", periksa_ketebalan_pilihan(100, 125))
        self.assertIn("Memenuhi", periksa_ketebalan_pilihan(150, 125))


class NavigationTests(unittest.TestCase):
    def test_routes_and_recap_persistence(self):
        state = {"rekap_balok": {"B1": {"dimensi": "300 × 500 mm"}}}
        initialize_state(state)
        self.assertEqual(state["halaman"], "Beranda")
        navigate(state, "Pra-Desain")
        self.assertEqual(state["halaman"], "Pra-Desain")
        navigate(state, "Pasca-ETABS")
        self.assertEqual(state["rekap_balok"]["B1"]["dimensi"], "300 × 500 mm")
        with self.assertRaises(ValueError):
            navigate(state, "Kolom")


class ColumnTests(unittest.TestCase):
    def test_automatic_square_recommendation_examples(self):
        for beam, expected in [(200, 300), (250, 300), (300, 300), (350, 350), (450, 450)]:
            with self.subTest(beam=beam):
                result = recommend_square_column(beam)
                self.assertEqual((result["width_mm"], result["depth_mm"]), (expected, expected))

    def test_unbraced_height_units_and_validation(self):
        self.assertEqual(convert_unbraced_height_to_mm(3.2, "m"), 3200)
        self.assertEqual(convert_unbraced_height_to_mm(3200, "mm"), 3200)
        for value, unit in [(0, "m"), (-1, "mm"), (float("inf"), "m"), (3, "cm")]:
            with self.subTest(value=value, unit=unit), self.assertRaises(ValueError):
                convert_unbraced_height_to_mm(value, unit)

    def test_slenderness_uses_square_radius_and_assumed_k(self):
        result = calculate_square_column_slenderness(3000, 300)
        self.assertEqual(result["k"], 1.0)
        self.assertEqual(result["radius_gyration_mm"], 90)
        self.assertAlmostEqual(result["slenderness_ratio"], 3000 / 90)

    def test_code_beam_width_and_dimension_validation(self):
        self.assertEqual(validate_column_code(" K2 "), "K2")
        for code in ["", "  ", None]:
            with self.subTest(code=code), self.assertRaises(ValueError):
                validate_column_code(code)
        for value in [0, -250, float("nan")]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                recommend_square_column(value)
        with self.assertRaises(ValueError):
            calculate_square_column_slenderness(3000, 0)

    def test_recap_store_and_session_persistence(self):
        state = {}
        initialize_state(state)
        state["rekap_kolom"]["K1"] = {"dimensi": "300 × 300 mm"}
        navigate(state, "Pra-Desain")
        navigate(state, "Pasca-ETABS")
        self.assertEqual(state["rekap_kolom"]["K1"]["dimensi"], "300 × 300 mm")


class RecapPresentationTests(unittest.TestCase):
    @staticmethod
    def beam_data(height, minimum, ratio):
        return {
            "Tinggi pilihan (mm)": height,
            "Tinggi minimum (mm)": minimum,
            "Lebar pilihan (mm)": height * ratio,
        }

    def test_beam_recap_warning_combinations(self):
        cases = [
            (400, 400, 0.50, 0),
            (350, 400, 0.57, 1),
            (400, 400, 0.45, 1),
            (350, 400, 0.45, 2),
            (400, 400, 0.6667, 0),
        ]
        for height, minimum, ratio, expected_count in cases:
            with self.subTest(height=height, minimum=minimum, ratio=ratio):
                self.assertEqual(
                    len(beam_recap_warnings(self.beam_data(height, minimum, ratio))),
                    expected_count,
                )

    def test_beam_warning_conditions_are_independent(self):
        height_only = beam_recap_warnings(self.beam_data(350, 400, 0.57))
        ratio_only = beam_recap_warnings(self.beam_data(400, 400, 0.45))
        both = beam_recap_warnings(self.beam_data(350, 400, 0.45))
        self.assertIn("Tinggi pilihan", height_only[0])
        self.assertIn("Rasio b/h", ratio_only[0])
        self.assertTrue(any("Tinggi pilihan" in item for item in both))
        self.assertTrue(any("Rasio b/h" in item for item in both))

    def test_slab_recap_selected_hierarchy_and_warning(self):
        data = {"Kode panel": "P1", "Jenis pelat": "Pelat satu arah", "Pilihan (mm)": 150, "h_min_mm": 250}
        title, details, warning = slab_recap_summary(data)
        self.assertIn("150 mm pilihan", title)
        self.assertIn("Rekomendasi minimum 250.00 mm", details)
        self.assertIn("Pilihan 150 mm < rekomendasi minimum 250.00 mm", warning)

    def test_slab_recap_equal_choice_has_no_warning(self):
        data = {"Kode panel": "P1", "Jenis pelat": "Pelat satu arah", "Pilihan (mm)": 250, "h_min_mm": 250}
        title, details, warning = slab_recap_summary(data)
        self.assertIn("250 mm pilihan", title)
        self.assertIn("Rekomendasi minimum 250.00 mm", details)
        self.assertIsNone(warning)

    def test_column_recap_prefers_selection_and_keeps_recommendation(self):
        data = {
            "Kode kolom": "K1", "Pilihan pengguna (mm)": 450,
            "Rekomendasi VECTRION": "300 × 300 mm", "lu (mm)": 3000,
            "Lebar balok terbesar (mm)": 250, "Rasio kelangsingan": 22.22,
        }
        title, details = column_recap_summary(data)
        self.assertEqual(title, "K1 · 450 × 450 mm")
        self.assertIn("Rekomendasi VECTRION 300 × 300 mm", details)
        self.assertIn("klu/r 22.22", details)


class EtabsBeamTests(unittest.TestCase):
    def test_area_conversion_and_requirement_status(self):
        result = hitung_tulangan_balok([16, 13], [1, 0], [16, 13], [1, 0])
        self.assertAlmostEqual(result["As atas tersedia (mm²)"], 201.0619298)
        self.assertEqual(status_kebutuhan(result["As atas tersedia (mm²)"], 200), "Memenuhi")
        self.assertEqual(status_kebutuhan(199, 200), "Tidak memenuhi")
        self.assertEqual(status_kebutuhan(200, 200), "Memenuhi")

    def test_excel_grouping_keeps_story_and_maxima_independent(self):
        from openpyxl import Workbook

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Conc Bm Sum - ACI 318-19"
        sheet.append(["TABLE: Concrete Beam Design Summary"])
        sheet.append(["Story", "Label", "UniqueName", "DesignSect", "Station", "AsTopTotal", "AsBotTotal"])
        sheet.append(["", "", "", "", "mm", "mm²", "mm²"])
        sheet.append(["Lantai 1", "B2", 1, "Balok 30x50", 0, 200, 150])
        sheet.append(["Lantai 1", "B50", 1, "Balok 30x50", 1, 150, 200])
        sheet.append(["Lantai 2", "B2", 2, "Balok 30x50", 0, 180, 160])
        stream = BytesIO()
        stream.name = "example.xlsx"
        workbook.save(stream)
        stream.seek(0)
        stream.name = "example.xlsx"

        result = read_etabs_beam_summary(stream)
        self.assertEqual(len(result["rows"]), 2)
        floor1 = next(row for row in result["rows"] if row["Story"] == "Lantai 1")
        self.assertEqual(floor1["AsTopTotal"], 200)
        self.assertEqual(floor1["AsBotTotal"], 200)
        self.assertEqual(floor1["jumlah_data"], 2)
        self.assertNotIn("Label", floor1)

    def test_two_post_etabs_routes_and_recap_state(self):
        state = {"rekap_balok": {"B1": {"ok": True}}}
        initialize_state(state)
        navigate(state, "Pasca-ETABS-Balok")
        self.assertEqual(state["halaman"], "Pasca-ETABS-Balok")
        record = {
            "DesignSect": "Balok 30x50", "Story": "Lantai 1",
            "As atas tersedia (mm²)": 200, "Status atas": "Memenuhi",
        }
        key = save_etabs_beam_recap(state, record)
        navigate(state, "Pasca-ETABS-Kolom")
        self.assertEqual(state["rekap_etabs_balok"][key]["As atas tersedia (mm²)"], 200)
        self.assertEqual(state["rekap_analisis_etabs"][key]["As atas tersedia (mm²)"], 200)
        self.assertEqual(state["rekap_balok"]["B1"]["ok"], True)
        clear_etabs_beam_recap(state, key)
        self.assertNotIn(key, state["rekap_etabs_balok"])
        self.assertNotIn(key, state["rekap_analisis_etabs"])

    def test_save_updates_existing_pair_without_touching_other_analysis(self):
        state = {
            "rekap_analisis_etabs": {"Lain|Atap": {"As atas tersedia (mm²)": 310}},
            "rekap_etabs_balok": {},
        }
        save_etabs_beam_recap(state, {"DesignSect": "200x300", "Story": "Lantai 1", "As atas tersedia (mm²)": 220})
        self.assertEqual(state["rekap_analisis_etabs"]["Lain|Atap"]["As atas tersedia (mm²)"], 310)
        self.assertIn("200x300|Lantai 1", state["rekap_analisis_etabs"])


if __name__ == "__main__":
    unittest.main()
