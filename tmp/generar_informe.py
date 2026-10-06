from pathlib import Path
import csv, json, html
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, NextPageTemplate, Image, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted, Flowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'entrega'
AUTHOR='Carlos Daniel Estrada Vega'
FONT=Path('C:/Windows/Fonts')
pdfmetrics.registerFont(TTFont('ArialLocal',str(FONT/'arial.ttf')))
pdfmetrics.registerFont(TTFont('ArialLocalBold',str(FONT/'arialbd.ttf')))
pdfmetrics.registerFont(TTFont('ConsolasLocal',str(FONT/'consola.ttf')))
pdfmetrics.registerFontFamily('ArialLocal',normal='ArialLocal',bold='ArialLocalBold',italic='ArialLocal',boldItalic='ArialLocalBold')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyLab',fontName='ArialLocal',fontSize=10.2,leading=14.5,spaceAfter=8,textColor=black))
styles.add(ParagraphStyle(name='TitleLab',fontName='ArialLocalBold',fontSize=24,leading=29,spaceAfter=14,textColor=black))
styles.add(ParagraphStyle(name='H1Lab',fontName='ArialLocalBold',fontSize=17,leading=22,spaceAfter=13,textColor=black))
styles.add(ParagraphStyle(name='H2Lab',fontName='ArialLocalBold',fontSize=11.5,leading=15,spaceBefore=8,spaceAfter=7,textColor=black))
styles.add(ParagraphStyle(name='SmallLab',fontName='ArialLocal',fontSize=8.5,leading=11.5,spaceAfter=6))
styles.add(ParagraphStyle(name='MonoLab',fontName='ConsolasLocal',fontSize=8,leading=10.5,spaceAfter=0))
styles.add(ParagraphStyle(name='CellLab',fontName='ArialLocal',fontSize=9,leading=12))
story=[]
def p(text,style='BodyLab'): return Paragraph(text,styles[style])
def add(text,style='BodyLab'): story.append(p(text,style))
def heading(text): add(text,'H1Lab')
def sub(text): add(text,'H2Lab')
def page(): story.append(PageBreak())
def table(rows,widths,header=True,pad=7):
    data=[[p(html.escape(str(c)),'CellLab') for c in row] for row in rows]
    t=Table(data,colWidths=widths,hAlign='LEFT',repeatRows=1 if header else 0)
    commands=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),pad),('BOTTOMPADDING',(0,0),(-1,-1),pad),('LINEBELOW',(0,0),(-1,-1),.4,HexColor('#d0d0d0'))]
    if header: commands += [('BACKGROUND',(0,0),(-1,0),HexColor('#eeeeee'))]
    t.setStyle(TableStyle(commands));story.append(t);story.append(Spacer(1,10))
def evidence(name,title):
    sub(title)
    text=(OUT/'evidencias'/(name+'.txt')).read_text(encoding='utf-8')
    # No se altera la salida; solo se ajustan las lineas al ancho de pagina.
    import textwrap
    wrapped='\n'.join('\n'.join(textwrap.wrap(l,width=99,replace_whitespace=False,drop_whitespace=False)) if l else '' for l in text.splitlines())
    block=Preformatted(wrapped,styles['MonoLab'])
    t=Table([[block]],colWidths=[499],hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),HexColor('#f5f5f5')),('BOX',(0,0),(-1,-1),.4,HexColor('#c9c9c9')),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9)]))
    story.append(t);story.append(Spacer(1,4))

def screenshot(name,title):
    sub(title)
    image=Image(str(OUT/'evidencias'/(name+'.png')))
    ratio=745/image.imageWidth
    image.drawWidth=745
    image.drawHeight=image.imageHeight*ratio
    image.hAlign='LEFT'
    story.append(image)
    story.append(Spacer(1,5))

