"""Generates 3D models for ASCII letters or UNICODE glyphs based on a font file.

Usage:

blender -b -P font_to_3d_models.py -- <font_path> <output_dir>
blender -b -P font_to_3d_models.py -- <font_path> <output_dir> <letters>

<font_path>: The path to the font file. Both TTF and OTF files are supported.
<outout_dir>: The dir to place the generated 3D models.
<letters>: Optional. If this argument is given, it contains all the UNICODE
    glyphs to be generated. Otherwise, all readable ASCII letters (ASCII 33-126)
    are generated.

For launching Blender commandline on Linux/MacOs/Windows, see:
https://docs.blender.org/manual/en/latest/advanced/command_line/index.html

E.g., on MacOS, to make models for all alphabet letters:

/Applications/Blender.app/Contents/MacOS/Blender -b -P font_to_3d_models.py -- ./Roboto-Regular.ttf ./out

to make models for A-Z:

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

    # Adds a new text object.
    bpy.ops.object.text_add()
    text_obj = bpy.data.objects['Text']
    text_obj.data.body = chr(char_code)
    text_obj.data.size = 2
    text_obj.data.font = bpy.data.fonts[font_name]
    text_obj.data.extrude = .06
    text_obj.data.bevel_depth = 0.02
    text_obj.data.bevel_resolution = 5
    text_obj.select_set(True)

    # Exports the model to a fbx file.
    model_file = 'U%04X.fbx' % char_code
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
        print('Font %s from %s is loaded.' % (font_name, font_path))
        return font_name
    else:
        print('Failed to load font %s from %s.' % (font_name, font_path))
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
        print('Output dir %s does not exist.' % output_dir)
        return

    print('Font file: %s' % font_path)
    print('Output dir: %s' % output_dir)

    letters = set()
    if (len(argv) >= 3):
        for c in argv[2]:
            letters.add(ord(c))
    else:
        for char_code in range(33, 127):
            letters.add(char_code)

    font_name = load_font(font_path)
    print('Using font %s to create alphabet models...' % font_name)

    # Generates models for the letters.
    for char_code in list(letters):
        create_3d_model(char_code, font_name, output_dir)


if __name__ == '__main__':
    # Filters out Blender arguments.
    for i, arg in enumerate(sys.argv):
        if arg == '--':
            break
    main(sys.argv[i+1:])
