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
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = str(part.get_payload(decode=True))  # decode
                body=body.replace("\\r\\n","\n")
                break
    else:
        body = str(tmsg.get_payload(decode=True))
    body=body.replace("\xc3\xb3", "ó")
    body=body.replace("\xc3\xa9", "é")
    return body

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
    
def inbox():
    gmailsmtpsvr = "smtp.gmail.com"
    gmailusr = "virtual.camarasal@gmail.com"
    gmailpwd = "omrasqvasswkwwqc"
    bshowbody = True
    try:
        mail = imaplib.IMAP4_SSL(gmailsmtpsvr)
        mail.login(gmailusr, gmailpwd)
        mail.select("inbox")
        result, data = mail.search(None, 'FROM "coordinacion.virtual@camarasal.com"')
        strids = data[0]
        lstids = strids.split()
        firstid = int(lstids[0])
        lastid = int(lstids[-1])
        countid = 0
        for id in range(lastid, firstid-1, -1):            
            typ, data = mail.fetch(str(id), '(RFC822)' ) # el parámetro id esperado es tipo cadena
            #id, data, bshowbody=False
            for contenido in data:
                if isinstance(contenido, tuple):
                    msg = email.message_from_string(contenido[1].decode())
                    a,b,c=extraer_texto(get_body(msg))
            countid+=1
    except Exception as e:
        print("Error: %s" % (e))
        return "","",""
    except:
        print("Error desconocido")
        return "","",""

    return a,b,c
    
a = inbox()
print(a)