class AESFlow(Flowable):
    def __init__(self):
        super().__init__()
        self.width=499; self.height=555
    def draw(self):
        c=self.canv
        def arrow(x1,y1,x2,y2,dashed=False):
            c.setStrokeColor(HexColor('#555555'));c.setLineWidth(.8)
            if dashed:c.setDash(3,2)
            c.line(x1,y1,x2,y2);c.setDash()
            import math
            angle=math.atan2(y2-y1,x2-x1)
            for delta in (-.45,.45): c.line(x2,y2,x2-6*math.cos(angle+delta),y2-6*math.sin(angle+delta))
        def box(x,y,w,h,lines,shade=False):
            c.setFillColor(HexColor('#eeeeee') if shade else white);c.setStrokeColor(HexColor('#777777'))
            c.roundRect(x-w/2,y-h/2,w,h,5,stroke=1,fill=1)
            c.setFillColor(black);c.setFont('ArialLocal',9)
            top=y+(len(lines)-1)*6
            for i,line in enumerate(lines):c.drawCentredString(x,top-i*12-3,line)
        def diamond(x,y,label):
            path=c.beginPath();path.moveTo(x,y+22);path.lineTo(x+45,y);path.lineTo(x,y-22);path.lineTo(x-45,y);path.close()
            c.setFillColor(white);c.drawPath(path,stroke=1,fill=1);c.setFillColor(black);c.setFont('ArialLocal',9);c.drawCentredString(x,y-3,label)
        box(249,528,170,32,['Clave de 128 bits'],True)
        arrow(249,512,249,496)
        box(249,480,190,32,['Expansión de clave: K0 a K10'],True)
        c.setFont('ArialLocalBold',11);c.drawCentredString(118,443,'Cifrado');c.drawCentredString(374,443,'Descifrado')
        for x,inv in ((118,False),(374,True)):
            box(x,410,184,32,['Bloque cifrado de 16 bytes' if inv else 'Bloque original de 16 bytes'])
            arrow(x,394,x,374)
            box(x,358,184,32,['AddRoundKey con K10' if inv else 'AddRoundKey con K0'])
            arrow(x,342,x,320)
            box(x,304,184,32,['r = 9' if inv else 'r = 1'])
            arrow(x,288,x,269)
            lines=['InvShiftRows → InvSubBytes','AddRoundKey con Kr','InvMixColumns'] if inv else ['SubBytes → ShiftRows','MixColumns','AddRoundKey con Kr']
            box(x,241,184,56,lines)
            arrow(x,213,x,193)
            diamond(x,171,'¿r > 1?' if inv else '¿r < 9?')
            c.setFont('ArialLocal',8);c.drawString(x+48,178,'Sí')
            loopx=x+115
            c.line(x+45,171,loopx,171);c.line(loopx,171,loopx,280);arrow(loopx,280,x,280)
            c.setFont('ArialLocal',8);c.drawString(x+46,285,'r = r - 1' if inv else 'r = r + 1')
            arrow(x,149,x,126);c.drawString(x+5,137,'No')
            final=['InvShiftRows → InvSubBytes','AddRoundKey con K0'] if inv else ['SubBytes → ShiftRows','AddRoundKey con K10']
            box(x,104,184,44,final)
            arrow(x,82,x,60)
            box(x,44,184,32,['Bloque original recuperado' if inv else 'Bloque cifrado de 16 bytes'])
        # La expansion alimenta todos los AddRoundKey; se muestran las entradas iniciales.
        arrow(154,480,16,480,True);c.setDash(3,2);c.line(16,480,16,358);c.setDash();arrow(16,358,26,358,True)
        arrow(344,480,483,480,True);c.setDash(3,2);c.line(483,480,483,358);c.setDash();arrow(483,358,466,358,True)

data=json.loads((OUT/'resultados'/'resumen.json').read_text())
summary=data['resultados']; times=list(csv.DictReader((OUT/'resultados'/'tiempos.csv').open()))
lookup={(int(r['procesos']),int(r['repeticion'])):float(r['segundos']) for r in times}

