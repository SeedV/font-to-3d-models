# Copyright 2021-2022 The SeedV Lab.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
        text_obj = create_text_obj(char_code, _ICON_TEXT_OBJ_NAME, font_name,
                                   0.05, 0.0, 4, (0, -.8, 0))

        bpy.ops.mesh.primitive_cube_add(enter_editmode=False,
                                        align='WORLD',
                                        location=(0, 0, 0),
                                        scale=(.8, .8, .8))
        bpy.context.object.name = _ICON_CUBE_OBJ_NAME
        cube_obj = bpy.data.objects[_ICON_CUBE_OBJ_NAME]
        bpy.ops.object.transform_apply(location=False,
                                       rotation=False,
                                       scale=True)
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.bevel(offset=0.3, offset_pct=0, segments=5,
                           release_confirm=True)
        bpy.ops.object.editmode_toggle()

        text_obj.select_set(True)
        cube_obj.select_set(True)
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
        text_obj.select_set(False)
        cube_obj.select_set(False)

        add_material(text_obj, _ICON_TEXT_MAT_NAME, (0, 0.318546, 1, 1, 1))
        add_material(cube_obj, _ICON_CUBE_MAT_NAME, (0, 0, 0, 1))

        text_obj.select_set(True)
        cube_obj.select_set(True)

    elif style == 2:
        text_obj = create_text_obj(char_code, _ICON_TEXT_OBJ_NAME, font_name,
                                   0.05, 0.0, 4, (0, 0, .7))
        bpy.ops.mesh.primitive_cube_add(enter_editmode=False,
                                        align='WORLD',
                                        location=(0, 0, 0),
                                        scale=(.5, .5, .05))
        bpy.context.object.name = _ICON_CUBE_OBJ_NAME
        cube_obj = bpy.data.objects[_ICON_CUBE_OBJ_NAME]
        bpy.ops.object.transform_apply(location=False,
                                       rotation=False,
                                       scale=True)

        text_obj.select_set(True)
        cube_obj.select_set(True)
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)

        add_material(text_obj, _ICON_TEXT_MAT_NAME, (1, 1, 1, 1))
        add_material(cube_obj, _ICON_CUBE_MAT_NAME, (0, 0, 0, 1))

        text_obj.select_set(True)
        cube_obj.select_set(True)

    elif style == 3:
        text_obj = create_text_obj(char_code, _ICON_TEXT_OBJ_NAME, font_name,
                                   0.05, 0.0, 4, (0, 0, 0))
        bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32,
                                             radius=1, enter_editmode=False,
                                             align='WORLD',
                                             location=(0, 0, 0),
                                             scale=(.8, .8, .8))
        bpy.context.object.name = _ICON_CUBE_OBJ_NAME
        cube_obj = bpy.data.objects[_ICON_CUBE_OBJ_NAME]

        text_obj.select_set(True)
        bpy.ops.object.convert(target='MESH')

        text_obj.select_set(False)
        cube_obj.select_set(True)

        bool_mod = cube_obj.modifiers.new(f'diff_mod', 'BOOLEAN')
        bool_mod.solver = 'FAST'
        bool_mod.operation = 'DIFFERENCE'
        bool_mod.object = text_obj
        bpy.ops.object.modifier_apply(modifier=bool_mod.name)

        add_material(cube_obj, _ICON_CUBE_MAT_NAME, (0, .6, 1, 1))

        text_obj.select_set(False)
        cube_obj.select_set(True)


    # Exports the model.
    if format == 'gltf':
        ext = 'glb'
    elif format == 'fbx':
        ext = 'fbx'

    model_file = f'{char_name}_s{style}.{ext}'
    model_path = os.path.join(output_dir, model_file)

    if format == 'gltf':
        bpy.ops.export_scene.gltf(filepath=model_path,
                                  export_format='GLB',
                                  check_existing=False,
                                  use_selection=True)
    elif format == 'fbx':
        bpy.ops.export_scene.fbx(filepath=model_path,
                                 check_existing=False,
                                 use_selection=True)


def create_text_obj(char_code, obj_name, font_name,
                    extrude, bevel_depth, bevel_resolution,
                    location):
    bpy.ops.object.text_add(align='WORLD', location=(0,0,0),
                            rotation=(90 * math.pi / 180, 0, 0),
                            scale=(1,1,1))
    bpy.context.object.name = obj_name
    text_obj = bpy.data.objects[obj_name]
    text_obj.data.align_x = 'CENTER'
    text_obj.data.align_y = 'CENTER'
    text_obj.data.body = chr(char_code)
    text_obj.data.size = 1.0
    text_obj.data.font = bpy.data.fonts[font_name]
    text_obj.data.extrude = extrude
    text_obj.data.bevel_depth = bevel_depth
    text_obj.data.bevel_resolution = bevel_resolution
    text_obj.location = location
    return text_obj


def add_material(obj, material_name, default_color):
    if material_name in bpy.data.materials:
        mat = bpy.data.materials[material_name]
    else:
        mat = bpy.data.materials.new(name=material_name)
    obj.data.materials.append(mat)
    obj.active_material.diffuse_color = default_color


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
