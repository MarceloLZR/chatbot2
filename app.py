import streamlit as st
import os
from groq import Groq
from apikey import groq_apikey  # Asegúrate de tener este archivo con tu clave de API de Groq

def main():
    # Configuración de la página
    st.set_page_config(page_title="Asistente Médico", page_icon="🩺", layout="wide")

    # Estilos CSS personalizados
      # Estilos CSS personalizados
    # Estilos CSS personalizados
    st.markdown("""
        <style>
            [data-testid="stAppViewContainer"] {
                background-color: #ffffff !important;
            }
            
            [data-testid="stHeader"] {
                background-color: #bbdefb !important;
                border-bottom: 1px solid #90caf9;
            }
            
            [data-testid="stSidebar"] {
                background-color: #ffffff !important;
                border-right: 1px solid #90caf9;
            }
            
            .stButton>button {
                background-color: #1976d2 !important;
                color: white !important;
                border: none !important;
                border-radius: 5px !important;
            }
            
            h1, h2, h3 {
                color: #1976d2 !important;
            }
            
            /* Estilos para inputs y selectboxes */
            .stTextInput>div>div>input, 
            .stTextArea>div>div>textarea,
            .stNumberInput>div>div>input,
            .stSelectbox>div>div>div {
                background-color: #f5f5f5 !important;
                border: 1px solid #90caf9 !important;
                color: #000000 !important;
            }

            /* Estilos específicos para las etiquetas de edad y género */
            .stNumberInput>label, .stSelectbox>label {
                color: #1976d2 !important;
                font-size: 2.2rem !important;
                font-weight: bold !important;
                margin-bottom: 8px !important;
            }
            
            /* Estilos para el texto del select */
            .stSelectbox>div>div>div {
                background-color: #f5f5f5 !important;
                color: #000000 !important;
            }
            
            .stTextInput>div>div>input::placeholder,
            .stTextArea>div>div>textarea::placeholder {
                color: #64b5f6 !important;
            }
            
            a {
                color: #1976d2 !important;
            }
            
            .stMarkdown {
                color: #000000 !important;
            }
            
            .warning-box {
                background-color: #bbdefb;
                border-left: 5px solid #1976d2;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 15px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Configuración del cliente Groq
    try:
        client = Groq(api_key=groq_apikey)
    except Exception as e:
        st.error(f"Error al inicializar Groq: {e}")
        return

    # Navegación de la barra lateral
    with st.sidebar:
        st.title("🩺 Asistente Médico")
        
        # Selección de página
        page = st.sidebar.selectbox("Selecciona un Servicio", [
            "Análisis de Medicamentos", 
            "Medicamentos Comunes", 
            "Verificador de Síntomas"
        ])

        # Información de la barra lateral
        st.markdown("""
        ### Sobre Este Asistente
        Este asistente médico proporciona:
        - Información de medicamentos
        - Guías de medicamentos comunes
        - Análisis de síntomas
        
        ### ⚠️ Limitaciones Importantes
        - No sustituye el consejo médico profesional
        - No puede proporcionar diagnósticos definitivos
        - Solo con fines informativos
        
        ### 🚨 En Caso de Emergencia
        Contacte inmediatamente a servicios de emergencia o visite el centro médico más cercano.
        """)

        # Botón para limpiar conversación
        if st.button("🗑️ Limpiar Conversación"):
            st.session_state.messages = []
            st.rerun()

    # Función para generar respuestas
    def generar_respuesta(prompt, mensaje_sistema):
        try:
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": mensaje_sistema},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )
            return completion.choices[0].message.content
        except Exception as e:
            st.error(f"Error al generar respuesta: {e}")
            return "No se pudo generar una respuesta."

    # Sección de Análisis de Medicamentos
    if page == "Análisis de Medicamentos":
        st.title("🔬 Análisis de Imagen de Medicamentos")
        
        st.markdown("""
        <div class="warning-box">
        📷 Sube una imagen de un medicamento para obtener información detallada.
        </div>
        """, unsafe_allow_html=True)

        archivo_subido = st.file_uploader("Elige una imagen de medicamento", type=["jpg", "png", "jpeg"])
        
        if archivo_subido is not None:
            # Mostrar la imagen subida
            st.image(archivo_subido, caption='Medicamento Subido', use_column_width=True)
            
            # Extraer el nombre del archivo
            nombre_archivo = archivo_subido.name
            
            
            mensaje_sistema = (
                "Eres un asistente especializado en identificar medicamentos a partir de descripciones detalladas. "
                "Proporciona información completa sobre las características, usos y precauciones del medicamento basándote en el nombre del archivo."
            )
            
            if st.button("Analizar Medicamento"):
                # Simular análisis utilizando el nombre del archivo
                respuesta = generar_respuesta(
                    f"Analiza el medicamento con este nombre: {nombre_archivo}. Proporciona información detallada (como usarlo, contraindicaciones, dosis, etc) pero no hagas referencia al nombre completo, por ejemplo panadol.jpg, solo centrate en panadol.", 
                    mensaje_sistema
                )
                st.markdown("### Detalles del Medicamento")
                st.write(respuesta)


    # Sección de Medicamentos Comunes
    elif page == "Medicamentos Comunes":
        st.title("💊 Guía de Medicamentos Comunes")
        
        categoria_medicamento = st.selectbox(
            "Selecciona la Categoría de Medicamento",
            [
                "Analgésicos", 
                "Antibióticos", 
                "Antiinflamatorios", 
                "Medicamentos Cardíacos"
            ]
        )

        if st.button("Obtener Información de Medicamentos"):
            mensaje_sistema = (
                "Proporciona información clara y concisa sobre medicamentos comunes "
                "en la categoría especificada. Incluye nombres genéricos, usos, precauciones "
                "y efectos secundarios comunes."
            )
            
            respuesta = generar_respuesta(
                f"Proporciona información detallada sobre medicamentos comunes en la categoría de {categoria_medicamento}.", 
                mensaje_sistema
            )
            
            st.markdown("### Información de Medicamentos")
            st.write(respuesta)
            
            st.markdown("""
            <div class="warning-box">
            ⚠️ Siempre consulte a un profesional de la salud antes de tomar cualquier medicamento.
            </div>
            """, unsafe_allow_html=True)

    # Sección de Verificador de Síntomas
    elif page == "Verificador de Síntomas":
        st.title("🩺 Análisis de Síntomas")
        
        st.markdown("""
        <div class="warning-box">
        📝 Describe tus síntomas en detalle para obtener información relevante.Cuanto más específico seas, más precisa será la información.
        </div>
        """, unsafe_allow_html=True)

        sintomas = st.text_area(
            "Describe tus síntomas en detalle", 
            help="Cuanto más específico seas, más precisa será la información."
        )
        
        col1, col2 = st.columns(2)
        with col1:
            edad = st.number_input("Edad", min_value=0, max_value=120, value=30)
        with col2:
            genero = st.selectbox("Género", ["Masculino", "Femenino", "Otro"])

        if st.button("Analizar Síntomas"):
            mensaje_sistema = (
                "Eres un asistente médico que proporciona información general sobre posibles "
                "condiciones médicas basadas en síntomas. TU RESPUESTA ES PURAMENTE INFORMATIVA "
                "Y NO UN DIAGNÓSTICO MÉDICO PROFESIONAL. Siempre recomienda consultar "
                "a un médico para un diagnóstico preciso."
            )
            
            respuesta = generar_respuesta(
                f"Tengo {edad} años, soy {genero}. Mis síntomas son: {sintomas}. "
                "Proporciona información general sobre posibles condiciones médicas, "
                "pero enfatiza que esto NO es un diagnóstico definitivo.", 
                mensaje_sistema
            )
            
            st.markdown("### Análisis de Síntomas")
            st.write(respuesta)
            
            st.markdown("""
            <div class="warning-box">
            🚨 ADVERTENCIA IMPORTANTE: Esta información NO sustituye la consulta médica profesional.
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