add('Laboratorio 03','TitleLab')
add('Búsqueda de claves AES con Open MPI','H1Lab')
add('<b>Universidad del Valle de Guatemala</b><br/>Computación Paralela y Distribuida<br/>'+AUTHOR+' · Carné 20853<br/>Trabajo individual · 5 de octubre de 2026')
sub('Objetivo')
add('Analizar el programa secuencial de búsqueda de claves AES, corregir sus limitaciones y desarrollar una versión paralela. Comparé ambas versiones con el mismo archivo cifrado y medí su rendimiento con dos, tres y cuatro procesos.')
sub('Qué es AES y dónde se utiliza')
add('AES es un algoritmo de cifrado simétrico: la misma clave permite cifrar y descifrar. AES-128 utiliza una clave de 128 bits, bloques de 128 bits y diez rondas de transformación. [1]')
table([['Campo','Aplicación'],['Comunicaciones web','TLS 1.3 incluye AES-GCM para proteger el tráfico de conexiones HTTPS. [2]'],['Redes privadas virtuales','IPsec ESP puede utilizar AES-GCM para proteger y autenticar paquetes. [3]'],['Almacenamiento','XTS-AES se utiliza para proteger la confidencialidad de datos en dispositivos de almacenamiento. [4]']],[130,369])
sub('Transformaciones principales')
table([['Transformación','Función'],['SubBytes','Sustituye cada byte mediante una tabla no lineal.'],['ShiftRows','Desplaza las filas del estado.'],['MixColumns','Mezcla los bytes de cada columna.'],['AddRoundKey','Combina el estado y la clave de ronda mediante XOR.']],[130,369])
add('El estado organiza los 16 bytes en una matriz de 4 × 4. La expansión de clave genera las claves de ronda. Para mensajes completos también se necesita elegir un modo de operación y resolver cómo tratar la longitud del texto. [1]','SmallLab')

page();heading('Cifrado y descifrado de AES 128')
add('El diagrama muestra el procesamiento de un bloque. Las claves de ronda alimentan cada operación AddRoundKey; el descifrado las utiliza en orden inverso. La ronda final omite MixColumns y, en el sentido inverso, InvMixColumns. [1]')
story.append(AESFlow())
add('Figura 1. Flujo del algoritmo AES-128. Las flechas discontinuas muestran la intervención de la expansión de clave.','SmallLab')
add('En el programa mejorado se usa GCM: AES cifra bloques de contador y el resultado se combina con el mensaje. GCM admite longitudes que no son múltiplos de 16 y añade una etiqueta de autenticación. Por eso la operación de descifrado GCM usa internamente el cifrado AES de los contadores. [5]','SmallLab')

page();heading('Análisis del programa original')
sub('Uso correcto de AES 128')
add('El programa utiliza <b>EVP_aes_128_ecb()</b> y entrega una clave de 16 bytes. El texto “Puedes lograrlo!” ocupa exactamente 16 bytes; su terminador no se cifra. Desactivar el relleno es correcto para ese bloque. Las operaciones de cifrado y descifrado se realizan con EVP y se comprueban sus resultados. No encontré un error en la selección de AES-128.')
sub('Construcción de la clave')
add('La función <b>make_key()</b> deja ocho bytes en cero y escribe la candidata en los ocho restantes. La clave 12345 se representa como <b>00000000000000000000000000003039</b>. Su tamaño es válido para AES-128, pero su construcción es predecible. Dentro del rango del ejercicio solamente varían 20 bits.')
sub('Modo ECB')
add('ECB procesa los bloques por separado. Con una misma clave, bloques originales iguales producen bloques cifrados iguales; además, no detecta modificaciones por sí solo. En este ejemplo hay un único bloque, así que no aparecen patrones entre varios bloques, pero el modo limita la extensión del programa a mensajes reales.')
sub('Verificación mediante texto conocido')
add('La búsqueda acepta una candidata cuando <b>memcmp()</b> confirma que el texto descifrado coincide con el original. Esto es válido para un experimento con texto conocido. Su limitación es que exige disponer del mensaje esperado. <b>SECRET_KEY</b> se usa para preparar el cifrado; el ciclo de búsqueda no consulta directamente ese valor.')
sub('Espacio de claves y trabajo efectivo')
add('El rango contiene 2<super>20</super> candidatas: 1 048 576. AES-128 tiene 2<super>128</super> claves posibles, aproximadamente 3,40 × 10<super>38</super>. El laboratorio explora una fracción 2<super>-108</super> de ese espacio. Encontrar una clave construida de esta forma no significa romper AES-128.')
add('La búsqueda empieza en cero y se detiene en 12345, por lo que prueba 12 346 candidatas. En la evaluación automatizada recuperó el mensaje en <b>0,011494 s</b>; en la captura adicional, en <b>0,009547 s</b>. No se compara directamente con la versión mejorada: cambian el modo criptográfico y la cantidad de trabajo.')
sub('Medición y otras limitaciones')
add('El programa ya imprime el tiempo obtenido con <b>CLOCK_MONOTONIC</b>, después de preparar el cifrado. También reutiliza el contexto de OpenSSL. Sus principales restricciones son el mensaje fijo, la clave fija y el rango definido al compilar. La versión original se conserva sin cambios para documentar el punto de partida.')
add('Referencia al código original: make_key, líneas 46-55; crypt_block, 62-100; preparación y búsqueda, 136-154; salida del tiempo, 165-166.','SmallLab')

