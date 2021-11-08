"""Generates 3D models for ASCII letters or UNICODE glyphs based on a font file.

Usage:

blender -b -P font_to_3d_models.py -- <font_path> <output_dir>
blender -b -P font_to_3d_models.py -- <font_path> <output_dir> <letters>

<font_path>: The path to the font file. Both TTF and OTF files are supported.
<outout_dir>: The dir to place the generated 3D models.
<letters>: Optional. If this argument is given, it contains all the UNICODE
    glyphs to be generated. Otherwise, all readable ASCII letters (ASCII 33-126)
    are generated.

For launching Blender from command line on Linux/MacOs/Windows, see:
https://docs.blender.org/manual/en/latest/advanced/command_line/index.html

E.g., on MacOS, to generate models for all alphabet letters:

/Applications/Blender.app/Contents/MacOS/Blender -b -P font_to_3d_models.py -- ./Roboto-Regular.ttf ./out

to generate models for A-Z:

/Applications/Blender.app/Contents/MacOS/Blender -b -P font_to_3d_models.py -- ./Roboto-Regular.ttf ./out 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
"""


import os
import sys


import bpy


def create_3d_model(char_code, font_name, outout_dir):
    """Creates a 3D model for a single letter.
    """
    # Deletes all text objects.
    for obj in bpy.data.objects:
        if obj.type == 'FONT':
            obj.select_set(True)
            bpy.ops.object.delete()

    char_name = 'U%04X' % char_code

    # Adds a new text object.
    bpy.ops.object.text_add()
    text_obj = bpy.data.objects['Text']
    text_obj.name = char_name
    text_obj.data.name = char_name
    text_obj.data.body = chr(char_code)
    text_obj.data.size = 2
    text_obj.data.font = bpy.data.fonts[font_name]
    text_obj.data.extrude = .04
    text_obj.data.bevel_depth = 0.005
    text_obj.data.bevel_resolution = 4
    text_obj.select_set(True)

    # Exports the model to a fbx file.
    model_file = '%s.fbx' % char_name
    model_path = os.path.join(outout_dir, model_file)

    print('Generating model for letter %s' % chr(char_code))
    bpy.ops.export_scene.fbx(filepath=model_path,
        check_existing=False,
        use_selection=True)


def load_font(font_path):
    """Loads the specified font into Blender.

    Returns the name of the loaded font.
    """
    existed_num = len(bpy.data.fonts)
    bpy.ops.font.open(filepath=font_path)
    if len(bpy.data.fonts) > existed_num:
        font_name = bpy.data.fonts[-1].name
        print(f'Font {font_name} from {font_path} is loaded.')
        return font_name
    else:
        print(f'Failed to load the font {font_path}')
        return None


def main(argv):
    if (len(argv) < 2):
        print('Usage: ')
        print('    blender -b -P font_to_3d_models.py -- <font_path> <output_dir>')
        print('    blender -b -P font_to_3d_models.py -- <font_path> <output_dir> <letters>')
        return

    font_path = os.path.abspath(argv[0])
    if (not os.path.isfile(font_path)):
        print('Font file %s does not exist.' % font_path)
        return

    output_dir = os.path.abspath(argv[1])
    if (not os.path.isdir(output_dir)):
        print(f'Output dir {output_dir} does not exist.')
        return

    print(f'Font file: {font_path}')
    print(f'Output dir: {output_dir}')

    letters = set()
    if (len(argv) >= 3):
        for c in argv[2]:
            letters.add(ord(c))
    else:
        for char_code in range(33, 127):
            letters.add(char_code)

    font_name = load_font(font_path)
    print(f'Using font {font_name} to create alphabet models...')

    # Generates models for the letters.
    for char_code in list(letters):
        create_3d_model(char_code, font_name, output_dir)


if __name__ == '__main__':
    # Filters out Blender arguments.
    for i, arg in enumerate(sys.argv):
        if arg == '--':
            break
    main(sys.argv[i+1:])
