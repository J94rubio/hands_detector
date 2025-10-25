# 🤟 Detector de Señas LSC (Lenguaje de Señas Colombiano)

Un detector de señas en tiempo real usando Python, MediaPipe y OpenCV disponible en múltiples versiones para reconocer las primeras 15 letras del alfabeto dactilológico del Lenguaje de Señas Colombiano.

## 📦 Versiones Disponibles

### 🖥️ **detector_gui.py** - Versión Completa
- Interfaz gráfica moderna con **formador de palabras**
- Auto-agregado de letras por tiempo (1.5 segundos)
- Historial de palabras y controles avanzados
- **Ideal para**: Comunicación completa y formación de frases

### ⚡ **detector_simple.py** - Versión Simple  
- Interfaz gráfica **sin formador de palabras**
- Enfoque en detección pura de señas
- Métricas de rendimiento y análisis detallado
- **Ideal para**: Aprendizaje, demos y pruebas de precisión

### 💻 **detector_manos.py** - Versión Básica
- Versión minimalista que ejecuta en terminal
- Solo video con detección básica
- Mínimo uso de recursos
- **Ideal para**: Pruebas rápidas y desarrollo

## 🌟 Características

### 📹 Detección en Tiempo Real
- Reconocimiento de 15 señas del LSC: **A, B, D, E, F, I, K, L, M, N, U, V, W, X, Y**
- Detección de landmarks de la mano usando MediaPipe
- Análisis de posición y dirección de dedos (arriba, abajo, doblado)
- Reconocimiento de gestos complejos (dedos curvados, semidoblados)

### 🖥️ Interfaz Gráfica Moderna
- **Video en tiempo real** con visualización de landmarks
- **Panel de información** detallado con estados y direcciones de dedos
- **Métricas de rendimiento** (tiempo de respuesta, FPS, promedios)
- **Formador de palabras** para crear frases completas
- **Historial de señas** con timestamps

### 📝 Formación de Palabras
- **Auto-agregado**: Mantén una seña por 1.5 segundos para agregarla automáticamente
- **Controles manuales**: Botones para agregar, borrar, limpiar y guardar
- **Historial de palabras**: Guarda las últimas 10 palabras creadas
- **Indicador de progreso** visual

### 📊 Métricas de Rendimiento
- **Tiempo de detección** de cada frame
- **Promedio** de los últimos 30 frames
- **FPS** en tiempo real
- **Última seña traducida** con timestamp

## 🛠️ Instalación

### Prerequisitos
- Python 3.7 o superior
- Webcam funcional

### Paso 1: Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/detector-senas-lsc.git
cd detector-senas-lsc
```

### Paso 2: Instalar dependencias
```bash
pip install opencv-python mediapipe pillow
```

### Paso 3: Ejecutar la aplicación
```bash
# Versión completa con formador de palabras (recomendada)
python detector_gui.py

# Versión simple solo detección (ligera)
python detector_simple.py