page();heading('Mejoras y distribución del trabajo')
add('<b>Autor de todas las mejoras:</b> '+AUTHOR+'.')
sub('Mejoras implementadas')
add('<b>1. Autenticación.</b> Reemplacé ECB por AES-128-GCM. Se genera un nonce aleatorio de 12 bytes y una etiqueta de 16 bytes. Una candidata se acepta únicamente si OpenSSL valida la etiqueta; el texto provisional se descarta cuando falla. Esto permite verificar sin guardar el texto original. [5, 6]')
add('<b>2. Preparación separada.</b> El comando <b>preparar</b> crea un archivo que contiene versión, longitud, nonce, etiqueta y texto cifrado. El comando <b>buscar</b> solo recibe ese archivo y el límite. Ni la clave secreta ni el mensaje original se guardan en el archivo.')
add('<b>3. Flexibilidad.</b> El mensaje se recibe como argumento, de 1 a 4096 bytes. La clave de prueba, el rango y el tamaño de lote MPI también son configurables. Se rechazan números negativos, entradas inválidas y archivos mal formados. El límite de búsqueda permitido es de 1 a 2<super>32</super> candidatas.')
add('<b>4. Comparación reproducible.</b> Ambas versiones comparten las rutinas de AES y leen exactamente el mismo archivo. Se conservó la reutilización del contexto EVP y se añadió el contador de candidatas. La asignación numérica de claves sigue siendo educativa: GCM no convierte ese conjunto predecible en claves seguras para producción. Un nonce no debe reutilizarse con la misma clave. [5]')
sub('Versión con Open MPI')
add('El proceso 0 lee el archivo y distribuye los datos con <b>MPI_Bcast</b>. Cada proceso tiene su propio contexto EVP y prueba lotes de candidatas. Para la ronda r, el proceso p de un grupo de n procesos recibe:')
add('<b>Inicio = (r × n + p) × B</b><br/><b>Fin exclusivo = mínimo(Inicio + B, límite)</b>')
table([['Ronda','Proceso 0','Proceso 1','Proceso 2'],['0','0 a 3','4 a 7','8 a 11'],['1','12 a 15','16','Sin candidatas']],[65,144,145,145])
add('Ejemplo: límite 17, tres procesos y lote B = 4. Los intervalos son disjuntos y cubren todas las candidatas al agotar el rango.','SmallLab')
add('Al terminar cada lote, <b>MPI_Allreduce</b> con <b>MPI_MIN</b> comunica la clave encontrada; UINT64_MAX indica que no hubo coincidencia. Todos los procesos participan, incluso quienes no tienen candidatas en la última ronda. Si alguien encuentra la clave, los demás terminan su lote actual y todos salen del ciclo. Si el rango se agota, finalizan sin resultado. Así se evita que un proceso salga antes de una operación colectiva. [7]')

