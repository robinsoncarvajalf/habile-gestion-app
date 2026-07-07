import streamlit as st
import datetime

# Configuración de la página
st.set_page_config(page_title="Hábile - Gestión e IA", page_icon="🧠", layout="wide")

# --- 1. SISTEMA DE USUARIOS Y AUTENTICACIÓN ---
USUARIOS_REGISTRADOS = {
    "katty": "profesora2026",
    "robin": "destiny5070",
    "tahia": "mama123"
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
if "datos_usuarios" not in st.session_state:
    st.session_state.datos_usuarios = {
        "katty": {
            "pacientes": {
                "Facundo": {"edad": 8, "objetivo": "Mejorar la comprensión lectora y atención", "perfil": "Muestra gran interés por los cuentos, pero se distrae a los 10 minutos."},
                "Gaspar": {"edad": 8, "objetivo": "Desarrollar habilidades de grafomotricidad", "perfil": "Creativo, prefiere actividades visuales. Requiere apoyo en la pinza fina."}
            },
            "citas": [
                {"hora": "09:00", "paciente": "Facundo", "motivo": "Sesión Semanal"},
                {"hora": "11:30", "paciente": "Gaspar", "motivo": "Evaluación Motriz"}
            ]
        },
        "robin": {
            "pacientes": {
                "Lucas": {"edad": 10, "objetivo": "Potenciar el pensamiento lógico-matemático", "perfil": "Muy hábil con la tecnología, responde bien a dinámicas gamificadas."}
            },
            "citas": [
                {"hora": "15:00", "paciente": "Lucas", "motivo": "Refuerzo Académico"}
            ]
        },
        "tahia": {
            "pacientes": {},
            "citas": []
        }
    }

# --- 3. LÓGICA DE LA MINI IA ---
def respuesta_ia(consulta, paciente_nombre, usuario):
    consulta_clean = consulta.lower()
    pacientes_usuario = st.session_state.datos_usuarios[usuario]["pacientes"]
    paciente_info = pacientes_usuario.get(paciente_nombre, {"objetivo": "General", "perfil": ""})
    
    if "actividades para el" in consulta_clean or "desarrollo de actividades" in consulta_clean:
        dia = "martes"
        for d in ["lunes", "martes", "miércoles", "jueves", "viernes"]:
            if d in consulta_clean:
                dia = d
                
        return f"""
        🤖 **Planificador IA:** Aquí tienes la propuesta para el **{dia.capitalize()}** para el paciente **{paciente_nombre}**:
        
        *   **Objetivo a trabajar:** {paciente_info['objetivo']}.
        
        **Cronograma Sugerido:**
        1.  **00-10 min (Inicio/Activación):** Dinámica de inicio rápido acorde a su perfil.
        2.  **10-30 min (Desarrollo Central):** Actividad enfocada en: *"{paciente_info['objetivo']}"*.
        3.  **30-40 min (Cierre):** Metacognición y refuerzo positivo.
        
        *Consejo de la IA:* Basado en el perfil: *"{paciente_info['perfil']}"*, te sugiero adaptar los estímulos visuales.
        """
    else:
        return f"🤖 **Asistente IA:** Hola. Estoy lista para ayudarte con {paciente_nombre} y su objetivo de '{paciente_info['objetivo']}'. ¿Qué necesitas armar hoy?"

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
        
        if len(mis_citas) == 0:
            st.info("No tienes citas programadas para hoy.")
        else:
            col1, col2 = st.columns(2)
            for i, cita in enumerate(mis_citas):
                with col1 if i % 2 == 0 else col2:
                    st.info(f"⏰ **{cita['hora']}** | **Paciente:** {cita['paciente']} \n\n *Motivo:* {cita['motivo']}")
                    
        st.divider()
        st.header("Mis Pacientes Asignados")
        if len(mis_pacientes) == 0:
            st.warning("Aún no tienes pacientes registrados.")
        else:
            for nombre, datos in mis_pacientes.items():
                with st.expander(f"👤 {nombre} (Edad: {datos['edad']} años)"):
                    st.write(f"**Perfil Inicial:** {datos['perfil']}")
                    st.write(f"**Objetivo Principal:** {datos['objetivo']}")
                    
    # --- MÓDULO: INFORMES Y OBJETIVOS ---
    elif menu == "📝 Informes y Objetivos":
        st.header("Creación de Objetivos e Informes")
        
        if len(mis_pacientes) == 0:
            st.warning("Debes tener pacientes registrados para usar este módulo.")
        else:
            paciente_sel = st.selectbox("Selecciona un Paciente", list(mis_pacientes.keys()))
            info_paciente = mis_pacientes[paciente_sel]
            
            tab1, tab2 = st.tabs(["🎯 Modificar Objetivos", "📄 Redactar Informe"])
            
            with tab1:
                st.subheader(f"Objetivo Actual para {paciente_sel}")
                nuevo_obj = st.text_area("Editar Objetivo Terapéutico:", value=info_paciente["objetivo"])
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
        
        if len(mis_pacientes) == 0:
            st.warning("Registra al menos un paciente para poder consultar a la IA.")
        else:
            paciente_ia = st.selectbox("¿Sobre qué paciente vas a consultar?", list(mis_pacientes.keys()))
            prompt_usuario = st.text_input("¿En qué te ayudo hoy?", placeholder="Ej: Hazme el desarrollo de actividades para el día martes")
            
            if st.button("Consultar a la IA ✨"):
                if prompt_usuario:
                    with st.spinner("Generando plan de actividades..."):
                        resultado = respuesta_ia(prompt_usuario, paciente_ia, usuario)
                        st.markdown(resultado)
                else:
                    st.warning("Escribe una pregunta para tu asistente.")
