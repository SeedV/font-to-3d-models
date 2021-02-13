# font-to-3d-models

A Blender script to auto generate 3D models for alphabet letters or Unicode glyphs based on a TTF/OTF font file.

## Prerequisites

[Blender](https://www.blender.org/) is installed, and [the command line interface of Blender](https://docs.blender.org/manual/en/latest/advanced/command_line/index.html) is executable.

## Usage

```
blender -b -P font_to_3d_models.py -- <font_path> <output_dir>
blender -b -P font_to_3d_models.py -- <font_path> <output_dir> <letters>

<font_path>: The path to the font file. Both TTF and OTF files are supported.
<outout_dir>: The dir to place the generated 3D models.
<letters>: Optional. If this argument is given, it contains all the UNICODE
    glyphs to be generated. Otherwise, all readable ASCII letters (ASCII 33-126)
    are generated.
```

For launching Blender from command line on Linux/MacOs/Windows, see [here](https://docs.blender.org/manual/en/latest/advanced/command_line/index.html).

E.g., on MacOS, to generate models for all alphabet letters:

```
/Applications/Blender.app/Contents/MacOS/Blender -b -P font_to_3d_models.py -- ./Roboto-Regular.ttf ./out
```

to generate models for A-Z:

```
/Applications/Blender.app/Contents/MacOS/Blender -b -P font_to_3d_models.py -- ./Roboto-Regular.ttf ./out 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
```

## Customization

Feel free to customize the parameters that the script use to create Blender 3D models, e.g.:

```
    text_obj.data.extrude = .06
    text_obj.data.bevel_depth = 0.02
    text_obj.data.bevel_resolution = 5
```

## Examples

3D models A-Z, using [the Roboto font](https://fonts.google.com/specimen/Roboto):

![](images/1.png)

3D models '世', '界', '你', '好', using [the Noto Sans SC font](https://fonts.google.com/specimen/Noto+Sans+SC):

![](images/2.png)