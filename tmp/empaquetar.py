from pathlib import Path
import zipfile, hashlib, json
from pypdf import PdfReader
root=Path(__file__).resolve().parents[1]
delivery=root/'entrega'
pdf=delivery/'Laboratorio_03_Carlos_Estrada_20853.pdf'
r=PdfReader(pdf)
assert len(r.pages)==8
content='\n'.join(page.extract_text() for page in r.pages)
for term in ('Carlos Daniel Estrada Vega','20853','Speedup','MPI_Allreduce','1048576','capturas'):
    assert term in content or (term == '1048576' and term in content.replace(' ', '')), term
assert sum(len(page.images) for page in r.pages) == 6
assert all(term not in content.lower() for term in ('quedaron pendientes', 'no son capturas', 'control de aplicaciones'))
original=Path('C:/Users/carlos.estrada/Downloads/busqueda_clave_aes_secuencial.c')
assert original.read_bytes()==(delivery/'programas'/'busqueda_clave_aes_secuencial.c').read_bytes()
paths=[pdf,delivery/'README.md']
paths+=sorted((delivery/'programas').iterdir())
paths+=sorted((delivery/'evidencias').glob('*.txt'))
captures=sorted((delivery/'evidencias').glob('*.png'))
assert len(captures)==6
paths+=captures
paths+=[delivery/'resultados'/n for n in ('datos.aes','tiempos.csv','resumen.json','tiempos_capturas.csv')]
paths=[p for p in paths if p.is_file()]
manifest={p.relative_to(delivery).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
(delivery/'SHA256.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
paths.append(delivery/'SHA256.json')
archive=root/'Laboratorio_03_Carlos_Estrada_20853.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in paths:z.write(p,Path('Laboratorio_03_20853')/p.relative_to(delivery))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print(f'Verificado: PDF de 8 paginas, {len(paths)} archivos, ZIP valido.')
print(f'ZIP: {archive.stat().st_size} bytes')
