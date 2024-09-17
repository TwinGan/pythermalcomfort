import numpy as np
from pythermalcomfort.models import discomfort_index

def test_discomfort_index(get_discomfort_index_url, retrieve_data, is_equal):
    # Retrieve reference table from external data source (JSON file in this case)
    reference_table = retrieve_data(get_discomfort_index_url)
    tolerance = reference_table["tolerance"]["di"]

    for entry in reference_table["data"]:
        # Extract input and output data from each entry
        inputs = entry["inputs"]
        expected_outputs = entry["outputs"]["di"]
        
        # Calculate discomfort_index for each input set
        if isinstance(inputs["tdb"], list):  # handle cases where inputs are lists
            for i, tdb in enumerate(inputs["tdb"]):
                input_args = {"tdb": tdb, "rh": inputs["rh"]}
                result = discomfort_index(**input_args)
                
                # Compare the result with the expected output
                assert is_equal(result, expected_outputs[i], tolerance), \
                    f"Discomfort index mismatch for tdb={tdb}, rh={inputs['rh']}: Expected {expected_outputs[i]}, but got {result}"

        else:  # handle cases where inputs might be individual values
            result = discomfort_index(**inputs)
            for i, res in enumerate(result):
                assert is_equal(res, expected_outputs[i], tolerance), \
                    f"Discomfort index mismatch for inputs={inputs}: Expected {expected_outputs[i]}, but got {res}"
                
    print("All tests passed!")

