import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
import math
import time

class DetectorSenasGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Detector de Señas LSC")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2C3E50')
        
        # Variables
        self.cap = None
        self.is_running = False
        self.current_frame = None
        
        # Variables para medir tiempo de respuesta
        self.detection_times = []
        self.last_detection_time = 0
        self.current_sign = "?"
        self.sign_start_time = None
        self.last_translated_sign = "Ninguna"
        self.last_sign_timestamp = ""
        
        # Variables para formar palabras
        self.current_word = ""
        self.word_history = []
        self.last_added_sign = ""
        self.sign_hold_time = 0
        self.sign_hold_threshold = 1.5  # segundos para confirmar una letra
        
        # MediaPipe setup
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Crear interfaz
        self.create_widgets()
        
    def create_widgets(self):
        # Título
        title_label = tk.Label(
            self.root, 
            text="🤟 Detector de Señas LSC 🤟", 
            font=("Arial", 24, "bold"), 
            bg='#2C3E50', 
            fg='#ECF0F1'
        )
        title_label.pack(pady=10)
        
        # Panel para formar palabras
        word_panel = tk.Frame(self.root, bg='#34495E', relief=tk.RAISED, bd=2)
        word_panel.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Título del panel de palabras
        word_title = tk.Label(word_panel, text="📝 Formador de Palabras", 
                            font=("Arial", 16, "bold"), bg='#34495E', fg='#ECF0F1')
        word_title.pack(pady=5)
        
        # Frame para la palabra actual
        word_display_frame = tk.Frame(word_panel, bg='#34495E')
        word_display_frame.pack(fill=tk.X, pady=5, padx=20)
        
        tk.Label(word_display_frame, text="Palabra actual:", 
                font=("Arial", 12), bg='#34495E', fg='#BDC3C7').pack(side=tk.LEFT)
        
        self.current_word_var = tk.StringVar(value="")
        word_entry = tk.Entry(word_display_frame, textvariable=self.current_word_var,
                            font=("Arial", 18, "bold"), bg='#ECF0F1', fg='#2C3E50',
                            width=30, justify=tk.CENTER, state='readonly')
        word_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Frame para controles de palabras
        word_controls = tk.Frame(word_panel, bg='#34495E')
        word_controls.pack(pady=5, padx=20)
        
        # Botones de control
        self.add_letter_button = tk.Button(word_controls, text="➕ Agregar Letra", 
                                         command=self.add_current_letter,
                                         font=("Arial", 10), bg='#27AE60', fg='white', width=12)
        self.add_letter_button.pack(side=tk.LEFT, padx=5)
        
        self.add_space_button = tk.Button(word_controls, text="␣ Espacio", 
                                        command=self.add_space,
                                        font=("Arial", 10), bg='#3498DB', fg='white', width=10)
        self.add_space_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = tk.Button(word_controls, text="⌫ Borrar", 
                                     command=self.delete_last_letter,
                                     font=("Arial", 10), bg='#E74C3C', fg='white', width=10)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = tk.Button(word_controls, text="🗑️ Limpiar", 
                                    command=self.clear_word,
                                    font=("Arial", 10), bg='#95A5A6', fg='white', width=10)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        self.save_word_button = tk.Button(word_controls, text="💾 Guardar", 
                                        command=self.save_word,
                                        font=("Arial", 10), bg='#9B59B6', fg='white', width=10)
        self.save_word_button.pack(side=tk.LEFT, padx=5)
        
        # Indicador de progreso para agregar letra
        self.progress_frame = tk.Frame(word_panel, bg='#34495E')
        self.progress_frame.pack(fill=tk.X, pady=2, padx=20)
        
        self.progress_var = tk.StringVar(value="Mantén la seña por 1.5 segundos para agregar la letra")
        progress_label = tk.Label(self.progress_frame, textvariable=self.progress_var,
                                font=("Arial", 9), bg='#34495E', fg='#F39C12')
        progress_label.pack()
        
        # Lista de palabras guardadas
        history_frame = tk.Frame(word_panel, bg='#34495E')
        history_frame.pack(fill=tk.X, pady=5, padx=20)
        
        tk.Label(history_frame, text="Palabras guardadas:", 
                font=("Arial", 10), bg='#34495E', fg='#BDC3C7').pack(side=tk.LEFT)
        
        self.word_history_var = tk.StringVar(value="Ninguna")
        history_label = tk.Label(history_frame, textvariable=self.word_history_var,
                               font=("Arial", 10), bg='#34495E', fg='#1ABC9C',
                               wraplength=600, justify=tk.LEFT)
        history_label.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Frame izquierdo para video
        video_frame = tk.Frame(main_frame, bg='#34495E', relief=tk.RAISED, bd=2)
        video_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Label para el video
        self.video_label = tk.Label(video_frame, bg='#34495E', text="Presiona 'Iniciar' para comenzar")
        self.video_label.pack(expand=True, padx=10, pady=10)
        
        # Frame derecho para información
        info_frame = tk.Frame(main_frame, bg='#34495E', relief=tk.RAISED, bd=2, width=350)
        info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        info_frame.pack_propagate(False)
        
        # Título del panel de información
        info_title = tk.Label(
            info_frame, 
            text="Información de Detección", 
            font=("Arial", 16, "bold"), 
            bg='#34495E', 
            fg='#ECF0F1'
        )
        info_title.pack(pady=10)
        
        # Seña detectada
        self.sena_var = tk.StringVar(value="Ninguna")
        sena_frame = tk.Frame(info_frame, bg='#34495E')
        sena_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(sena_frame, text="Seña Detectada:", font=("Arial", 12, "bold"), 
                bg='#34495E', fg='#ECF0F1').pack()
        self.sena_display = tk.Label(sena_frame, textvariable=self.sena_var, 
                                   font=("Arial", 36, "bold"), 
                                   bg='#27AE60', fg='white', relief=tk.RAISED, bd=3)
        self.sena_display.pack(pady=5, fill=tk.X)
        
        # Estados de dedos
        estados_frame = tk.LabelFrame(info_frame, text="Estados de Dedos", 
                                    font=("Arial", 11, "bold"), 
                                    bg='#34495E', fg='#ECF0F1')
        estados_frame.pack(pady=8, padx=10, fill=tk.X)
        
        self.estados_var = tk.StringVar(value="No detectados")
        tk.Label(estados_frame, textvariable=self.estados_var, 
                font=("Arial", 10), bg='#34495E', fg='#BDC3C7', wraplength=300, justify=tk.LEFT).pack(pady=5)
        
        # Direcciones de dedos
        direcciones_frame = tk.LabelFrame(info_frame, text="Direcciones de Dedos", 
                                        font=("Arial", 11, "bold"), 
                                        bg='#34495E', fg='#ECF0F1')
        direcciones_frame.pack(pady=8, padx=10, fill=tk.X)
        
        self.direcciones_var = tk.StringVar(value="No detectadas")
        tk.Label(direcciones_frame, textvariable=self.direcciones_var, 
                font=("Arial", 10), bg='#34495E', fg='#BDC3C7', wraplength=300, justify=tk.LEFT).pack(pady=5)
        
        # Última seña traducida
        ultima_sena_frame = tk.LabelFrame(info_frame, text="Última Seña Traducida", 
                                        font=("Arial", 11, "bold"), 
                                        bg='#34495E', fg='#ECF0F1')
        ultima_sena_frame.pack(pady=8, padx=10, fill=tk.X)
        
        self.ultima_sena_var = tk.StringVar(value="Ninguna")
        self.timestamp_var = tk.StringVar(value="--:--:--")
        
        # Frame para la última seña
        sena_info_frame = tk.Frame(ultima_sena_frame, bg='#34495E')
        sena_info_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(sena_info_frame, text="Seña:", font=("Arial", 9), 
                bg='#34495E', fg='#BDC3C7', width=6, anchor='w').pack(side=tk.LEFT)
        tk.Label(sena_info_frame, textvariable=self.ultima_sena_var, 
                font=("Arial", 14, "bold"), bg='#34495E', fg='#1ABC9C', anchor='w').pack(side=tk.LEFT)
        
        # Frame para el timestamp
        time_info_frame = tk.Frame(ultima_sena_frame, bg='#34495E')
        time_info_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(time_info_frame, text="Hora:", font=("Arial", 9), 
                bg='#34495E', fg='#BDC3C7', width=6, anchor='w').pack(side=tk.LEFT)
        tk.Label(time_info_frame, textvariable=self.timestamp_var, 
                font=("Arial", 10), bg='#34495E', fg='#95A5A6', anchor='w').pack(side=tk.LEFT)
        
        # Métricas de tiempo de respuesta
        tiempo_frame = tk.LabelFrame(info_frame, text="Tiempo de Respuesta", 
                                   font=("Arial", 11, "bold"), 
                                   bg='#34495E', fg='#ECF0F1')
        tiempo_frame.pack(pady=8, padx=10, fill=tk.X)
        
        self.tiempo_deteccion_var = tk.StringVar(value="0.00 ms")
        self.tiempo_promedio_var = tk.StringVar(value="0.00 ms")
        self.fps_var = tk.StringVar(value="0 FPS")
        
        # Frame para última detección
        ultimo_frame = tk.Frame(tiempo_frame, bg='#34495E')
        ultimo_frame.pack(fill=tk.X, pady=2)
        tk.Label(ultimo_frame, text="Última:", font=("Arial", 9), 
                bg='#34495E', fg='#BDC3C7', width=8, anchor='w').pack(side=tk.LEFT)
        tk.Label(ultimo_frame, textvariable=self.tiempo_deteccion_var, 
                font=("Arial", 11, "bold"), bg='#34495E', fg='#F39C12', anchor='w').pack(side=tk.LEFT)
        
        # Frame para promedio
        promedio_frame = tk.Frame(tiempo_frame, bg='#34495E')
        promedio_frame.pack(fill=tk.X, pady=2)
        tk.Label(promedio_frame, text="Promedio:", font=("Arial", 9), 
                bg='#34495E', fg='#BDC3C7', width=8, anchor='w').pack(side=tk.LEFT)
        tk.Label(promedio_frame, textvariable=self.tiempo_promedio_var, 
                font=("Arial", 11, "bold"), bg='#34495E', fg='#3498DB', anchor='w').pack(side=tk.LEFT)
        
        # Frame para FPS
        fps_frame = tk.Frame(tiempo_frame, bg='#34495E')
        fps_frame.pack(fill=tk.X, pady=2)
        tk.Label(fps_frame, text="FPS:", font=("Arial", 9), 
                bg='#34495E', fg='#BDC3C7', width=8, anchor='w').pack(side=tk.LEFT)
        tk.Label(fps_frame, textvariable=self.fps_var, 
                font=("Arial", 11, "bold"), bg='#34495E', fg='#E74C3C', anchor='w').pack(side=tk.LEFT)
        
        # Lista de señas disponibles
        lista_frame = tk.LabelFrame(info_frame, text="Señas Disponibles", 
                                  font=("Arial", 11, "bold"), 
                                  bg='#34495E', fg='#ECF0F1')
        lista_frame.pack(pady=8, padx=10, fill=tk.BOTH, expand=True)
        
        senas_text = "A, B, D, E, F, I, K, L\nM, N, U, V, W, X, Y"
        tk.Label(lista_frame, text=senas_text, 
                font=("Arial", 12), bg='#34495E', fg='#BDC3C7', 
                justify=tk.CENTER).pack(pady=10)
        
        # Frame de controles
        controls_frame = tk.Frame(self.root, bg='#2C3E50')
        controls_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Botones
        self.start_button = tk.Button(
            controls_frame, 
            text="▶ Iniciar", 
            command=self.start_detection,
            font=("Arial", 12, "bold"),
            bg='#27AE60', 
            fg='white', 
            width=12,
            relief=tk.RAISED,
            bd=3
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(
            controls_frame, 
            text="⏹ Detener", 
            command=self.stop_detection,
            font=("Arial", 12, "bold"),
            bg='#E74C3C', 
            fg='white', 
            width=12,
            state=tk.DISABLED,
            relief=tk.RAISED,
            bd=3
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.exit_button = tk.Button(
            controls_frame, 
            text="❌ Salir", 
            command=self.exit_app,
            font=("Arial", 12, "bold"),
            bg='#95A5A6', 
            fg='white', 
            width=12,
            relief=tk.RAISED,
            bd=3
        )
        self.exit_button.pack(side=tk.RIGHT, padx=5)
        
        # Barra de estado
        self.status_var = tk.StringVar(value="Listo para comenzar")
        status_bar = tk.Label(
            self.root, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            bg='#BDC3C7', 
            fg='#2C3E50'
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def dedos_curvados(self, landmarks, umbral=0.07):
        curvados = 0
        dedos = [(5,8), (9,12), (13,16), (17,20)]
        for base, tip in dedos:
            x1, y1 = landmarks.landmark[base].x, landmarks.landmark[base].y
            x2, y2 = landmarks.landmark[tip].x, landmarks.landmark[tip].y
            distancia = math.sqrt((x2-x1)**2 + (y2-y1)**2)
            if distancia < umbral:
                curvados += 1
        return curvados >= 4

    def indice_semidoblado(self, landmarks):
        base_y = landmarks.landmark[6].y
        medio_y = landmarks.landmark[7].y
        punta_y = landmarks.landmark[8].y
        
        distancia_base_punta = abs(base_y - punta_y)
        distancia_medio_base = abs(medio_y - base_y)
        
        return (punta_y < base_y and distancia_medio_base < distancia_base_punta * 0.7)

    def get_finger_directions(self, landmarks):
        directions = []
        
        if landmarks.landmark[4].y < landmarks.landmark[3].y:
            directions.append('up')
        elif landmarks.landmark[4].y > landmarks.landmark[3].y:
            directions.append('down')
        else:
            directions.append('folded')
        
        finger_tips = [8, 12, 16, 20]
        finger_bases = [6, 10, 14, 18]
        
        for tip, base in zip(finger_tips, finger_bases):
            tip_y = landmarks.landmark[tip].y
            base_y = landmarks.landmark[base].y
            
            if tip_y < base_y - 0.02:
                directions.append('up')
            elif tip_y > base_y + 0.02:
                directions.append('down')
            else:
                directions.append('folded')
        
        return directions

    def get_finger_states(self, landmarks):
        finger_states = []
        finger_states.append(landmarks.landmark[4].x < landmarks.landmark[3].x)
        for tip, base in [(8, 6), (12, 10), (16, 14), (20, 18)]:
            finger_states.append(landmarks.landmark[tip].y < landmarks.landmark[base].y)
        return finger_states

    def reconocer_sena(self, finger_states, landmarks=None):
        directions = None
        if landmarks is not None:
            directions = self.get_finger_directions(landmarks)
        
        if finger_states == [True, False, False, False, False]:
            return "A"
        if (finger_states == [False, True, True, True, True] and 
            directions is not None and 
            all(d == 'up' for d in directions[1:])):
            return "B"
        if finger_states == [False, True, False, False, False]:
            return "D"
        if landmarks is not None and self.dedos_curvados(landmarks):
            return "E"
        if finger_states == [True, True, False, False, False]:
            return "F"
        if finger_states == [False, False, False, False, True]:
            return "I"
        if finger_states == [True, True, True, False, False]:
            return "K"
        if finger_states == [True, True, False, False, False]:
            return "L"
        
        if directions is not None:
            dedos_abajo = sum(1 for i in [1,2,3,4] if directions[i] == 'down')
            if dedos_abajo == 4 and directions[0] in ['folded']:
                return "M"
            # if dedos_abajo == 3:
            #     return "N"
        
        if finger_states == [False, True, False, False, True]:
            return "U"
        if finger_states == [False, True, True, False, False]:
            return "V"
        if finger_states == [False, True, True, True, False]:
            return "W"
        if (finger_states[0] == False and finger_states[2] == False and 
            finger_states[3] == False and finger_states[4] == False and
            landmarks is not None and self.indice_semidoblado(landmarks)):
            return "X"
        if finger_states == [True, False, False, False, True]:
            return "Y"
        
        return "?"
    
    def start_detection(self):
        if not self.is_running:
            try:
                self.cap = cv2.VideoCapture(0)
                if not self.cap.isOpened():
                    messagebox.showerror("Error", "No se pudo acceder a la cámara")
                    return
                
                self.is_running = True
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.NORMAL)
                self.status_var.set("Detectando señas...")
                
                # Iniciar hilo de detección
                self.detection_thread = threading.Thread(target=self.detection_loop)
                self.detection_thread.daemon = True
                self.detection_thread.start()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al iniciar la detección: {str(e)}")
    
    def detection_loop(self):
        frame_count = 0
        fps_start_time = time.time()
        
        with self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        ) as hands:
            while self.is_running:
                frame_start_time = time.time()
                
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                # Procesar frame
                frame = cv2.flip(frame, 1)  # Espejo horizontal
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                
                # Medir tiempo de procesamiento MediaPipe
                mp_start_time = time.time()
                results = hands.process(image)
                mp_end_time = time.time()
                
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                
                # Dibujar landmarks y detectar señas
                detection_start_time = time.time()
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.mp_drawing.draw_landmarks(
                            image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                        
                        finger_states = self.get_finger_states(hand_landmarks)
                        directions = self.get_finger_directions(hand_landmarks)
                        sena = self.reconocer_sena(finger_states, hand_landmarks)
                        
                        # Medir tiempo de detección completo
                        detection_end_time = time.time()
                        detection_time = (detection_end_time - detection_start_time) * 1000  # en ms
                        
                        # Calcular tiempo total de procesamiento
                        total_processing_time = (mp_end_time - mp_start_time) * 1000  # en ms
                        
                        # Actualizar estadísticas de tiempo
                        self.update_timing_stats(detection_time, total_processing_time, sena)
                        
                        # Actualizar GUI en hilo principal
                        self.root.after(0, self.update_info, sena, finger_states, directions)
                        break
                else:
                    self.root.after(0, self.update_info, "?", [], [])
                
                # Calcular FPS
                frame_count += 1
                if frame_count % 10 == 0:  # Actualizar FPS cada 10 frames
                    current_time = time.time()
                    fps = 10 / (current_time - fps_start_time)
                    self.root.after(0, self.update_fps, fps)
                    fps_start_time = current_time
                
                # Convertir frame para tkinter
                image = cv2.resize(image, (640, 480))
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)
                
                # Actualizar video en hilo principal
                self.root.after(0, self.update_video, image)
    
    def update_video(self, image):
        self.video_label.config(image=image)
        self.video_label.image = image
    
    def update_timing_stats(self, detection_time, total_time, sena):
        # Agregar tiempo a la lista (mantener solo los últimos 30 valores)
        self.detection_times.append(total_time)
        if len(self.detection_times) > 30:
            self.detection_times.pop(0)
        
        # Detectar cambio de seña para medir tiempo de respuesta
        if sena != self.current_sign:
            if sena != "?" and self.current_sign == "?":
                # Nueva seña detectada desde "no detectada"
                self.sign_start_time = time.time()
                self.update_last_translated_sign(sena)
            elif sena != "?" and self.current_sign != "?":
                # Cambio de una seña a otra
                if self.sign_start_time is not None:
                    response_time = (time.time() - self.sign_start_time) * 1000
                    self.last_detection_time = response_time
                self.sign_start_time = time.time()
                self.update_last_translated_sign(sena)
            elif sena != "?" and self.current_sign == "?":
                # Primera seña detectada
                self.update_last_translated_sign(sena)
            
            self.current_sign = sena
    
    def update_last_translated_sign(self, sena):
        """Actualiza la información de la última seña traducida"""
        if sena != "?":
            self.last_translated_sign = sena
            # Obtener timestamp actual
            current_time = time.strftime("%H:%M:%S")
            self.last_sign_timestamp = current_time
            
            # Actualizar GUI en el hilo principal
            self.root.after(0, self.update_last_sign_display, sena, current_time)
    
    def update_last_sign_display(self, sena, timestamp):
        """Actualiza la visualización de la última seña en la GUI"""
        self.ultima_sena_var.set(sena)
        self.timestamp_var.set(timestamp)
    
    def add_current_letter(self):
        """Agrega la letra actual a la palabra en formación"""
        if self.current_sign != "?" and self.current_sign != "":
            self.current_word += self.current_sign
            self.current_word_var.set(self.current_word)
            self.last_added_sign = self.current_sign
            self.status_var.set(f"Agregada letra: {self.current_sign}")
    
    def add_space(self):
        """Agrega un espacio a la palabra"""
        self.current_word += " "
        self.current_word_var.set(self.current_word)
        self.status_var.set("Espacio agregado")
    
    def delete_last_letter(self):
        """Borra la última letra de la palabra"""
        if self.current_word:
            self.current_word = self.current_word[:-1]
            self.current_word_var.set(self.current_word)
            self.status_var.set("Última letra borrada")
    
    def clear_word(self):
        """Limpia toda la palabra actual"""
        self.current_word = ""
        self.current_word_var.set(self.current_word)
        self.status_var.set("Palabra limpiada")
    
    def save_word(self):
        """Guarda la palabra actual en el historial"""
        if self.current_word.strip():
            self.word_history.append(self.current_word.strip())
            # Mantener solo las últimas 10 palabras
            if len(self.word_history) > 10:
                self.word_history.pop(0)
            
            # Actualizar visualización del historial
            history_text = " | ".join(self.word_history) if self.word_history else "Ninguna"
            self.word_history_var.set(history_text)
            
            self.status_var.set(f"Palabra guardada: {self.current_word}")
            self.clear_word()
        else:
            self.status_var.set("No hay palabra para guardar")
    
    def check_auto_add_letter(self, sena):
        """Verifica si se debe agregar automáticamente una letra"""
        current_time = time.time()
        
        if sena != "?" and sena == self.current_sign:
            # La misma seña se mantiene
            if self.sign_hold_time == 0:
                self.sign_hold_time = current_time
            
            hold_duration = current_time - self.sign_hold_time
            
            if hold_duration >= self.sign_hold_threshold and self.last_added_sign != sena:
                # Agregar letra automáticamente
                self.current_word += sena
                self.current_word_var.set(self.current_word)
                self.last_added_sign = sena
                self.status_var.set(f"Auto-agregada: {sena}")
                self.sign_hold_time = 0  # Reset timer
            else:
                # Mostrar progreso
                remaining = self.sign_hold_threshold - hold_duration
                if remaining > 0:
                    self.progress_var.set(f"Manteniendo {sena}... {remaining:.1f}s restantes")
                
        else:
            # Seña cambió, resetear timer
            self.sign_hold_time = 0
            self.progress_var.set("Mantén la seña por 1.5 segundos para agregar la letra")
    
    def update_fps(self, fps):
        self.fps_var.set(f"{fps:.1f} FPS")
    
    def update_info(self, sena, finger_states, directions):
        self.sena_var.set(sena)
        
        # Verificar auto-agregado de letras
        if self.is_running:
            self.check_auto_add_letter(sena)
        
        # Actualizar métricas de tiempo
        if self.detection_times:
            ultimo_tiempo = self.detection_times[-1]
            promedio = sum(self.detection_times) / len(self.detection_times)
            
            self.tiempo_deteccion_var.set(f"{ultimo_tiempo:.2f} ms")
            self.tiempo_promedio_var.set(f"{promedio:.2f} ms")
        
        # Cambiar color según la seña
        if sena != "?":
            self.sena_display.config(bg='#27AE60')  # Verde para seña detectada
        else:
            self.sena_display.config(bg='#E67E22')  # Naranja para no detectada
        
        # Actualizar estados y direcciones
        if finger_states:
            estados_texto = f"Pulgar: {'Ext' if finger_states[0] else 'Dob'}\n"
            estados_texto += f"Índice: {'Ext' if finger_states[1] else 'Dob'}\n"
            estados_texto += f"Medio: {'Ext' if finger_states[2] else 'Dob'}\n"
            estados_texto += f"Anular: {'Ext' if finger_states[3] else 'Dob'}\n"
            estados_texto += f"Meñique: {'Ext' if finger_states[4] else 'Dob'}"
            self.estados_var.set(estados_texto)
        
        if directions:
            direcciones_texto = f"Pulgar: {directions[0]}\n"
            direcciones_texto += f"Índice: {directions[1]}\n"
            direcciones_texto += f"Medio: {directions[2]}\n"
            direcciones_texto += f"Anular: {directions[3]}\n"
            direcciones_texto += f"Meñique: {directions[4]}"
            self.direcciones_var.set(direcciones_texto)
    
    def stop_detection(self):
        self.is_running = False
        if self.cap:
            self.cap.release()
        
        # Resetear variables de tiempo
        self.detection_times = []
        self.last_detection_time = 0
        self.current_sign = "?"
        self.sign_start_time = None
        self.last_translated_sign = "Ninguna"
        self.last_sign_timestamp = ""
        
        # Resetear variables de palabras
        self.sign_hold_time = 0
        self.last_added_sign = ""
        
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_var.set("Detección detenida")
        self.video_label.config(image="", text="Presiona 'Iniciar' para comenzar")
        self.sena_var.set("Ninguna")
        self.estados_var.set("No detectados")
        self.direcciones_var.set("No detectadas")
        self.tiempo_deteccion_var.set("0.00 ms")
        self.tiempo_promedio_var.set("0.00 ms")
        self.fps_var.set("0 FPS")
        self.ultima_sena_var.set("Ninguna")
        self.timestamp_var.set("--:--:--")
        self.progress_var.set("Mantén la seña por 1.5 segundos para agregar la letra")
    
    def exit_app(self):
        if self.is_running:
            self.stop_detection()
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DetectorSenasGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.exit_app)
    root.mainloop()