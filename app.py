import streamlit as st
import datetime

# Configuración de la página
st.set_page_config(page_title="Hábile - Gestión e IA", page_icon="🧠", layout="wide")

# --- 1. SISTEMA DE USUARIOS Y AUTENTICACIÓN ---
# ¡Aquí es donde creas los nuevos usuarios, mi cielo! 
# Solo debes seguir el formato "usuario": "contraseña". Puedes agregar los que quieras.
USUARIOS_REGISTRADOS = {
    "katty": "profesora2026",
    "robin": "destiny5070",
    "tahia": "mama123",
    "carolina": "terapeuta2026",  # <--- Ejemplo de nuevo usuario
    "andrea": "psicologa2026"     # <--- Ejemplo de otro nuevo usuario
}

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = ""

def cerrar_sesion():
    st.session_state.autenticado = False
    st.session_state.usuario_actual = ""
    st.rerun()

# --- 2. BASE DE DATOS SIMULADA POR USUARIO ---
# Aseguramos que si agregas un usuario arriba, el sistema le cree su espacio automáticamente
if "datos_usuarios" not in st.session_state:
    st.session_state.datos_usuarios = {}

# Inicializar dinámicamente los datos para cada usuario registrado
for user in USUARIOS_REGISTRADOS.keys():
    if user not in st.session_state.datos_usuarios:
        # Datos por defecto para Katty (para que no aparezca vacío al probar)
        if user == "katty":
            st.session_state.datos_usuarios[user] = {
                "pacientes": {
                    "Facundo": {"edad": 8, "objetivo": "Mejorar la comprensión lectora y atención", "perfil": "Muestra gran interés por los cuentos, pero se distrae a los 10 minutos."},
                    "Gaspar": {"edad": 8, "objetivo": "Desarrollar habilidades de grafomotricidad", "perfil": "Creativo, prefiere actividades visuales. Requiere apoyo en la pinza fina."}
                },
                "citas": [
                    {"hora": "09:00", "paciente": "Facundo", "motivo": "Sesión Semanal"},
                    {"hora": "11:30", "paciente": "Gaspar", "motivo": "Evaluación Motriz"}
                ]
            }
        # Datos por defecto para Robin
        elif user == "robin":
            st.session_state.datos_usuarios[user] = {
                "pacientes": {
                    "Lucas": {"edad": 10, "objetivo": "Potenciar el pensamiento lógico-matemático", "perfil": "Muy hábil con la tecnología, responde bien a dinámicas gamificadas."}
                },
                "citas": [
                    {"hora": "15:00", "paciente": "Lucas", "motivo": "Refuerzo Académico"}
                ]
            }
        # Los usuarios nuevos parten con su agenda y pacientes limpios para que ellos los creen
        else:
            st.session_state.datos_usuarios[user] = {
                "pacientes": {},
                "citas": []
            }

# --- 3. LÓGICA DE LA IA MEJORADA (Ahora más flexible) ---
def respuesta_ia(consulta, paciente_nombre, usuario):
    consulta_clean = consulta.lower()
    pacientes_usuario = st.session_state.datos_usuarios[usuario]["pacientes"]
    paciente_info = pacientes_usuario.get(paciente_nombre, {"objetivo": "Desarrollo integral", "perfil": "Sin historial previo"})
    
    # Identificar el día que pide el usuario (busca cualquier coincidencia)
    dia = "Martes"
    for d in ["lunes", "martes", "miércoles", "miercoles", "jueves", "viernes", "sábado", "sabado"]:
        if d in consulta_clean:
            dia = d.capitalize()
            if dia == "Miercoles": dia = "Miércoles"
            if dia == "Sabado": dia = "Sábado"

    # Respuesta inteligente multiuso
    return f"""
    🤖 **Planificador IA Hábile:** He procesado tu solicitud para el día **{dia}** enfocada en el paciente **{paciente_nombre}**.
    
    * **Enfoque terapéutico:** Teniendo en cuenta su objetivo principal (*"{paciente_info['objetivo']}"*), he diseñado el siguiente bloque de intervención.
    
    **Cronograma de Actividades Recomendado:**
    1.  **Inicio (10 min) - Enfoque y Conexión:** Actividad lúdica rompehielo de baja frustración. Si el perfil lo requiere, usar apoyos visuales o un juego de atención rápida.
    2.  **Desarrollo (25 min) - Trabajo Central:** Ejercicio segmentado en pasos cortos. Trabajar directamente en el desarrollo de sus habilidades mediante modelamiento y refuerzo positivo.
    3.  **Cierre (10 min) - Consolidación:** Preguntas de metacognición ("¿Qué aprendimos hoy?") y entrega de un estímulo o refuerzo por su esfuerzo.
    
    *💡 Sugerencia del asistente:* Basado en su perfil (*"{paciente_info['perfil']}"*), evita las jornadas muy largas sin pausas y mantén un tono de voz dulce y cercano para asegurar su motivación.
    """

# --- 4. PANTALLA DE LOGIN ---
if not st.session_state.autenticado:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h2 style='text-align: center;'>🔐 Iniciar Sesión</h2>", unsafe_allow_html=True)
        st.write("Por favor, ingresa tus credenciales para acceder a tu agenda personalizada.")
        
        usuario_input = st.text_input("Usuario").strip().lower()
        contrasena_input = st.text_input("Contraseña", type="password")
        
        if st.button("Ingresar a la Plataforma", use_container_width=True):
            if usuario_input in USUARIOS_REGISTRADOS and USUARIOS_REGISTRADOS[usuario_input] == contrasena_input:
                st.session_state.autenticado = True
                st.session_state.usuario_actual = usuario_input
                st.success(f"¡Bienvenido/a, {usuario_input.capitalize()}!")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos. Intenta de nuevo, sol.")
