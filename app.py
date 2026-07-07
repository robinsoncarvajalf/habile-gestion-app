import streamlit as st
import datetime

# Configuración de la página
st.set_page_config(page_title="Hábile - Gestión e IA", page_icon="🧠", layout="wide")

# --- 1. BASE DE DATOS DE USUARIOS (Inicialización) ---
# Creamos un diccionario en el estado de la sesión para que guarde los usuarios nuevos
if "usuarios_registrados" not in st.session_state:
    st.session_state.usuarios_registrados = {
        "katty": "educacion2026",
        "robin": "gestion5070",
        "tahia": "clinica123"
    }

# --- 2. BASE DE DATOS DE PACIENTES Y CITAS ---
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
        }
    }

# Variables de control para el inicio de sesión
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = ""

def cerrar_sesion():
    st.session_state.autenticado = False
    st.session_state.usuario_actual = ""
    st.rerun()

# --- 3. LÓGICA DE LA IA ASISTENTE ---
def respuesta_ia(consulta, paciente_nombre, usuario):
    consulta_clean = consulta.lower()
    pacientes_usuario = st.session_state.datos_usuarios[usuario]["pacientes"]
    paciente_info = pacientes_usuario.get(paciente_nombre, {"objetivo": "Desarrollo integral", "perfil": "Sin historial previo"})
    
    dia = "Martes"
    for d in ["lunes", "martes", "miércoles", "miercoles", "jueves", "viernes", "sábado", "sabado"]:
        if d in consulta_clean:
            dia = d.capitalize()
            if dia == "Miercoles": dia = "Miércoles"
            if dia == "Sabado": dia = "Sábado"

    return f"""
    🤖 **Planificador IA Hábile:** He procesado tu solicitud para el día **{dia}** enfocada en el paciente **{paciente_nombre}**.
    
    * **Enfoque de Intervención:** Teniendo en cuenta su objetivo principal (*"{paciente_info['objetivo']}"*), se sugerirá el siguiente diseño de sesión.
    
    **Cronograma de Actividades Recomendado:**
    1.  **Inicio (10 min) - Enfoque y Conexión:** Actividad lúdica introductoria de baja frustración. Utilizar apoyos visuales o dinámicas de atención rápida según el caso.
    2.  **Desarrollo (25 min) - Trabajo Central:** Ejercicio estructurado y segmentado en pasos cortos. Enfocado directamente en el desarrollo de la habilidad mediante modelamiento.
    3.  **Cierre (10 min) - Consolidación:** Espacio de metacognición ("¿Qué aprendimos hoy?") y entrega de refuerzo positivo por el esfuerzo realizado.
    
    *Sugerencia técnica:* Basado en el perfil registrado (*"{paciente_info['perfil']}"*), se recomienda evitar bloques extensos sin pausas activas para asegurar la motivación.
    """

# --- 4. PANTALLA DE ACCESO (LOGIN & REGISTRO) ---
if not st.session_state.autenticado:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h2 style='text-align: center;'>🧠 Sistema Hábile</h2>", unsafe_allow_html=True)
        
        # Creamos dos pestañas: una para entrar y otra para registrarse
        tab_login, tab_registro = st.tabs(["🔐 Iniciar Sesión", "📝 Crear Cuenta Nueva"])
        
        # PESTAÑA 1: INICIAR SESIÓN
        with tab_login:
            st.write("Ingrese sus credenciales para acceder a su panel.")
            usuario_input = st.text_input("Usuario", key="login_user").strip().lower()
            contrasena_input = st.text_input("Contraseña", type="password", key="login_pass")
            
            if st.button("Ingresar a la Plataforma", use_container_width=True):
                if usuario_input in st.session_state.usuarios_registrados and st.session_state.usuarios_registrados[usuario_input] == contrasena_input:
                    st.session_state.autenticado = True
                    st.session_state.usuario_actual = usuario_input
                    # Asegurar que el usuario tenga su espacio de datos creado
                    if usuario_input not in st.session_state.datos_usuarios:
                        st.session_state.datos_usuarios[usuario_input] = {"pacientes": {}, "citas": []}
                    st.success(f"Bienvenido/a, {usuario_input.capitalize()}.")
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos. Por favor, intente de nuevo.")
                    
        # PESTAÑA 2: CREAR CUENTA NUEVA
        with tab_registro:
            st.write("Regístrese para obtener su propia agenda privada.")
            nuevo_usuario = st.text_input("Elija un Nombre de Usuario", key="reg_user").strip().lower()
            nueva_contrasena = st.text_input("Elija una Contraseña", type="password", key="reg_pass")
            confirmar_pass = st.text_input("Confirme su Contraseña", type="password", key="reg_pass_conf")
            
            if st.button("Registrarse y Crear Cuenta", use_container_width=True):
                if not nuevo_usuario or not nueva_contrasena:
                    st.error("Por favor, complete todos los campos.")
                elif nuevo_usuario in st.session_state.usuarios_registrados:
                    st.error("Este nombre de usuario ya está ocupado. Intente con otro.")
                elif nueva_contrasena != confirmar_pass:
                    st.error("Las contraseñas no coinciden.")
                else:
                    # Guardar el nuevo usuario en el sistema
                    st.session_state.usuarios_registrados[nuevo_usuario] = nueva_contrasena
                    # Crear su base de datos vacía inmediatamente
                    st.session_state.datos_usuarios[nuevo_usuario] = {"pacientes": {}, "citas": []}
                    st.success("¡Cuenta creada con éxito! Ahora puede ir a la pestaña 'Iniciar Sesión' e ingresar.")

