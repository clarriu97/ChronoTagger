# ChronoTagger

ChronoTagger is a tool to add dates and times to image EXIF metadata based on their filenames. It is especially useful for organizing images that lack date and time metadata or have lost this information.

## Features

- **Date and time extraction** from filenames matching specific patterns.
- **EXIF metadata updating** for images.
- **Preservation of image order** based on sequence numbers in filenames.
- **Easily extensible** to support more filename formats.

## Installation

Make sure you have [PDM](https://pdm.fming.dev/latest/) installed. Then, clone this repository and run:

```bash
pdm install
```

## Usage

Place the undated images in a folder, by default named `undated`. You can change the folder name if you wish.

Run the script from the command line:

```bash
pdm run python -m chronotagger.script --undated_folder "undated" --dated_folder "dated"
```

- `--undated_folder`: Folder containing images without dates. Default is undated.
- `--dated_folder`: Folder where the images with dates will be saved. Default is dated.
