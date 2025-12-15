import unittest
from src.flicker_core import calculate_frequencies, calculate_cycle_params

class TestFlickerCore(unittest.TestCase):

    def test_frequency_generation(self):
        freqs = calculate_frequencies(60, 3, 5)
        self.assertEqual(len(freqs), 5)
        self.assertAlmostEqual(freqs[0], 20.0)
        self.assertAlmostEqual(freqs[1], 15.0)
        self.assertAlmostEqual(freqs[2], 12.0)
        self.assertAlmostEqual(freqs[3], 10.0)
        self.assertAlmostEqual(freqs[4], 8.57142857)

    def test_cycle_calculation(self):
        frames, on = calculate_cycle_params(60, 10, 0.5)
        self.assertEqual(frames, 6) 
        self.assertEqual(on, 3)

        frames, on = calculate_cycle_params(120, 20, 0.25)
        self.assertEqual(frames, 6)
        self.assertEqual(on, 2)

    def test_cycle_safety_guards(self):
        frames, on = calculate_cycle_params(120, 60, 0.01)
        self.assertEqual(on, 1)
        frames, on = calculate_cycle_params(120, 60, 0.99)
        self.assertTrue(on < frames)

if __name__ == "__main__":
    unittest.main( )