else:
    # --- 5. APLICACIÓN PRINCIPAL (SÓLO PARA USUARIOS AUTENTICADOS) ---
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
        
        with st.expander("➕ Agregar Nueva Cita a la Agenda"):
            nueva_hora = st.text_input("Hora (Ej: 16:00)")
            nuevo_pac = st.text_input("Nombre del Paciente/Alumno")
            nuevo_mot = st.text_input("Motivo de la sesión")
            if st.button("Agendar"):
                if nueva_hora and nuevo_pac:
                    st.session_state.datos_usuarios[usuario]["citas"].append({"hora": nueva_hora, "paciente": nuevo_pac, "motivo": nuevo_mot})
                    st.success("Cita agendada correctamente.")
                    st.rerun()
        
        if len(mis_citas) == 0:
            st.info("No tiene citas programadas para el día de hoy.")
        else:
            col1, col2 = st.columns(2)
            for i, cita in enumerate(mis_citas):
                with col1 if i % 2 == 0 else col2:
                    st.info(f"⏰ **{cita['hora']}** | **Paciente:** {cita['paciente']} \n\n *Motivo:* {cita['motivo']}")
                    
        st.divider()
        st.header("Mis Pacientes Asignados")
        
        with st.expander("➕ Registrar Nuevo Paciente/Alumno"):
            p_nombre = st.text_input("Nombre Completo")
            p_edad = st.number_input("Edad", min_value=1, max_value=100, value=8)
            p_obj = st.text_area("Objetivo Principal de Intervención")
            p_perf = st.text_area("Perfil o Diagnóstico Inicial")
            if st.button("Registrar Paciente"):
                if p_nombre:
                    st.session_state.datos_usuarios[usuario]["pacientes"][p_nombre] = {"edad": p_edad, "objetivo": p_obj, "perfil": p_perf}
                    st.success(f"Paciente {p_nombre} registrado con éxito.")
                    st.rerun()

        if len(mis_pacientes) == 0:
            st.warning("Aún no registra pacientes en su cuenta.")
        else:
            for nombre, datos in mis_pacientes.items():
                with st.expander(f"👤 {nombre} (Edad: {datos['edad']} años)"):
                    st.write(f"**Perfil Inicial:** {datos['perfil']}")
                    st.write(f"**Objetivo Principal:** {datos['objetivo']}")
                    
    # --- MÓDULO: INFORMES Y OBJETIVOS ---
    elif menu == "📝 Informes y Objetivos":
        st.header("Creación de Objetivos e Informes")
        
        if len(mis_pacientes) == 0:
            st.warning("Debe registrar pacientes en la pestaña 'Mi Agenda' para utilizar este módulo.")
        else:
            paciente_sel = st.selectbox("Selecciona un Paciente", list(mis_pacientes.keys()))
            info_paciente = mis_pacientes[paciente_sel]
            
            tab1, tab2 = st.tabs(["🎯 Modificar Objetivos", "📄 Redactar Informe"])
            
            with tab1:
                st.subheader(f"Objetivo Actual para {paciente_sel}")
                nuevo_obj = st.text_area("Editar Objetivo Terapéutico:", value=info_paciente["objetivo"])
                if st.button("Guardar Objetivo"):
                    st.session_state.datos_usuarios[usuario]["pacientes"][paciente_sel]["objetivo"] = nuevo_obj
                    st.success("Objetivo actualizado con éxito.")
                    
            with tab2:
                st.subheader(f"Informe - {paciente_sel}")
                st.text_input("Título del Informe", value="Informe de Avance Trimestral")
                st.text_area("Escribe observaciones...", height=150)
                if st.button("Guardar Borrador"):
                    st.success("Informe guardado de manera local.")
                    
    # --- MÓDULO: ASISTENTE IA ---
    elif menu == "🤖 Asistente IA":
        st.header("Asistente Virtual de Habilidades")
        st.write("Solicite a la IA la estructura de su jornada. El sistema analizará los objetivos del caso seleccionado para diseñar el cronograma.")
        
        if len(mis_pacientes) == 0:
            st.warning("Registre al menos un paciente en 'Mi Agenda' para poder realizar consultas.")
        else:
            paciente_ia = st.selectbox("¿Sobre qué paciente va a consultar?", list(mis_pacientes.keys()))
            prompt_usuario = st.text_input("Ingrese su requerimiento:", placeholder="Ej: Desarrollar actividades para el día martes")
            
            if st.button("Consultar a la IA ✨"):
                if prompt_usuario:
                    with st.spinner("Generando planificación de actividades..."):
                        resultado = respuesta_ia(prompt_usuario, paciente_ia, usuario)
                        st.markdown(resultado)
                else:
                    st.warning("Por favor, escriba una consulta para el asistente.")
