# hamer_helper
![image](https://github.com/user-attachments/assets/fa94292d-3043-4e1a-b5aa-f205312e536c)


```
$ python hamer_example.py --help
usage: hamer_example.py [-h] --input-dir PATH --output-dir PATH [--search-ext [STR [STR ...]]]

For each image in the input directory, run HaMeR and composite the detections.

╭─ options ─────────────────────────────────────────────────────────────────────────────────────────────────╮
│ -h, --help              show this help message and exit                                                   │
│ --input-dir PATH        The directory to search for images. (required)                                    │
│ --output-dir PATH       The directory to write the composited images. (required)                          │
│ --search-ext [STR [STR ...]]                                                                              │
│                         Image extensions to search for in the input directory. (default: .jpg .jpeg .png) │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

**Instructions:**

1. Set up an environment with the original HaMeR repo: https://github.com/geopavlakos/hamer
2. Make sure the HaMeR demo script works.
3. Clone `hamer_helper`, then install it via pip in the same environment. (for example: `pip install -e .` in `hamer_helper/`)
4. Run `python hamer_example.py --input-dir PATH --output-dir PATH`.
    - `--input-dir PATH` should point to a directory containing JPEG files.

