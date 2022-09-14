"""Generates 3D models from Font Awesome Free icons.
"""


import argparse
import json
import math
import os
import sys


_ICON_TEXT_OBJ_NAME = 'IconText'
_ICON_TEXT_MAT_NAME = 'IconTextMat'
_ICON_CUBE_OBJ_NAME = 'IconCube'
_ICON_CUBE_MAT_NAME = 'IconCubeMat'


def create_3d_icon(icon_name, char_code, font_name, style, output_dir, format):
    """Creates a 3D model for a single letter.
    """
    # Deletes all text objects.
    for obj in bpy.data.objects:
        if obj.type == 'FONT':
            obj.select_set(True)
            bpy.ops.object.delete()

    char_name = icon_name
    print('\n-----------------------------------------------------------------')
    print(f'Generating 3D model for glyph {char_name}, style {style}')

    if style == 1:
        bpy.ops.object.text_add(align='WORLD', location=(0,0,0),
                                rotation=(90 * math.pi / 180, 0, 0),
                                scale=(1,1,1))
        bpy.context.object.name = _ICON_TEXT_OBJ_NAME
        text_obj = bpy.data.objects[_ICON_TEXT_OBJ_NAME]
        text_obj.data.align_x = 'CENTER'
        text_obj.data.align_y = 'CENTER'
        text_obj.data.body = chr(char_code)
        text_obj.data.size = 1.0
        text_obj.data.font = bpy.data.fonts[font_name]
        text_obj.data.extrude = 0.05
        text_obj.data.bevel_depth = 0.0
        text_obj.data.bevel_resolution = 4
        text_obj.location = (0, -.8, 0)

        bpy.ops.mesh.primitive_cube_add(enter_editmode=False,
                                        align='WORLD',
                                        location=(0, 0, 0), scale=(.8, .8, .8))
        bpy.context.object.name = _ICON_CUBE_OBJ_NAME
        cube_base_obj = bpy.data.objects[_ICON_CUBE_OBJ_NAME]
        bpy.ops.object.transform_apply(location=False,
                                       rotation=False,
                                       scale=True)
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.bevel(offset=0.3, offset_pct=0, segments=5,
                           release_confirm=True)
        bpy.ops.object.editmode_toggle()

        text_obj.select_set(True)
        cube_base_obj.select_set(True)
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
        text_obj.select_set(False)
        cube_base_obj.select_set(False)

        if _ICON_TEXT_MAT_NAME in bpy.data.materials:
            icon_text_mat = bpy.data.materials[_ICON_TEXT_MAT_NAME]
        else:
            icon_text_mat = bpy.data.materials.new(name=_ICON_TEXT_MAT_NAME)
        text_obj.data.materials.append(icon_text_mat)
        text_obj.active_material.diffuse_color = (0, 0.318546, 1, 1)

        if _ICON_CUBE_MAT_NAME in bpy.data.materials:
            icon_cube_mat = bpy.data.materials[_ICON_CUBE_MAT_NAME]
        else:
            icon_cube_mat = bpy.data.materials.new(name=_ICON_CUBE_MAT_NAME)
        cube_base_obj.data.materials.append(icon_cube_mat)
        cube_base_obj.active_material.diffuse_color = (0, 0, 0, 1)

        text_obj.select_set(True)
        cube_base_obj.select_set(True)

    elif style == 2:
        raise NotImplementedError(f'Not implemented style {style}')

    elif style == 3:
        raise NotImplementedError(f'Not implemented style {style}')

    # Exports the model.
    if format == 'gltf':
        ext = 'glb'
    elif format == 'fbx':
        ext = 'fbx'

    model_file = f'{char_name}_s{style}.{ext}'
    model_path = os.path.join(output_dir, model_file)

    if format == 'gltf':
        bpy.ops.export_scene.gltf(filepath=model_path,
                                  check_existing=False,
                                  use_selection=True)
    elif format == 'fbx':
        bpy.ops.export_scene.fbx(filepath=model_path,
                                 export_format='GLB',
                                 check_existing=False,
                                 use_selection=True)


def load_font(font_path):
    """Loads the specified font into Blender.

    Returns the name of the loaded font.
    """
    existed_num = len(bpy.data.fonts)
    bpy.ops.font.open(filepath=font_path)
    if len(bpy.data.fonts) > existed_num:
        # TODO: Support multiple-fonts in one font file.
        font_name = bpy.data.fonts[-1].name
        print(f'Font "{font_name}" from {font_path} is loaded.')
        return font_name
    else:
        raise ValueError(f'Failed to load font from {font_path}')


def main(args):
    font_path = os.path.abspath(args.font_file)
    if (not os.path.isfile(font_path)):
        raise ValueError(f'Font file {font_path} does not exist.')

    js_path = os.path.abspath(args.js_file)
    if (not os.path.isfile(js_path)):
        raise ValueError(f'JS file {font_path} does not exist.')

    output_dir = os.path.abspath(args.out_dir)
    if (not os.path.isdir(output_dir)):
        raise ValueError(f'Output dir {output_dir} does not exist.')

    print(f'Font file: {font_path}')
    print(f'Output dir: {output_dir}')

    font_name = load_font(font_path)

    with open(js_path, 'r') as f:
        in_icons = False
        for line in f:
            line = line.strip()
            if not in_icons:
                if line.startswith('var icons ='):
                    in_icons = True
            else:
                if line.find(':') < 0:
                    in_icons = False
                    break
                icon_name, json_str = (x.strip() for x in line.split(':'))
                icon_name = icon_name.strip('"')
                json_str = json_str.strip(',')
                char_code = int(json.loads(json_str)[3], 16)
                create_3d_icon(icon_name, char_code, font_name,
                               args.style, output_dir, args.format)


if __name__ == '__main__':
    print(f'Python version: {sys.version}\n')

    # Filters out Blender's command line arguments.
    for i, arg in enumerate(sys.argv):
        if arg == '--':
            break

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog='[Blender executable] -b -P font_awesome_to_3d_models.py --',
        description='''Generate 3D glyph models from a Font Awesome font file.
This script must be launched with the [Blender executable]. See
https://docs.blender.org/manual/en/latest/advanced/command_line/index.html
on how to locate the [Blender executable] on Windows/macOS/Linux.''')
    parser.add_argument('-f', '--font_file', type=str,
                        default='fonts/font_awesome_6.2.0/fa-solid-900.ttf',
                        help='The path of Font Awesome font (.TTF or .OTF).')
    parser.add_argument('-j', '--js_file', type=str,
                        default='fonts/font_awesome_6.2.0/solid.js',
                        help='The path of Font Awesome js file.')
    parser.add_argument('-s', '--style', type=int, default=1,
                        choices=[1,2,3],
                        help='The output style of 3D models.')
    parser.add_argument('-o', '--out_dir', type=str, required=True,
                        help='The dir to save the output 3D model files.')
    parser.add_argument('--format', choices=['gltf', 'fbx'], default='gltf',
                        help='The format of the output 3D files.')

    try:
        import bpy
    except ImportError:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args(sys.argv[i+1:])
    main(args)
