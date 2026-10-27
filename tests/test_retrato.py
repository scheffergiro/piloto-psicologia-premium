"""Asset safety, output isolation and v2 compatibility (no legacy renderer)."""
import json
import struct
import tempfile
import unittest
import zlib
from pathlib import Path
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0,str(ROOT))
from gerar import gerar
from gerar_retrato import gerar_retrato


def png():
    def chunk(kind,data):
        return struct.pack('!I',len(data))+kind+data+struct.pack('!I',zlib.crc32(kind+data)&0xffffffff)
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('!2I5B',1,1,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(b'\0\xdd\xd5\xc2'))+chunk(b'IEND',b'')

class AssetSafetyTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.config=self.root/'cliente.json';self.output=self.root/'public'
        self.data=json.loads((ROOT/'cliente.json').read_text())
        self.source=self.root/'src';(self.source/'assets').mkdir(parents=True)
        # Use original non-personal source assets with an isolated image directory.
        for name in ('home.html','styles.css','motion.js','navigation.js'):
            (self.source/name).write_bytes((ROOT/'src'/name).read_bytes())
        import shutil
        shutil.copytree(ROOT/'src/assets/fonts',self.source/'assets/fonts')
        self.mock=patch('gerar.SOURCE',self.source);self.mock.start();self.addCleanup(self.mock.stop)
    def generate(self):
        self.config.write_text(json.dumps(self.data));gerar(self.config,self.output)
        return (self.output/'index.html').read_text()
    def photo(self):
        self.data['HOME']['photo'].update(file='assets/retrato.png',alt='Imagem geométrica sintética',width=682,height=863)
        (self.source/'assets/retrato.png').write_bytes(png())
    def test_photo_is_copied_from_source_and_removed_when_unconfigured(self):
        self.photo();self.assertIn('alt="Imagem geométrica sintética"',self.generate())
        self.assertEqual((self.output/'assets/retrato.png').read_bytes(),png())
        self.data['HOME']['photo']['file']='';self.generate();self.assertFalse((self.output/'assets/retrato.png').exists())
    def test_photo_requires_alt_and_file_signature(self):
        self.photo();self.data['HOME']['photo']['alt']=''
        with self.assertRaises(ValueError):self.generate()
        self.data['HOME']['photo']['alt']='Teste';(self.source/'assets/retrato.png').write_bytes(b'not an image')
        with self.assertRaises(ValueError):self.generate()
    def test_missing_configured_photo_is_rejected_before_output(self):
        self.photo();(self.source/'assets/retrato.png').unlink()
        with self.assertRaises(ValueError):self.generate()
        self.assertFalse(self.output.exists())
    def test_traversal_absolute_and_symlink_are_rejected(self):
        self.photo()
        for path in ('../outside.png','/tmp/outside.png','assets/../retrato.png','assets\\retrato.png','assets/retrato.png:evil'):
            self.data['HOME']['photo']['file']=path
            with self.subTest(path=path),self.assertRaises(ValueError):self.generate()
        self.data['HOME']['photo']['file']='assets/link.png';(self.source/'assets/link.png').symlink_to(self.source/'assets/retrato.png')
        with self.assertRaises(ValueError):self.generate()
    def test_hardlink_is_rejected(self):
        import os
        self.photo();os.link(self.source/'assets/retrato.png',self.source/'assets/linked.png')
        with self.assertRaises(ValueError):self.generate()
    def test_output_symlink_is_rejected(self):
        target=self.root/'unrelated';target.mkdir();self.output.symlink_to(target,target_is_directory=True)
        with self.assertRaises(ValueError):self.generate()
        self.assertEqual(list(target.iterdir()),[])
    def test_generated_file_symlink_cannot_overwrite_unrelated_file(self):
        self.generate();outside=self.root/'keep.txt';outside.write_text('keep')
        (self.output/'styles.css').unlink();(self.output/'styles.css').symlink_to(outside)
        with self.assertRaises(ValueError):self.generate()
        self.assertEqual(outside.read_text(),'keep')
    def test_tampered_manifest_cannot_remove_outside_files(self):
        self.generate();(self.output/'.generated-files.json').write_text('["../keep.txt"]')
        with self.assertRaises(ValueError):self.generate()
    def test_source_directory_cannot_be_used_as_output(self):
        self.config.write_text(json.dumps(self.data))
        for dest in (ROOT,ROOT.parent,ROOT/'src',ROOT/'templates'):
            with self.subTest(dest=dest),self.assertRaises(ValueError):gerar(self.config,dest)
    def test_unrelated_output_file_is_preserved(self):
        self.generate();(self.output/'keep.txt').write_text('keep');self.generate()
        self.assertEqual((self.output/'keep.txt').read_text(),'keep')
    def test_compatibility_function_uses_the_same_renderer(self):
        self.generate();before=(self.output/'index.html').read_bytes()
        gerar_retrato(self.config,self.output,experimental=False);self.assertEqual(before,(self.output/'index.html').read_bytes())

if __name__=='__main__':unittest.main()
