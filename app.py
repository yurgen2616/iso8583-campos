from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

campos_iso8583 = ["mapa de los bits extendidos", "numero de cuenta principal pan", "codigo de procesamiento",
                  "monto de transaccion", "monto de liquidacion", "monto de facturacion al titular de la tarjeta",
                  "fecha y hora de transmision", "monto, tarifa de facturacion al titular de la tarjeta",
                  "tasa de conversion, liquidacion", "tasa de conversion, facturacion al titular de la tarjeta",
                  "numero de auditoria de seguimiento de sistema", "hora de transaccion local", "fecha de transaccion local",
                  "fecha de vencimiento de la tarjeta", "fecha de liquidacion", "fecha de conversion", "fecha de captura",
                  "tipo de comerciante", "codigo de pais de la institucion adquiriente", "pan extendido, codigo de pais",
                  "institucion expedidora, codigo de pais", "modo de entrada de punto de servicio", "numero de pan de la aplicacion",
                  "codigo funcion (iso 8583 de 1993) identificador de red", "codigo condicion de punto de servicio",
                  "codigo captura de punto de servicio", "autorizacion longitud de respuesta de identificacion",
                  "monto, tarifa de transaccion", "monto, tarifa de liquidacion", "monto, tarifa de procesamiento de transaccion",
                  "monto, tarifa de procesamiento de liquidacion", "adquirir codigo de identificacion de la institucion",
                  "codigo de identificacion de la institucion remitente", "numero de cuenta principal, extendido",
                  "numero de pista 2 track 2", "numero de pista 3 track 3", "numero de referencia de recuperacion",
                  "respuesta de identificacion de autorizacion", "codigos de respuesta", "codigo de restriccion de servicio",
                  "identificacion de terminal del aceptador de tarjeta", "codigo de identificacion del aceptador de tarjeta",
                  "nombre ubicacion del aceptador de tarjeta", "datos adicionales", "numero de pista 1 track 1",
                  "datos adicionales iso", "datos adicionales nacional", "datos adicionales privado", "codigo de moneda de transaccion",
                  "codigo de moneda de liquidacion", "codigo de moneda de facturacion del titular de la tarjeta", "datos de numero de identifiacion personal",
                  "informacion de control en referencia a la seguridad", "cantidades adicionales", "iso reservado icc", "iso reservado",
                  "nacional reservado", "nacional reservado", "nacional reservado", "aviso | codigo de motivo nacional reservado", "privado reservado", "privado reservado",
                  "privado reservado", "codigo de autentificacion de mensajes mac"]

diccionario_campos = {campo: numero for numero, campo in enumerate(campos_iso8583, start=1)}

def iniciar_preguntas():
    campos_pendientes = campos_iso8583.copy()
    random.shuffle(campos_pendientes)
    preguntas = [{'campo': campo, 'tipo_pregunta': random.choice(["numero", "texto"])} for campo in campos_pendientes]
    session['preguntas'] = preguntas
    session['indice'] = 0
    session['correctas'] = 0
    session['incorrectas'] = 0

@app.route('/')
def index():
    if 'preguntas' not in session:
        iniciar_preguntas()

    preguntas = session['preguntas']
    indice = session['indice']

    if indice >= len(preguntas):
        return redirect(url_for('completado'))

    pregunta_actual = preguntas[indice]
    session['indice'] += 1

    if pregunta_actual['tipo_pregunta'] == "numero":
        pregunta = f"¿A qué número corresponde lo siguiente: {pregunta_actual['campo']}?"
    else:
        pregunta = f"¿Cuál es el nombre del campo correspondiente al número {diccionario_campos[pregunta_actual['campo']]}?"

    respuesta_correcta = diccionario_campos[pregunta_actual['campo']] if pregunta_actual['tipo_pregunta'] == "numero" else pregunta_actual['campo']
    session['respuesta_correcta'] = str(respuesta_correcta)

    return render_template('index.html', pregunta=pregunta, correctas=session.get('correctas', 0), incorrectas=session.get('incorrectas', 0))

@app.route('/responder', methods=['POST'])
def responder():
    respuesta = request.form['respuesta']
    respuesta_correcta = session.get('respuesta_correcta')

    es_correcto = (respuesta.lower() == respuesta_correcta.lower())

    if es_correcto:
        session['correctas'] = session.get('correctas', 0) + 1
    else:
        session['incorrectas'] = session.get('incorrectas', 0) + 1

    return render_template('respuesta.html', es_correcto=es_correcto, respuesta_correcta=respuesta_correcta)

@app.route('/completado')
def completado():
    return render_template('completado.html', correctas=session.get('correctas', 0), incorrectas=session.get('incorrectas', 0))

@app.route('/reiniciar')
def reiniciar():
    iniciar_preguntas()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
