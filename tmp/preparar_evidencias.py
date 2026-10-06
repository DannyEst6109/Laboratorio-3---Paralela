from pathlib import Path
import html
root=Path(__file__).resolve().parents[1]/'entrega'/'evidencias'
titles={'01_compilacion':'Compilación de los tres programas','02_original':'Ejecución del programa original',
'03_preparacion':'Preparación del archivo cifrado','04_secuencial':'Búsqueda secuencial mejorada',
'05_mpi_2':'Búsqueda con dos procesos','05_mpi_3':'Búsqueda con tres procesos','05_mpi_4':'Búsqueda con cuatro procesos',
'06_mediciones_resumen':'Resumen de las mediciones','07_pruebas_resumen':'Verificación funcional'}
for name,title in titles.items():
    text=(root/(name+'.txt')).read_text(encoding='utf-8')
    (root/(name+'.html')).write_text('''<!doctype html><html lang="es"><meta charset="utf-8">
<title>Laboratorio 03 - Evidencia</title><style>
body{margin:24px;background:#fff;color:#151515;font-family:Arial,sans-serif}
main{width:1020px;padding:18px;border:1px solid #ccc;box-sizing:border-box}
h1{font-size:24px;margin:0 0 8px}p{font-size:15px;margin:0 0 14px;color:#555}
pre{font:19px/1.5 Consolas,monospace;white-space:pre-wrap;overflow-wrap:anywhere;
background:#f4f5f7;padding:16px;margin:0}small{display:block;margin-top:12px;font-size:14px;color:#555}
</style><main><h1>'''+html.escape(title)+'''</h1>
<p>Laboratorio 03 · Ubuntu en WSL · Registro real de comandos y resultados</p>
<pre>'''+html.escape(text)+'''</pre><small>Fuente: '''+name+'''.txt · Salida capturada de los programas, visualizada en Chrome.</small></main></html>''',encoding='utf-8')
print('Registros preparados para su captura en el navegador.')
