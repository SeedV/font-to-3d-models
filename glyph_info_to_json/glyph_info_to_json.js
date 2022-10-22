// Copyright 2021-2022 The SeedV Lab.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import fs from 'fs';
import opentype from 'opentype.js';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';


function output(outputJson, fontInfo) {
  fs.writeFile(outputJson, JSON.stringify(fontInfo), (err) => {
    if (err != null) {
      throw `Failed to output to ${outputJson}: ${err}`;
    }
  });
}


function glyph_info_to_json(fontFile, outputJson) {
  opentype.load(fontFile, function(err, font) {
    if (err != null) {
      throw `Failed to load font file ${fontFile}: ${err}`;
    }

    // TODO: Include and use the font.kerningPairs map.
    const fontInfo = {}
    fontInfo.fontFamily = font.names.fontFamily.en;
    fontInfo.fontSubfamily = font.names.fontSubfamily.en;
    fontInfo.fullName = font.names.fullName.en;
    fontInfo.version = font.names.version.en;
    fontInfo.license = font.names.license.en;
    fontInfo.unitsPerEm = font.tables.head.unitsPerEm;
    fontInfo.xMin = font.tables.head.xMin;
    fontInfo.xMax = font.tables.head.xMax;
    fontInfo.yMin = font.tables.head.yMin;
    fontInfo.yMax = font.tables.head.yMax;
    fontInfo.ascender = font.tables.hhea.ascender;
    fontInfo.descender = font.tables.hhea.descender;
    fontInfo.advanceWidthMax = font.tables.hhea.advanceWidthMax;
    fontInfo.minLeftSideBearing = font.tables.hhea.minLeftSideBearing;
    fontInfo.minRightSideBearing = font.tables.hhea.minRightSideBearing;

    fontInfo.glyphs = [];
    for (let i = 0; i < font.glyphs.length; i++) {
      const glyph = font.glyphs.glyphs[i];
      const glyphInfo = {};
      if (glyph.unicode != null) {
        glyphInfo.unicode = glyph.unicode;
        glyphInfo.advanceWidth = glyph.advanceWidth;
        glyphInfo.leftSideBearing =
            glyph.leftSideBearing ? glyph.leftSideBearing : 0;
        glyphInfo.xMin = glyph.xMin ? glyph.xMin : 0;
        glyphInfo.xMax = glyph.xMax ? glyph.xMax : 0;
        glyphInfo.yMin = glyph.yMin ? glyph.yMin : 0;
        glyphInfo.yMax = glyph.yMax ? glyph.yMax : 0;
        fontInfo.glyphs.push(glyphInfo);
      }
    }
    output(outputJson, fontInfo);
  });
}


const argv = yargs(hideBin(process.argv))
  .scriptName("glyph_info_to_json")
  .usage('$0 [args]')
  .option('font_file', {
    alias: 'f',
    type: 'string',
    description: 'TTF or OTF file path',
  })
  .option('output_json', {
    alias: 'o',
    type: 'string',
    description: 'Output JSON file',
  })
  .help()
  .argv;

  glyph_info_to_json(argv.font_file, argv.output_json)