else:
    # --- 5. APLICACIÓN PRINCIPAL ---
    usuario = st.session_state.usuario_actual
    mis_pacientes = st.session_state.datos_usuarios[usuario]["pacientes"]
    mis_citas = st.session_state.datos_usuarios[usuario]["citas"]
    
    st.sidebar.markdown(f"### 👤 Cuenta: **{usuario.capitalize()}**")
    if st.sidebar.button("Cerrar Sesión 🚪"):
        cerrar_sesion()
        
    st.sidebar.divider()
    menu = st.sidebar.radio("Navegación", ["📅 Mi Agenda", "📝 Informes y Objetivos", "🤖 Asistente IA"])
    
    st.title("🧠 Panel de Gestión Terapéutica e IA")
    st.caption(f"Sesión activa para el profesional: {usuario.capitalize()}")
    
    # --- MÓDULO: MI AGENDA ---
    if menu == "📅 Mi Agenda":
        st.header("Mis Horarios y Citas del Día")
        
        # Formulario para agregar citas en tiempo real
        with st.expander("➕ Agregar Nueva Cita a la Agenda"):
            nueva_hora = st.text_input("Hora (Ej: 16:00)")
            nuevo_pac = st.text_input("Nombre del Paciente/Alumno")
            nuevo_mot = st.text_input("Motivo de la sesión")
            if st.button("Agendar"):
                if nueva_hora and nuevo_pac:
                    st.session_state.datos_usuarios[usuario]["citas"].append({"hora": nueva_hora, "paciente": nuevo_pac, "motivo": nuevo_mot})
                    st.success("¡Cita agendada!")
                    st.rerun()
        
        if len(mis_citas) == 0:
            st.info("No tienes citas programadas para hoy.")
        else:
            col1, col2 = st.columns(2)
            for i, cita in enumerate(mis_citas):
                with col1 if i % 2 == 0 else col2:
                    st.info(f"⏰ **{cita['hora']}** | **Paciente:** {cita['paciente']} \n\n *Motivo:* {cita['motivo']}")
                    
        st.divider()
        st.header("Mis Pacientes Asignados")
        
        # Formulario para agregar pacientes en tiempo real
        with st.expander("➕ Registrar Nuevo Paciente/Alumno"):
            p_nombre = st.text_input("Nombre Completo")
            p_edad = st.number_input("Edad", min_value=1, max_value=100, value=8)
            p_obj = st.text_area("Objetivo Principal de Intervención")
            p_perf = st.text_area("Perfil o Diagnóstico Inicial")
            if st.button("Registrar Paciente"):
                if p_nombre:
                    st.session_state.datos_usuarios[usuario]["pacientes"][p_nombre] = {"edad": p_edad, "objetivo": p_obj, "perfil": p_perf}
                    st.success(f"¡{p_nombre} registrado con éxito!")
                    st.rerun()

        if len(mis_pacientes) == 0:
            st.warning("Aún no tienes pacientes registrados en tu cuenta.")
        else:
            for nombre, datos in mis_pacientes.items():
                with st.expander(f"👤 {nombre} (Edad: {datos['edad']} años)"):
                    st.write(f"**Perfil Inicial:** {datos['perfil']}")
                    st.write(f"**Objetivo Principal:** {datos['objetivo']}")
                    
    # --- MÓDULO: INFORMES Y OBJETIVOS ---
    elif menu == "📝 Informes y Objetivos":
        st.header("Creación de Objetivos e Informes")
        
        if len(mis_pacientes) == 0:
            st.warning("Debes registrar pacientes en la pestaña 'Mi Agenda' para usar este módulo, cielo.")
        else:
            paciente_sel = st.selectbox("Selecciona un Paciente", list(mis_pacientes.keys()))
            info_paciente = mis_pacientes[paciente_sel]
            
            tab1, tab2 = st.tabs(["🎯 Modificar Objetivos", "📄 Redactar Informe"])
            
            with tab1:
                st.subheader(f"Objetivo Actual para {paciente_sel}")
                nuevo_obj = st.text_area("Editar Objetivo Terapéutico:", value=info_paciente["objective"] if "objective" in info_paciente else info_paciente["objetivo"])
                if st.button("Guardar Objetivo"):
                    st.session_state.datos_usuarios[usuario]["pacientes"][paciente_sel]["objetivo"] = nuevo_obj
                    st.success("¡Objetivo actualizado con éxito!")
                    
            with tab2:
                st.subheader(f"Informe - {paciente_sel}")
                st.text_input("Título del Informe", value="Informe de Avance Trimestral")
                st.text_area("Escribe observaciones...", height=150)
                if st.button("Guardar Borrador"):
                    st.success("Informe guardado localmente.")
                    
    # --- MÓDULO: ASISTENTE IA ---
    elif menu == "🤖 Asistente IA":
        st.header("Asistente Virtual de Habilidades")
        st.write("Pídele a la IA que estructure tu día. Ella leerá los objetivos del paciente seleccionado para armarte las actividades.")
        
        if len(mis_pacientes) == 0:
            st.warning("Registra al menos un paciente en 'Mi Agenda' para poder consultar a la IA.")
        else:
            paciente_ia = st.selectbox("¿Sobre qué paciente vas a consultar?", list(mis_pacientes.keys()))
            prompt_usuario = st.text_input("¿En qué te ayudo hoy, corazón?", placeholder="Ej: Hazme el desarrollo de actividades para el día martes")
            
            if st.button("Consultar a la IA ✨"):
                if prompt_usuario:
                    with st.spinner("Generando plan de actividades..."):
                        resultado = respuesta_ia(prompt_usuario, paciente_ia, usuario)
                        st.markdown(resultado)
                else:
                    st.warning("Escribe una pregunta para tu asistente, sol.")
