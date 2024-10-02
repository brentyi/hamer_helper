# hamer_helper

<img alt="viser logo" src="https://github.com/user-attachments/assets/5c87d823-1f45-49f1-9ed7-848659cc6d6a" width="auto" height="200" />
<br />

A small wrapper around [HaMeR](https://github.com/geopavlakos/hamer), a great model for 3D hand estimation from RGB images!

We provide a modular API (`HamerHelper()`) and an example script (`inference.py`).

---

**Instructions:**

1. Set up an environment with the original HaMeR repo: https://github.com/geopavlakos/hamer
2. Make sure the HaMeR demo script works.
3. Clone `hamer_helper`, then install it via pip in the same environment. (for example: `pip install -e .` in `hamer_helper/`)
4. Run `python inference.py --input-dir PATH --output-dir PATH`.

---

```
$ python inference.py --help
usage: inference.py [-h] --input-dir PATH --output-dir PATH [--search-ext [STR [STR ...]]]

For each image in the input directory, run HaMeR and composite the detections.

╭─ options ─────────────────────────────────────────────────────────────────────────────────────────────────╮
│ -h, --help              show this help message and exit                                                   │
│ --input-dir PATH        The directory to search for images. (required)                                    │
│ --output-dir PATH       The directory to write the composited images. (required)                          │
│ --search-ext [STR [STR ...]]                                                                              │
│                         Image extensions to search for in the input directory. (default: .jpg .jpeg .png) │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
