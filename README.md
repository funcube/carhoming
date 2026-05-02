# carhoming

## compress_images.py

Resize images in a folder to **1200px wide** and compress them to **under 100KB**,
saving the results into a `WEB/` subfolder with a clean naming scheme.

### Install

```bash
pip install Pillow
```

### Usage

```bash
python3 compress_images.py /path/to/folder
```

The tool will:

1. Read every supported image in the folder (`jpg`, `jpeg`, `png`, `webp`, `bmp`, `tiff`).
2. Resize so the longest width is `1200px` (aspect ratio preserved).
3. Binary-search the JPEG quality to land under `100KB`; downscales further if needed.
4. Write outputs to `<folder>/WEB/<folder_name>_NN_web.jpg` (e.g. `mytrip_01_web.jpg`).
5. Print a per-file before/after comparison and a total summary.

### Windows drag-and-drop

Place `compress_images.bat` next to `compress_images.py`, then **drag a folder
onto `compress_images.bat`**. It calls Python for you and pauses at the end so
you can read the results.

### Example

```
$ python3 compress_images.py ~/Photos/mytrip
Processing 3 image(s) from /home/me/Photos/mytrip
Output: /home/me/Photos/mytrip/WEB
------------------------------------------------------------------------
[OK] IMG_4012.jpg                   -> mytrip_01_web.jpg      5.5MB ->    99.9KB  (  1.8%)
[OK] IMG_4013.jpg                   -> mytrip_02_web.jpg      1.8MB ->    99.0KB  (  5.5%)
[OK] IMG_4014.jpg                   -> mytrip_03_web.jpg    227.1KB ->    98.8KB  ( 43.5%)
------------------------------------------------------------------------
Total: 7.5MB -> 297.7KB  saved 7.2MB (96.1%)
```