# Versión básica en terminal (minimalista)
python detector_manos.py
```

## 🎮 Cómo Usar

### Versión Completa (detector_gui.py)

#### Iniciar Detección
1. Ejecuta `python detector_gui.py`
2. Presiona el botón **"▶ Iniciar"**
3. Coloca tu mano frente a la cámara
4. Realiza las señas del LSC

#### Formar Palabras

#### Método Automático:
1. Haz una seña y **mantémela por 1.5 segundos**
2. La letra se agregará automáticamente a la palabra
3. Cambia a la siguiente seña y repite
4. Presiona **"💾 Guardar"** para guardar la palabra

#### Método Manual:
1. Haz una seña
2. Presiona **"➕ Agregar Letra"**
3. Usa **"␣ Espacio"** para separar palabras
4. Usa **"⌫ Borrar"** para corregir errores

### Versión Simple (detector_simple.py)

#### Uso Simplificado
1. Ejecuta `python detector_simple.py`
2. Presiona **"▶ Iniciar Detección"**
3. Coloca tu mano frente a la cámara
4. Observa las señas detectadas en tiempo real

**Características de la versión simple:**
- ✅ **Detección pura** sin formación de palabras
- ✅ **Métricas completas** de rendimiento
- ✅ **Análisis detallado** de estados de dedos
- ✅ **Interfaz limpia** y enfocada
- ✅ **Menor uso** de recursos del sistema

### Controles por Versión

#### Versión Completa:
- **▶ Iniciar**: Comenzar la detección
- **⏹ Detener**: Pausar la detección
- **➕ Agregar Letra**: Agregar seña actual manualmente
- **␣ Espacio**: Agregar espacio entre palabras
- **⌫ Borrar**: Eliminar última letra
- **🗑️ Limpiar**: Borrar palabra completa
- **💾 Guardar**: Guardar palabra en historial
- **❌ Salir**: Cerrar aplicación

#### Versión Simple:
- **▶ Iniciar Detección**: Comenzar la detección
- **⏹ Detener Detección**: Pausar la detección
- **❌ Salir**: Cerrar aplicación

## 📋 Señas Reconocidas

El sistema reconoce las siguientes señas del LSC:

| Letra | Descripción |
|-------|-------------|
| **A** | Puño cerrado con pulgar extendido hacia el costado |
| **B** | Palma abierta, todos los dedos hacia arriba |
| **D** | Solo índice extendido hacia arriba |
| **E** | Puño cerrado, todos los dedos curvados |
| **F** | Pulgar, índice y medio extendidos |
| **I** | Solo meñique extendido |
| **K** | Índice, medio y pulgar extendidos |
| **L** | Pulgar e índice extendidos formando "L" |
| **M** | Cuatro dedos hacia abajo, pulgar doblado |
| **N** | Tres dedos hacia abajo |
| **U** | Índice y meñique extendidos |
| **V** | Índice y medio extendidos (victoria) |
| **W** | Índice, medio y anular extendidos |
| **X** | Índice semidoblado, otros dedos doblados |
| **Y** | Pulgar y meñique extendidos |

## 🏗️ Arquitectura del Proyecto

```
detector-senas-lsc/
├── detector_gui.py          # Interfaz gráfica completa con formador de palabras
├── detector_simple.py       # Interfaz gráfica simple (solo detección)
├── detector_manos.py        # Versión básica en terminal
├── README.md               # Este archivo
└── requirements.txt        # Dependencias del proyecto
```

### Componentes Principales

#### 1. **DetectorSenasGUI** (detector_gui.py)
- Interfaz gráfica completa con tkinter
- Manejo de video en tiempo real
- Panel de información y métricas
- **Sistema completo de formación de palabras**
- Auto-agregado de letras por tiempo
- Historial de palabras guardadas

#### 2. **DetectorSenasSimple** (detector_simple.py)
- Interfaz gráfica **sin formador de palabras**
- Enfoque en detección pura y métricas
- Menor uso de recursos del sistema
- Ideal para aprendizaje y demos

#### 3. **Funciones de Detección** (compartidas)
- `get_finger_states()`: Detecta si los dedos están extendidos o doblados
- `get_finger_directions()`: Determina dirección de dedos (up/down/folded)
- `reconocer_sena()`: Lógica principal de reconocimiento
- `dedos_curvados()`: Detecta dedos curvados para señas especiales
- `indice_semidoblado()`: Detecta posición intermedia del índice

## 📊 Métricas de Rendimiento

El sistema muestra métricas en tiempo real:

- **Última detección**: Tiempo de procesamiento del último frame
- **Promedio**: Tiempo promedio de los últimos 30 frames  
- **FPS**: Frames por segundo actual
- **Última seña**: Última seña reconocida con timestamp

### Interpretación de Tiempos
- **< 50ms**: ✅ Excelente
- **50-100ms**: ✅ Bueno  
- **100-200ms**: ⚠️ Aceptable
- **> 200ms**: ❌ Requiere optimización

## 🔧 Configuración Avanzada

### Ajustar Sensibilidad
En `detector_gui.py`, puedes modificar:

```python
# Tiempo para auto-agregar letras (segundos)
self.sign_hold_threshold = 1.5

# Confianza mínima de detección
min_detection_confidence = 0.7
min_tracking_confidence = 0.5

# Umbral para dedos curvados
umbral = 0.07
```

### MediaPipe Settings
```python
mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,              # Máximo 2 manos
    min_detection_confidence=0.7,  # Confianza mínima
    min_tracking_confidence=0.5    # Seguimiento mínimo
)
```

## 🐛 Solución de Problemas

### Problemas Comunes

#### La cámara no se abre
```bash
# Verifica que no esté siendo usada por otra aplicación
# Reinicia la aplicación
python detector_gui.py
```

#### Detección imprecisa
- Asegúrate de tener buena iluminación
- Mantén la mano a 60-80cm de la cámara
- Usa fondo neutro (evita patrones)
- Verifica que la seña esté bien formada

#### Rendimiento lento
- Cierra otras aplicaciones que usen la cámara
- Reduce la resolución del video
- Verifica que tu sistema cumpla los requisitos

### Logs y Debug
La aplicación muestra información de debug en:
- **Barra de estado**: Estado actual del sistema
- **Panel de métricas**: Tiempos de procesamiento
- **Estados de dedos**: Información detallada de detección

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Ideas para Contribuir
- Agregar más letras del alfabeto LSC
- Implementar reconocimiento de números
- Mejorar la precisión de detección
- Agregar sonidos o síntesis de voz
- Exportar palabras a archivos de texto
- Modo de entrenamiento/práctica
- Soporte para diferentes idiomas de señas

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👏 Agradecimientos

- **MediaPipe** por la tecnología de detección de hands landmarks
- **OpenCV** por el procesamiento de video
- **Comunidad LSC** por la documentación del lenguaje de señas
- **Pillow** para el manejo de imágenes en la GUI

## 📞 Contacto

- **Autor**: Tu Nombre
- **Email**: tu.email@ejemplo.com  
- **Proyecto**: [https://github.com/tu-usuario/detector-senas-lsc](https://github.com/tu-usuario/detector-senas-lsc)

---

### 🚀 ¡Empieza a comunicarte en LSC hoy mismo!

Este detector te permitirá practicar y aprender el alfabeto dactilológico del Lenguaje de Señas Colombiano de manera interactiva y divertida.