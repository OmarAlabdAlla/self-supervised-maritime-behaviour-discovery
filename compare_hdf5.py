import h5py
import numpy as np


OLD_FILE = "../extend/DP_50_Compressed_allaData_3ports_4hours.hdf5"
NEW_FILE = "DP_50_Compressed_allaData_3ports_to_use_in_github.hdf5"


def values_equal(a, b):
    if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
        return np.array_equal(a, b)

    return a == b


with h5py.File(OLD_FILE, "r") as old, h5py.File(NEW_FILE, "r") as new:

    old_keys = sorted(list(old.keys()))
    new_keys = sorted(list(new.keys()))

    print("Old datasets:", len(old_keys))
    print("New datasets:", len(new_keys))

    print("Dataset names equal:", old_keys == new_keys)

    if old_keys != new_keys:
        print("First missing in new:", list(set(old_keys) - set(new_keys))[:10])
        print("First extra in new:", list(set(new_keys) - set(old_keys))[:10])
        raise SystemExit

    for idx, key in enumerate(old_keys):

        old_data = old[key][()]
        new_data = new[key][()]

        if not np.array_equal(old_data, new_data):
            print("Image data differs at:", key)
            print("Old shape:", old_data.shape)
            print("New shape:", new_data.shape)
            raise SystemExit

        old_attrs = dict(old[key].attrs)
        new_attrs = dict(new[key].attrs)

        if old_attrs.keys() != new_attrs.keys():
            print("Attribute keys differ at:", key)
            print("Old attrs:", old_attrs.keys())
            print("New attrs:", new_attrs.keys())
            raise SystemExit

        for attr_name in old_attrs:

            if not values_equal(old_attrs[attr_name], new_attrs[attr_name]):
                print("Attribute differs at:", key)
                print("Attribute:", attr_name)
                print("Old:", old_attrs[attr_name])
                print("New:", new_attrs[attr_name])
                raise SystemExit

        if idx % 10000 == 0:
            print(f"Checked {idx:,}/{len(old_keys):,}", flush=True)

    print()
    print("HDF5 files are identical.")