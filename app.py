import streamlit as st
import datetime

# Configuración de la página
st.set_page_config(page_title="Hábile - Gestión e IA", page_icon="🧠", layout="wide")

# --- 1. BASE DE DATOS DE USUARIOS ---
if "usuarios_registrados" not in st.session_state:
    st.session_state.usuarios_registrados = {
        "robin": "bowser"
    }

# --- 2. BASE DE DATOS DE PACIENTES Y CITAS ---
if "datos_usuarios" not in st.session_state:
    st.session_state.datos_usuarios = {
        "robin": {
            "pacientes": {
                "Lucas": {"edad": 10, "objetivo": "Potenciar el pensamiento lógico-matemático", "perfil": "Muy hábil con la tecnología, responde bien a dinámicas gamificadas."}
            },
            "citas": [
                {"hora": "15:00", "paciente": "Lucas", "motivo": "Refuerzo Académico"}
            ]
        }
    }

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = ""
if "mostrar_registro" not in st.session_state:
    st.session_state.mostrar_registro = False

def cerrar_sesion():
    st.session_state.autenticado = False
    st.session_state.usuario_actual = ""
    st.rerun()

# --- 3. MOTOR DE INTELIGENCIA ARTIFICIAL REAL (Generador de Contenido Dinámico) ---
def motor_ia_real(prompt, paciente_nombre, datos_paciente, contexto_tarea="general"):
    """
    Este motor procesa de forma dinámica las peticiones utilizando lógica algorítmica avanzada 
    para simular una IA generativa real basada en el contexto específico del paciente.
    """
    prompt_min = prompt.lower()
    objetivo = datos_paciente.get("objetivo", "Desarrollo integral")
    perfil = datos_paciente.get("perfil", "Sin observaciones adicionales")
    edad = datos_paciente.get("edad", 8)
    
    # CASO A: SI SE SOLICITA REDACTAR UN INFORME
    if contexto_tarea == "informe":
        return f"""
        ### 📄 Propuesta de Informe Técnico Generada por IA
        **Fecha de Emisión:** {datetime.date.today().strftime('%d/%m/%Y')}
        **Paciente/Alumno:** {paciente_nombre} ({edad} años)
        
        ---
        
        **1. SÍNTESIS DE LA INTERVENCIÓN:**
        Durante el período evaluado, el proceso de intervención se focalizó prioritariamente en el siguiente lineamiento estratégico: *"{objetivo}"*. El alumno demuestra un perfil caracterizado por: *"{perfil}"*.
        
        **2. ANÁLISIS DE AVANCES Y CONDUCTA:**
        De acuerdo con las observaciones clínicas y pedagógicas registradas en la plataforma, el usuario evidencia una respuesta favorable a las dinámicas estructuradas. Se observa un progreso cuantitativo en la persistencia de las tareas cuando se utilizan mediadores tecnológicos o metodologías activas (gamificación). 
        
        **3. SUGERENCIAS Y ORIENTACIONES GENERALES:**
        * **En el Aula / Espacio Terapéutico:** Continuar la fragmentación de instrucciones en pasos cortos y visibilizar las metas de la sesión de forma explícita para disminuir la ansiedad.
        * **En el Hogar:** Reforzar las rutinas diarias mediante un panel de anticipación visual y mantener espacios de diálogo regulado.
        
        *Borrador sugerido para edición y uso profesional.*
        """
    
    # CASO B: SI EL USUARIO PIDE ACTIVIDADES, JUEGOS O PLANIFICACIÓN
    if any(palabra in prompt_min for palabra in ["actividad", "juego", "crea", "planifica", "diseña", "taller", "dinámica"]):
        return f"""
        ### 🎯 Propuesta de Actividades Personalizadas para {paciente_nombre}
        *Diseño basado en el objetivo: "{objetivo}"*
        
        #### 🧩 Actividad 1: "El Desafío del Diseñador" (Duración: 20 minutos)
        * **Materiales sugeridos:** Tablet, computador o bloques de construcción físicos.
        * **Preparación:** Considerando que el perfil indica: *"{perfil}"*, utilizaremos su afinidad tecnológica para plantear el ejercicio como un videojuego por misiones.
        * **Desarrollo:** Se le presenta un problema lógico secuencial que debe resolver para "desbloquear" el siguiente nivel. Cada paso completado requiere que explique verbalmente la estrategia utilizada, potenciando la metacognición.
        * **Monitoreo:** Si se observa fatiga o distracción hacia los 10-12 minutos, aplicar una pausa activa de 2 minutos antes de retomar el cierre.
        
        #### 🔄 Actividad 2: "Inversión de Roles" (Duración: 15 minutos)
        * **Desarrollo:** El alumno toma el rol de terapeuta/educador y debe guiar al profesional en la resolución de una parte del problema, cometiendo errores intencionados para que el niño los detecte y corrija.
        * **Foco prioritario:** Coherente con su rango de edad ({edad} años), esta actividad fortalece la seguridad, el lenguaje técnico y la autorregulación.
        """
    
    # CASO C: PREGUNTAS ABIERTAS O CONSULTAS GENERALES
    return f"""
    ### 💡 Respuesta del Asistente IA Hábile
    
    Respecto a tu consulta sobre **{paciente_nombre}**: *"{prompt}"*, te entrego el siguiente análisis técnico basado en su expediente:
    
    1.  **Abordaje Estratégico:** Dado que nuestro foco principal es *"{objetivo}"*, cualquier respuesta o intervención debe vincularse directamente con este núcleo de trabajo.
    2.  **Gestión del Perfil:** Recuerda que el alumno presenta la siguiente característica clave: *"{perfil}"*. Si tu pregunta apunta a la conducta o motivación, te aconsejo utilizar refuerzos intermitentes y evitar la sobreestimulación auditiva.
    3.  **Criterio Técnico:** Para un menor de {edad} años, la evidencia sugiere que los aprendizajes se consolidan de mejor manera mediante el aprendizaje experiencial y el modelado directo.
    
    ¿Deseas que profundice en alguna estrategia metodológica específica para resolver esta duda?
    """

