"""Generates 3D models for ASCII letters or UNICODE glyphs based on a font file.
"""


import argparse
from curses.ascii import isspace
import os
import sys


def create_3d_model(char_code, font_name, outout_dir,
                    glyph_size, extrude, bevel_depth, bevel_resolution):
    """Creates a 3D model for a single letter.
    """
    # Deletes all text objects.
    for obj in bpy.data.objects:
        if obj.type == 'FONT':
            obj.select_set(True)
            bpy.ops.object.delete()

    char_name = 'U%04X' % char_code
    print('\n-----------------------------------------------------------------')
    print(f'Generating 3D model for glyph {char_name}')

    # Adds a new text object.
    bpy.ops.object.text_add()
    text_obj = bpy.data.objects['Text']
    text_obj.name = char_name
    text_obj.data.name = char_name
    text_obj.data.body = chr(char_code)
    text_obj.data.size = glyph_size
    text_obj.data.font = bpy.data.fonts[font_name]
    text_obj.data.extrude = extrude
    text_obj.data.bevel_depth = bevel_depth
    text_obj.data.bevel_resolution = bevel_resolution
    text_obj.select_set(True)

    # Exports the model to a fbx file.
    model_file = '%s.fbx' % char_name
    model_path = os.path.join(outout_dir, model_file)

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
        print(f'Font "{font_name}" from {font_path} is loaded.')
        return font_name
    else:
        raise ValueError(f'Failed to load font from {font_path}')


def load_charset(charset_path, glyphs):
    """Loads all the non-space glyphs from a UTF-8 plain text file.
    """
    with open(charset_path, encoding='UTF-8') as f:
        for line in f:
            for c in line:
                if not c.isspace() and c.isprintable():
                    glyphs.add(ord(c))


def main(args):
    font_path = os.path.abspath(args.font_file)
    if (not os.path.isfile(font_path)):
        raise ValueError(f'Font file {font_path} does not exist.')

    output_dir = os.path.abspath(args.out_dir)
    if (not os.path.isdir(output_dir)):
        raise ValueError(f'Output dir {output_dir} does not exist.')

    print(f'Font file: {font_path}')
    print(f'Output dir: {output_dir}')

    glyphs = set()
    if args.letters:
        for c in args.letters:
            glyphs.add(ord(c))
    elif args.charset_file:
        load_charset(args.charset_file, glyphs)
    else:
        for char_code in range(args.start_char_code, args.end_char_code + 1):
            glyphs.add(char_code)

    font_name = load_font(font_path)
    for char_code in list(glyphs):
        create_3d_model(char_code, font_name, output_dir,
                        args.glyph_size, args.extrude,
                        args.bevel_depth, args.bevel_resolution)


if __name__ == '__main__':
    print(f'Python version: {sys.version}\n')

    # Filters out Blender's command line arguments.
    for i, arg in enumerate(sys.argv):
        if arg == '--':
            break

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog='[Blender executable] -b -P font_to_3d_models.py --',
        description='''Generate 3D glyph models from a font file.
This script must be launched with the [Blender executable]. See
https://docs.blender.org/manual/en/latest/advanced/command_line/index.html
on how to locate the [Blender executable] on Windows/macOS/Linux.''')
    parser.add_argument('-f', '--font_file', type=str, required=True,
                        help='The path of the font (.TTF or .OTF) file.')
    parser.add_argument('-o', '--out_dir', type=str, required=True,
                        help='The dir to save the output .FBX model files.')
    parser.add_argument('-c', '--charset_file', type=str,
                        help='The path of a plain text charset file.')
    parser.add_argument('-l', '--letters', type=str,
                        help='Letters or glyphs to be converted.')
    parser.add_argument('-s', '--start_char_code', type=int, default=33,
                        help='The start (inclusive) of a Unicode code range.')
    parser.add_argument('-e', '--end_char_code', type=int, default=126,
                        help='The end (inclusive) of a Unicode code range.')
    parser.add_argument('--glyph_size', type=float, default=1.0,
                        help='The size of the generated 3D glyph.')
    parser.add_argument('--extrude', type=float, default=0.02,
                        help='The extrude of the 3D model.')
    parser.add_argument('--bevel_depth', type=float, default=0.0,
                        help='The bevel depth of the 3D model.')
    parser.add_argument('--bevel_resolution', type=float, default=4,
                        help='The bevel resolution of the 3D model.')

    try:
        import bpy
    except ImportError:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args(sys.argv[i+1:])
    main(args)
