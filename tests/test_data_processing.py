import unittest
from src.data_processing import process_well_log_data

class TestDataProcessing(unittest.TestCase):

    def test_process_well_log_data(self):
        # Example test case for the data processing function
        input_data = {
            'depth': [100, 200, 300],
            'gamma_ray': [50, 60, 70],
            'resistivity': [1.0, 2.0, 3.0]
        }
        expected_output = {
            'depth': [100, 200, 300],
            'gamma_ray': [50, 60, 70],
            'resistivity': [1.0, 2.0, 3.0],
            'normalized_gamma_ray': [0.0, 0.2, 0.4]  # Example normalization
        }
        
        output_data = process_well_log_data(input_data)
        self.assertEqual(output_data, expected_output)

if __name__ == '__main__':
    unittest.main()