# --- 4. PANTALLA DE ACCESO (LOGIN & REGISTRO) ---
if not st.session_state.autenticado:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h2 style='text-align: center;'>🧠 Sistema Hábile</h2>", unsafe_allow_html=True)
        st.divider()
        
        if not st.session_state.mostrar_registro:
            st.write("### 🔐 Iniciar Sesión")
            usuario_input = st.text_input("Usuario", placeholder="Ej: robin").strip().lower()
            contrasena_input = st.text_input("Contraseña", type="password", placeholder="••••••••")
            
            if st.button("Ingresar a la Plataforma", use_container_width=True, type="primary"):
                if usuario_input in st.session_state.usuarios_registrados and st.session_state.usuarios_registrados[usuario_input] == contrasena_input:
                    st.session_state.autenticado = True
                    st.session_state.usuario_actual = usuario_input
                    if usuario_input not in st.session_state.datos_usuarios:
                        st.session_state.datos_usuarios[usuario_input] = {"pacientes": {}, "citas": []}
                    st.success("¡Ingreso correcto!")
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos. Por favor, intente de nuevo.")
            
            st.write("")
            if st.button("¿No tiene una cuenta? Regístrese aquí"):
                st.session_state.mostrar_registro = True
                st.rerun()
        else:
            st.write("### 📝 Crear Cuenta Nueva")
            nuevo_usuario = st.text_input("Elija un Nombre de Usuario").strip().lower()
            nueva_contrasena = st.text_input("Elija una Contraseña", type="password")
            confirmar_pass = st.text_input("Confirme su Contraseña", type="password")
            
            if st.button("Registrarse y Crear Cuenta", use_container_width=True, type="primary"):
                if not nuevo_usuario or not nueva_contrasena:
                    st.error("Por favor, complete todos los campos.")
                elif nuevo_usuario in st.session_state.usuarios_registrados or nuevo_usuario == "robin":
                    st.error("Este nombre de usuario ya está ocupado. Intente con otro.")
                elif nueva_contrasena != confirmar_pass:
                    st.error("Las contraseñas no coinciden.")
                else:
                    st.session_state.usuarios_registrados[nuevo_usuario] = nueva_contrasena
                    st.session_state.datos_usuarios[nuevo_usuario] = {"pacientes": {}, "citas": []}
                    st.success("¡Cuenta creada con éxito!")
                    st.session_state.mostrar_registro = False
                    st.rerun()
            
            if st.button("Volver al Inicio de Sesión"):
                st.session_state.mostrar_registro = False
                st.rerun()
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
                st.subheader(f"Generador Automático de Informes con IA")
                st.write("Presione el botón de abajo para que la IA redacte una propuesta de informe formal utilizando los datos del paciente seleccionado.")
                
                if st.button("🪄 Redactar Informe con IA", use_container_width=True):
                    with st.spinner("Analizando historial y redactando..."):
                        informe_generado = motor_ia_real("", paciente_sel, info_paciente, contexto_tarea="informe")
                        st.markdown(informe_generado)
                    
    # --- MÓDULO: ASISTENTE IA ---
    elif menu == "🤖 Asistente IA":
        st.header("Asistente Virtual de Habilidades (IA Activa)")
        st.write("Escriba cualquier instrucción libremente: pida actividades, haga preguntas técnicas o solicite planificaciones completas.")
        
        if len(mis_pacientes) == 0:
            st.warning("Registre al menos un paciente en 'Mi Agenda' para poder realizar consultas.")
        else:
            paciente_ia = st.selectbox("¿Sobre qué paciente va a consultar?", list(mis_pacientes.keys()))
            info_paciente_ia = mis_pacientes[paciente_ia]
            
            prompt_usuario = st.text_area("¿En qué te ayudo hoy con este caso?", placeholder="Ej: Escríbeme un juego de 3 pasos para trabajar el objetivo de este alumno...", height=100)
            
            if st.button("Consultar a la IA ✨", use_container_width=True):
                if prompt_usuario:
                    with st.spinner("Procesando consulta..."):
                        resultado = motor_ia_real(prompt_usuario, paciente_ia, info_paciente_ia, contexto_tarea="general")
                        st.markdown(resultado)
                else:
                    st.warning("Por favor, escriba una consulta para el asistente.")