page();heading('Resultados de rendimiento')
add('<b>Entorno:</b> Ubuntu 26.04.1 LTS en WSL2, Intel Core Ultra 5 125U, 14 CPU lógicas visibles y 15 GiB de memoria. GCC 15.2.0, Open MPI 5.0.10 y OpenSSL 3.5.5. Compilación con C11, -O2, -Wall, -Wextra y -Wpedantic.')
add('Usé el mensaje “Puedes lograrlo!”, el rango [0, 1 048 576), la clave 1 048 575 y lotes de 4096. En todas las ejecuciones se probaron <b>1 048 576 candidatas</b> y se recuperaron la misma clave y el mismo mensaje. La preparación del archivo y su lectura quedan fuera del tiempo de búsqueda.')
add('Se hizo un calentamiento por configuración y cinco repeticiones medidas, alternando el orden. En MPI, la medición comienza después de MPI_Barrier e incluye la búsqueda y la coordinación de parada. Se reporta el mayor tiempo entre procesos. No incluye el arranque de mpirun, la impresión ni las reducciones finales de estadísticas.')
sub('Tiempos medidos en segundos')
rows=[['Repetición','Secuencial','2 procesos','3 procesos','4 procesos']]
for i in range(1,6): rows.append([i]+[f'{lookup[n,i]:.6f}' for n in (1,2,3,4)])
table(rows,[75,106,106,106,106],pad=3)
add('<b>Speedup(n) = T<sub>secuencial</sub> / T<sub>paralelo,n</sub></b>. La siguiente tabla utiliza las medianas de los tiempos; eficiencia = speedup / n.')
rows=[['Procesos','Mediana (s)','Speedup','Eficiencia']]
for s in summary: rows.append([s['procesos'],f"{s['mediana']:.6f}",f"{s['speedup']:.3f}",f"{s['eficiencia']*100:.2f}%"])
table(rows,[95,135,135,134],pad=3)
sub('Speedup de cada repetición')
rows=[['Repetición','2 procesos','3 procesos','4 procesos']]
for i in range(1,6):rows.append([i]+[f'{lookup[1,i]/lookup[n,i]:.3f}' for n in (2,3,4)])
table(rows,[95,135,135,134],pad=3)
add('Cuatro procesos dieron el mejor resultado: <b>3,087 veces</b> el rendimiento secuencial, equivalente a una reducción aproximada del 67,6% del tiempo mediano. Tres procesos no mejoraron respecto de dos. La variación entre repeticiones, la planificación de WSL y los costos de sincronización pueden explicar este comportamiento. El speedup ligeramente superior a dos con dos procesos no demuestra escalamiento superlineal sostenido.','SmallLab')

story.append(NextPageTemplate('Landscape'))
page();heading('Capturas de compilación y ejecución')
add('Capturas tomadas en Ubuntu desde Windows Terminal. Esta sesión adicional verifica la compilación y los resultados; las cinco repeticiones de la evaluación se conservan en la tabla de rendimiento y en los registros originales.','SmallLab')
screenshot('01_compilacion','Compilación de los tres programas sin advertencias')
screenshot('02_original','Programa secuencial original')
screenshot('04_secuencial','Programa secuencial mejorado')
add('El original recupera 12345. La versión mejorada prueba 1 048 576 candidatas y recupera 1048575, con el mensaje esperado y autenticación correcta.','SmallLab')

page();heading('Evidencia de ejecución con Open MPI')
add('Las tres ejecuciones recuperaron la clave 1048575 y el mensaje <b>Puedes lograrlo!</b>, con autenticación correcta.','SmallLab')
screenshot('05_mpi_2','Dos procesos')
screenshot('05_mpi_3','Tres procesos')
screenshot('05_mpi_4','Cuatro procesos')
capture_times={1:1.056688770,2:0.574145790,3:0.541838446,4:0.516579520}
rows=[['Procesos','Tiempo de la captura (s)','Speedup de esta sesión']]
for n in (2,3,4):rows.append([n,f'{capture_times[n]:.9f}',f'{capture_times[1]/capture_times[n]:.3f}'])
table(rows,[100,325,320],pad=3)
add('Base de estos speedups: secuencial mejorada de la captura, 1,056688770 s. Esta sesión se presenta por separado de las medianas de la evaluación automatizada.','SmallLab')

