import imaplib
import email
import quopri
import re

def get_body(tmsg):    
    body = ""
    if tmsg.is_multipart():        
        for part in tmsg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))    
            # skip any text/plain (txt) attachments
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = str(part.get_payload(decode=True))  # decode
                body=body.replace("\\r\\n","\n")
                break
    # not multipart - i.e. plain text, no attachments, keeping fingers crossed
    else:
        body = str(tmsg.get_payload(decode=True))
    body=body.replace("\xc3\xb3", "ó")
    body=body.replace("\xc3\xa9", "é")
    return body

def get_emailinfo(id, data, bshowbody=False):
    
    for contenido in data:
        # comprueba que 'contenido' sea una tupla, si es así continua
        if isinstance(contenido, tuple):                    
            # recuperamos información del email:            
            msg = email.message_from_string(contenido[1].decode())
            if(bshowbody):
                    #print ("--------------------------------------------------------")
                    a,b,c=extraer_texto(get_body(msg))
                    print("El correo es: ", a)
                    print("El telefono es: ", b)
                    print("El curso es: ", c)
                    #print ("--------------------------------------------------------")
            return True
    # si no hay info
    return False

def get_emails(gmailsmtpsvr, gmailusr, gmailpwd, bshowbody):
    try:
        # Conectamos a nuestro servidor gmail, que utiliza la subclase IMAP4_SSL
        mail = imaplib.IMAP4_SSL(gmailsmtpsvr)
        # logamos:
        mail.login(gmailusr, gmailpwd)
        # seleccionamos bandeja de entrada 'inbox'
        mail.select("inbox")
        # recuperamos lista de emails, es posible filtrar la consulta
            # ALL devuelve todos los emails
            # Ejemplo de filtro: '(FROM "coordinacion.virtual@camarasal.com" SUBJECT "ejemplo python")'        
        #result, data = mail.search(None, 'ALL')
        result, data = mail.search(None, 'FROM "coordinacion.virtual@camarasal.com"')
        # coge lista de ids encontrados
        strids = data[0]
        lstids = strids.split()
        # recuperamos valores para bucle
        firstid = int(lstids[0])
        lastid = int(lstids[-1])
        countid = 0
        # mostramos datos de los ids encontrados
        #print("primer id: %d\nultimo id: %d\n..." % (firstid, lastid))
        # recorremos lista de mayor a menor (mas recientes primero)
        for id in range(lastid, firstid-1, -1):            
            typ, data = mail.fetch(str(id), '(RFC822)' ) # el parámetro id esperado es tipo cadena
            if (get_emailinfo(id, data, bshowbody)):
                countid+=1
        # fin, si llegamos aqui todo es correcto
        print("emails listados %d" % countid)
    except Exception as e:
        print("Error: %s" % (e))
        return ""
    except:
        print("Error desconocido")
        return ""

el_texto = """Nuevo pedido: #4010

Has recibido el siguiente pedido de Maria Imelda Zaldivar Hercules:

[Pedido #4010]<https://camarasal.com/wp-admin/post.php?post=4010&action=edit> (24 de julio de 2023)
Producto
Cantidad
Precio
Congreso de Mujer y Liderazgo
1
$70.00
Subtotal:
$70.00
Descuento:
-$10.00
M\xc3\xa9todo de pago:
Tarjeta de cr\xc3\xa9dito con WOMPI
Total:
$60.00 (incluye $6.90 Impuesto)

Sexo: Femenino

DUI: 028111663

Cargo: Gerente de Finanzas

Direcci\xc3\xb3n de facturaci\xc3\xb3n
Maria Imelda Zaldivar Hercules
Sociedad de Ahorro y Cr\xc3\xa9dito Apoyo Integral, S.A.
47 Av Sur y Almd Roosevelt Col Flor Blanca
San Salvador
2250-6003<tel:22506003>
imelda.zaldivar@integral.com.sv<mailto:imelda.zaldivar@integral.com.sv>

Enhorabuena por la venta.
Procesa tus pedidos sobre la marcha. Consigue la aplicaci\xc3\xb3n<https://woocommerce.com/mobile?blog_id=0&utm_campaign=deeplinks_promote_app&utm_medium=email&utm_source=camarasal.com&utm_term=0>.

C\xc3\xa1mara de Comercio e Industria de El Salvador \xe2\x80\x94 Built with WooCommerce<https://woocommerce.com>"""

def extraer_texto(texto):
    var_correo = ""
    var_telefono = []
    var_curso = ""
    patron_correo = r'<mailto:([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})>'
    patron_telefono = r'\b(\d{4}[-.]?\d{4})|<tel:(\d{8})>\b'
    posicion_inicio = texto.find("Precio")
    posicion_final = next((i for i, c in enumerate(texto[posicion_inicio:]) if c.isdigit()), None) + posicion_inicio
    resultado_correo = re.search(patron_correo, texto)
    resultados_telefono = re.findall(patron_telefono, texto)
    
    if resultado_correo:
        correo_encontrado = resultado_correo.group(0)
        var_correo = re.search(r'mailto:(.*)>', correo_encontrado).group(1)
    else:
        var_correo = ""

    if resultados_telefono:
        for telefono in resultados_telefono:
            telefono_encontrado = "".join(telefono)
            var_telefono.append(telefono_encontrado)
    else:
        var_telefono = ""
        
    var_curso = texto[posicion_inicio+6:posicion_final].strip()
    return var_correo,var_telefono,var_curso
    

def test():    
    mitexto=get_emails("smtp.gmail.com", "virtual.camarasal@gmail.com", "omrasqvasswkwwqc", True);

test()
#a,b,c = extraer_texto(el_texto)