story.append(NextPageTemplate('Portrait'))
page();heading('Verificación y archivos entregados')
add('El script <b>evaluar.py</b> terminó con <b>17 comprobaciones funcionales aprobadas</b>, además de validar las 20 ejecuciones medidas. El registro completo se conserva en <b>07_pruebas_completas.txt</b>.')
table([['Prueba','Resultado'],['Vector de respuesta conocida AES-128-GCM','Cifrado, etiqueta y descifrado coinciden con el vector.'],['Claves al inicio, en medio y al final','Misma clave y mensaje en secuencial y MPI.'],['Reparto irregular y procesos sin trabajo','Finalización correcta con rangos no divisibles y más procesos que candidatas.'],['Rango agotado','Se prueban exactamente 17 candidatas; salida 2.'],['Etiqueta alterada','Ninguna versión acepta el mensaje como válido.'],['Longitudes de 1 y 4096 bytes','Recuperación y autenticación correctas.'],['Entradas inválidas y archivo inexistente','Salida de error controlada; MPI termina sin bloqueo.']],[190,309])
sub('Contenido de la entrega')
add('<b>programas:</b> secuencial original, secuencial mejorado, versión MPI, cabecera compartida, Makefile, test_aes.c y evaluar.py.<br/><b>resultados:</b> datos.aes, tiempos.csv, resumen.json y tiempos_capturas.csv.<br/><b>evidencias:</b> seis capturas y registros completos de comandos y resultados.<br/><b>README.md:</b> instrucciones para compilar, ejecutar y repetir las pruebas.')
sub('Referencias')
refs=[
('1','NIST. FIPS 197, Advanced Encryption Standard, actualización 2023.','https://csrc.nist.gov/pubs/fips/197/final'),
('2','IETF. RFC 8446, TLS 1.3, 2018; sección 9.1.','https://www.rfc-editor.org/rfc/rfc8446.html#section-9.1'),
('3','IETF. RFC 4106, AES-GCM en IPsec ESP, 2005.','https://www.rfc-editor.org/rfc/rfc4106.html'),
('4','NIST. SP 800-38E, XTS-AES para dispositivos de almacenamiento, 2010.','https://csrc.nist.gov/pubs/sp/800/38/e/final'),
('5','NIST. SP 800-38D, GCM y GMAC, 2007.','https://csrc.nist.gov/pubs/sp/800/38/d/final'),
('6','OpenSSL. EVP_EncryptInit, operaciones de cifrado autenticado.','https://docs.openssl.org/3.1/man3/EVP_EncryptInit/'),
('7','Open MPI. MPI_Allreduce, manual de la API.','https://docs.open-mpi.org/en/main/man-openmpi/man3/MPI_Allreduce.3.html')]
for num,title,url in refs:add(f'[{num}] {title}<br/><link href="{html.escape(url)}" color="#222222">{html.escape(url)}</link>','SmallLab')
add('Fuentes consultadas el 5 de octubre de 2026. El programa original y la consigna fueron proporcionados como material del laboratorio.','SmallLab')

def decorate(c,doc):
    c.saveState();c.setFont('ArialLocal',8);c.setFillColor(HexColor('#555555'))
    c.drawString(48,28,'Laboratorio 03 · '+AUTHOR+' · 20853')
    c.drawRightString(c._pagesize[0]-48,28,str(doc.page));c.restoreState()
doc=BaseDocTemplate(str(OUT/'Laboratorio_03_Carlos_Estrada_20853.pdf'),pagesize=A4,rightMargin=48,leftMargin=48,topMargin=43,bottomMargin=46,title='Laboratorio 03 - Búsqueda de claves AES con Open MPI',author=AUTHOR)
doc.addPageTemplates([
    PageTemplate(id='Portrait',frames=[Frame(48,46,A4[0]-96,A4[1]-89,id='normal')],pagesize=A4,onPage=decorate),
    PageTemplate(id='Landscape',frames=[Frame(48,46,landscape(A4)[0]-96,landscape(A4)[1]-89,id='wide')],pagesize=landscape(A4),onPage=decorate)
])
doc.build(story)
print('PDF generado.')
