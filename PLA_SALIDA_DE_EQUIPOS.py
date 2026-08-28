import os
import sys
import ssl
import base64
import inspect
import tempfile
import certifi
from datetime import datetime
from fpdf import FPDF
import flet as ft

try:
    from batercon_logo import LOGO_BASE64
except ImportError:
    LOGO_BASE64 = None

os.environ['SSL_CERT_FILE'] = certifi.where()
ssl._create_default_https_context = ssl._create_unverified_context

meses_es = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
ahora = datetime.now()
fecha_formateada = f"La Paz, {ahora.day} de {meses_es[ahora.month - 1]} de {ahora.year}"

def make_border(color="#2D3748", width=1):
    bs = ft.BorderSide(width, color)
    return ft.Border(top=bs, bottom=bs, left=bs, right=bs)

INYECTORA_OPTIONS = [
    {"item": "INYECTORA - FREYSSINET", "serie": ""},
    {"item": "INYECTORA - ELECTRICA ARNO (PISTON DOBLE)", "serie": "BIE-01"},
    {"item": "INYECTORA - C/BLADE PISTON (PISTON SIMPLE)", "serie": "BIE-02"},
    {"item": "INYECTORA - MANUAL (PISTON SIMPLE)", "serie": "BIM-03"},
    {"item": "INYECTORA - NEUMÁTICA DE DOBLE EFECTO", "serie": "INY-NEU-01"}
]

BATIDORAS = [
    {"item": "BATIDORA FREYSSINET N° 1", "serie": "BAT-FR-01"},
    {"item": "BATIDORA FREYSSINET N° 2", "serie": "BAT-FR-02"},
    {"item": "BATIDORA TURBO-MIXER ELECTRICO", "serie": "BAT-EL-01"},
    {"item": "BATIDORA MANUAL DE TAMBOR", "serie": "BAT-MAN-01"}
]

GENERADORES = [
    {"item": "GENERADOR - KHOLER 2013", "serie": "GGE-01"},
    {"item": "GENERADOR - BRIGGS & STRATTON 2017", "serie": "GGE-03"},
    {"item": "GENERADOR - BRIGGS & STRATTON 2014", "serie": "GGE-02"}
]

GATOS_FREYSSINET = [
    {"item": "GATO - FREYSSINET S6 (FRANCIA)", "serie": "GH-01"},
    {"item": "GATO - FREYSSINET S6 (USA)", "serie": "GH-02"},
    {"item": "GATO - FREYSSINET S6 (MEXICO)", "serie": "GH-03"},
    {"item": "GATO - FREYSSINET C (MEXICO)", "serie": "GH-04"},
]

GATOS_OVM_HM = [
    {"item": "GATO - OVM YWG250 1", "serie": "GH-05"},
    {"item": "GATO - OVM YWG250 2", "serie": "GH-06"},
    {"item": "GATO - HM YWG250 1", "serie": "GH-07"},
    {"item": "GATO - HM YWG250 2", "serie": "GH-08"},
    {"item": "GATO - OVM MONOTORON 1 0.5", "serie": "GH-09"},
    {"item": "GATO - OVM MONOTORON 1 0.6", "serie": "GH-10"},
    {"item": "GATO - HM MONOTORON 1 0.5", "serie": "GH-11"},
    {"item": "GATO - HM MONOTORON 1 0.6", "serie": "GH-12"}
]

BOMBAS = [
    {"item": "BOMBA - ELECTRICA OVM1 (1.2K RPM)", "serie": "BE-01"},
    {"item": "BOMBA - ELECTRICA OVM2 (1.2K RPM)", "serie": "BE-02"},
    {"item": "BOMBA - ELECTRICA OVM3 (1.2K RPM)", "serie": "BE-03"},
    {"item": "BOMBA - ELECTRICA HM1 (1.3K RPM)", "serie": "BE-04"},
    {"item": "BOMBA - ELECTRICA HM2 (1.3K RPM)", "serie": "BE-05"},
    {"item": "BOMBA - ELECTRICA HM3 (1.3K RPM)", "serie": "BE-07"},
    {"item": "BOMBA - MANUAL FREYSSINET1", "serie": "BM-01"},
    {"item": "BOMBA - MANUAL FREYSSINET2", "serie": "BM-02"},
    {"item": "BOMBA - MANUAL HM1", "serie": "BM-03"},
    {"item": "BOMBA - MANUAL HM2", "serie": "BM-04"}
]

CABLES = [
    {"item": "CABLES EQUIP1", "serie": "EQ1-CAB-EXT5M", "cant": "13"},
    {"item": "CABLES EQUIP2", "serie": "EQ2-CAB-EXT5M", "cant": "13"},
    {"item": "CABLES EQUIP3", "serie": "EQ3-CAB-EXT5M", "cant": "13"},
    {"item": "CABLES EQUIP1Y2", "serie": "EQ1-CAB-EXT5M EQ2-CAB-EXT5M", "cant": ""},
    {"item": "CABLES EQUIP1Y3", "serie": "EQ1-CAB-EXT5M EQ3-CAB-EXT5M", "cant": ""},
    {"item": "CABLES EQUIP2Y3", "serie": "EQ2-CAB-EXT5M EQ3-CAB-EXT5M", "cant": ""}
]

def _gen_opts(prefix, code=""):
    s = f"-{code}" if code else ""
    return [
        {"item": f"{prefix} 1", "serie": f"EQ1{s}", "cant": "1"},
        {"item": f"{prefix} 2", "serie": f"EQ2{s}", "cant": "1"},
        {"item": f"{prefix} 3", "serie": f"EQ3{s}", "cant": "1"},
        {"item": f"{prefix} 1Y2", "serie": f"EQ1{s} EQ2{s}".strip(), "cant": "1"},
        {"item": f"{prefix} 1Y3", "serie": f"EQ1{s} EQ3{s}".strip(), "cant": "1"},
        {"item": f"{prefix} 2Y3", "serie": f"EQ2{s} EQ3{s}".strip(), "cant": "1"},
    ]

EQUIPO_DE_PRUEBA_DE_CARGA = _gen_opts("EQUIP PRUEBA DE CARGA", "CEN-REG")
CABLE_DE_PRUEBA_DE_CARGA = _gen_opts("CABLE P", "CAB-ALIS-5M")
ALARGADOR = _gen_opts("ALARGADOR")
CORTA_PICO = _gen_opts("CORTA PICO")
CAJAS_PLASTICAS = _gen_opts("CAJA PLASTICA")

SENSORES = [
    {"item": f"SENSORES DE {tipo}", "serie": "EQ-RA-DES", "cant": "1"}
    for tipo in ["ROSCA", "RESORTE", "LASER", "ROSCA Y RESORTE", "ROSCA Y LASER", "RESORTE Y LASER"]
]

RAW_INVENTARIO = {
    "IMPLEMENTOS DE SEGURIDAD": [
        ("CASCOS BLANCOS", "", ""),
        ("CASCOS AMARILLOS", "", ""),
        ("ARNEZ", "", "1"),
        ("CHALECOS REFLECTIVOS", "", ""),
        ("CUERDAS", "", ""),
        ("MOSQUETON", "", ""),
    ],
    "SIST. FREYSSINET": [
        ("BOMBA", "", "1"),
        ("GATO", "", "1"),
        ("CAMPANA", "", "1"),
        ("GENERADOR", "", "1"),
        ("CHUKS", "", "12"),
        ("MANOMETRO ", "", "2"),
        ("MANGUERAS (TESADO)", "", "2"),
        ("TECLE", "", "1"),
        ("TRIPODE", "", "1"),
        ("MALETIN DE HERRAMIENTAS", "", ""),
        ("REQUINTADOR", "", "")
    ],
    "SIST. OVM / HM": [
        ("BOMBA", "", "1"),
        ("GATO", "", "1"),
        ("GENERADOR", "", "1"),
        ("TUBOS", "", "12"),
        ("CUÑAS", "", "12"),
        ("MANOMETRO ", "", "2"),
        ("MANGUERAS (TESADO)", "", "2"),
        ("TECLE", "", "1"),
        ("TRIPODE", "", "1"),
        ("MALETIN DE HERRAMIENTAS", "", ""),
        ("CORONA", "", ""),
        ("PLACA", "", ""),
        ("REQUINTADOR", "", ""),
        ("ACOPLE", "", "")
    ],
    "CONTRA FLECHA": [
        ("CABLES DE 5 METROS", "", "1"),
        ("EQUIPO DE PRUEBA DE CARGA", "", "4"),
        ("SENSORES", "", "4"),
        ("CABLE DE EQUIPO", "", "4"),
        ("ALARGADOR", "", "4"),
        ("CORTA PICO", "", "4"),
        ("CAJA PLASTICA", "", "4"),
        ("MESA", "", "4"),
        ("CHANCHITO/ PROTECTOR DE CABLES", "", "4"),
        ("COMPUTADORA", "", "4"),
        ("CARGADOR DE COMPUTADORA", "", "4"),
        ("IMPRESORA", "", "4"),
        ("MAUS", "", "4"),
        ("HOJAS", "", "4"),
        ("TABLERO", "", "4")
    ],
    "INYECCION": [
        ("INYECTORA FREYSSINET", "", "1"),
        ("BATIDORA DE ALTA TURBULENCIA", "", "1"),
        ("GENERADOR", "", "1"),
        ("MANGUERA DE INYECCION", "ACC-19", "1"),
        ("MANOMETRO ", "ACC-20", "1"),
        ("MALETIN DE HERRAMIENTAS", "ACC-21", "1"),
        ("BOMBA DE AGUA", "ACC-22", "1"),
        ("ADITIVO FLUIDIFICANTE", "", ""),
        ("ADITIVO EXPANSOR", "", ""),
        ("BALDE DE MEDICION", "EQ/LAB/BAL-8LT/1", "1"),
        ("FRASCO", "EQ/LAB/BAL-8LT/1", "1"),
        ("JARRA", "EQ/LAB/BAL-8LT/1", "1"),
    ],
    "REFLEXION DE ONDA (PIT)": [
        ("EQUIPO PARA PRUEBA DE INTEGRIDAD DE PILOTES DE BAJA DEFORMACION", "C-61", "1"),
        ("MARTILLO", "CR-TANG R-40", "1"),
        ("CABLE DE SENSOR", "TB SN:XD177", "1"),
        ("CABLE CONECTOR", "", "1"),
        ("CARGADOR", "JMS0905", "1"),
        ("CABLE DOBLE USB", "", "1"),
        ("CAJA PLOMA CON FUNDA", "", "1"),
        ("GENERADOR", "", "1"),
        ("CINCEL / COMBO", "", "1"),
        ("LIJA", "", "1"),
        ("GEL / VASELINA", "", "1"),
        ("FLASH / FLEXO 3M / CHANCHITO / ABRAZADERAS DE NYLON", "", "1"),
        ("MESA / ALARGADOR / MANUALES", "", "1"),
        ("TABLERO / BOLIGRAFOS / PLANILLAS / MARCADORES / PIZARRA", "", "1")
    ],
    "ULTRASONIDO": [
        ("COMPUTADORA ULTRASONIDO", "C-62", "1"),
        ("CABLES DE SENSORES", "", "2"),
        ("CABLE CONECTOR", "", "1"),
        ("SENSORES", "", "2"),
        ("CARGADOR", "", "1"),
        ("MALETA PLOMA CON FUNDA", "", "1"),
        ("GENERADOR", "", "1"),
        ("GEL / VASELINA", "", "1"),
        ("FLASH / FLEXO 3M / CHANCHITO / ABRAZADERAS DE NYLON", "", "1"),
        ("MESA / ALARGADOR / MANUALES", "", "1"),
        ("TABLERO / BOLIGRAFOS / PLANILLAS / MARCADORES / PIZARRA", "", "1")
    ],
    "CROSS - HOLE": [
        ("RSM - SY6c", "EQ-CSL-01-IBT", "1"),
        ("CARGADOR DE SENSOR", "EQ-CSL-CAR-01", "1"),
        ("CABLE DE CARGADOR", "EQ-CSL-CABL-01", "1"),
        ("RODILLO DE TRANSMISOR", "EQ-CSL-ROD-01", "1"),
        ("POLEA NEGRA", "EQ-CSL-PO-01", "1"),
        ("POLEA ROJA", "EQ-CSL-PO-02", "1"),
        ("POLEA VERDE", "EQ-CSL-PO-03", "1"),
        ("POLEA AMARILLA", "EQ-CSL-PO-04", "1"),
        ("CABLE EXTENSOR", "EQ-CSL-CAB-EX-01", "1"),
        ("CABLE EXTENSOR REPUESTO", "EQ-CSL-CAB-EX- REP-02", "1"),
        ("CARGADOR Y CABLE DE REPUESTO", "EQ-CSL-BAT-REP-02", "1"),
        ("CARRETE COLOR VERDE", "EQ-CSL-CARR-01", "1"),
        ("CARRETE COLOR AZUL", "EQ-CSL-CARR-02", "1"),
        ("CARRETE COLOR NARANJA", "EQ-CSL-CARR-03", "1"),
        ("CARRETE COLOR AMARILLO", "EQ-CSL-CARR-04", "1"),
        ("TRIPODE", "EQ-CSL-TRP-01", "1"),
        ("FLEXO/ VERNIER/ USB/ SD/ ALARGADOR/ CHANCHITO", "EQ-CSL-HER-01", "1"),
        ("PIZARRA", "EQ-CSL-PZ-01", "1"),
        ("BOMBA DE AGUA SUMERGIBLE", "BAS-2 LAB", "1"),
        ("MESA", "", "1"),
        ("SOMBRILLA", "", "1"),
        ("GENERADOR", "", "1"),
        ("HERRAMIENTAS Y ACCESORIOS CROSS-HOLE", "EQ-CSL-HER-02", "1")
    ],
    "EXTRACCION DE NUCLEOS": [
        ("HUSQVARNA DMS 240", "", "1"),
        ("MANGUERA DE ALIMENTACION DE AGUA", "", "1"),
        ("BOMBA AL VACIO - VACUM", "", "1"),
        ("ESTRUCTURA DE SOPORTE VERTICAL IBT", "", "1"),
        ("MANGUERA DE BOMBA AL VACIO", "", "1"),
        ("BOMBA DE AGUA 0.5 HP", "", "1"),
        ("MANGUERA DE AGUA AZUL", "", "1"),
        ("BOMBA DE AGUA 1HP", "", "1"),
        ("MANGUERA DE AGUA VERDE", "", "1"),
        ("BROCA 3 PULG", "", "1"),
        ("BROCA 4 PULG", "", "1"),
        ("BROCA 2 PULG", "", "1"),
        ("FILM PARA MUESTRAS/ MARCADORES/ TRAPOS", "", "1"),
        ("PLASTICOS/ NIVEL/ ABRAZADERAS", "", "1"),
        ("ALARGADOR/ CHANCHITO", "", "1")
    ],
    "LABORATORIO MOVIL": [
        ("BALANZA", "EQ/LAB/BAL/01", "1"),
        ("JARRA", "EQ/LAB/JAR/1", "1"),
        ("VASO PLASTICO", "EQ/LAB/VAS-PLA/1", "1"),
        ("JARRA 1L", "EQ/LAB/JA/PLA/01", "1"),
        ("TARA METALICA D=30 cm", "EQ/LAB/TAR-30C/1", "1"),
        ("TARA METALICA D=10 cm", "EQ/LAB/TAR-10C/1-2", "2"),
        ("PURUÑA GRANDE", "EQ/LAB/PUR#12/4", "1"),
        ("PURUÑA PEQUEÑA", "EQ/LAB/PUR#8/1", "1"),
        ("TERMOMETRO", "EQ/LAB/TER/01", "1"),
        ("TERMOMETRO DIGITAL", "EQ/LAB/TER-DIG/1", "1"),
        ("PIPETA", "EQ/LAB/PSI/01", "1"),
        ("COLADERA METALICA", "EQ/LAB/COL-MET/1", "1"),
        ("MOTOR DE BATIDORA", "EQ/LAB/MEZ/01", "1"),
        ("LLAVES", "EQ/LAB/BAT-LLA/03,4", "1"),
        ("MALETIN DE HERRAMIENTAS", "EQ/LAB/MAL/01", "1"),
        ("CONO DE FLUIDEZ", "EQ/LAB/FLU-CON/1", "1"),
        ("JARRA METALICA", "EQ/MAR/JAR/2", "1"),
        ("BRIQUETAS", "EQ/LAB/MUE-BRI", "4"),
        ("PH METRO", "EQ/LAB/PH/01", "1"),
        ("CRONOMETRO", "EQ/LAB/CRO/01", "1"),
        ("TRAPOS/ ACEITE SUCIO/ MARCADOR/ BOLSAS/ PLANILLAS/ JERINGA", "", "1"),
        ("ADITIVO EXPANSOR", "", "1"),
        ("ADITIVO FLUIDIFICANTE", "", "1"),
    ],
    "MUESTREO DE PROBETAS DE HORMIGON": [
        ("PURUÑA DE CONCRETO", "EQ/LAB/PUR-CO/1", "1"),
        ("PATO", "EQ/LAB/PA/1", "1"),
        ("MARTILLO DE GOMA", "EQ/LAB/MAR-GOM/1", "1"),
    ] + [
        ("PROBETA CILINDRICA", f"EQ/LAB/PRO-CI/{i}", "1") for i in range(1, 13)
    ] + [
        ("APISONADOR", "EQ/LAB/API/1", "4"),
        ("CRONOMETRO", "EQ/LAB/CRO/01", "1"),
        ("TRAPOS/ ACEITE SUCIO/ MARCADOR/ BOLSAS/ PLANILLAS", "", "1"),
        ("CONO DE ABRAMS", "EQ/LAB/ABRA/1", "1"),
        ("SOPORTE DE CONO DE ABRAMS", "EQ/LAB/SOP-ABRA/2-3", "1"),
    ],
}

DEFAULT_INVENTARIO = {
    cat: [{"item": itm[0], "serie": itm[1], "cant": itm[2]} for itm in items]
    for cat, items in RAW_INVENTARIO.items()
}

def get_dropdown_options(category, item_name):
    cat_u = str(category).strip().upper()
    name_u = str(item_name).upper()
    
    if "GENERADOR" in name_u or item_name in [opt["item"] for opt in GENERADORES]:
        return GENERADORES
        
    if cat_u in ["INYECCION", "INYECTADO"]:
        if "INYECTORA" in name_u or item_name in [opt["item"] for opt in INYECTORA_OPTIONS]:
            return INYECTORA_OPTIONS
        if "BATIDORA" in name_u or item_name in [opt["item"] for opt in BATIDORAS]:
            return BATIDORAS
            
    if cat_u in ["SIST. FREYSSINET", "SIST. OVM / HM", "TESADO"]:
        if "BOMBA" in name_u or item_name in [opt["item"] for opt in BOMBAS]:
            if "FREYSSINET" in cat_u:
                return [b for b in BOMBAS if "FREYSSINET" in b["item"]]
            elif "OVM" in cat_u or "HM" in cat_u:
                return [b for b in BOMBAS if "OVM" in b["item"] or "HM" in b["item"]]
            return BOMBAS
            
        if "GATO" in name_u or item_name in [opt["item"] for opt in GATOS_FREYSSINET] or item_name in [opt["item"] for opt in GATOS_OVM_HM]:
            if "FREYSSINET" in cat_u:
                return GATOS_FREYSSINET
            if "OVM" in cat_u or "HM" in cat_u:
                return GATOS_OVM_HM
            return GATOS_FREYSSINET + GATOS_OVM_HM
            
    if cat_u in ["CONTRA FLECHA", "CONTRAFLECHA"]:
        if "CABLE DE EQUIPO" in name_u or "CABLE DE PRUEBA DE CARGA" in name_u or item_name in [opt["item"] for opt in CABLE_DE_PRUEBA_DE_CARGA]:
            return CABLE_DE_PRUEBA_DE_CARGA
        if "CABLES" in name_u or item_name in [opt["item"] for opt in CABLES]:
            return CABLES
        if "EQUIPO DE PRUEBA DE CARGA" in name_u or "EQUIP PRUEBA DE CARGA" in name_u or item_name in [opt["item"] for opt in EQUIPO_DE_PRUEBA_DE_CARGA]:
            return EQUIPO_DE_PRUEBA_DE_CARGA
        if "SENSORES" in name_u or item_name in [opt["item"] for opt in SENSORES]:
            return SENSORES
        if "ALARGADOR" in name_u or item_name in [opt["item"] for opt in ALARGADOR]:
            return ALARGADOR
        if "CORTA PICO" in name_u or item_name in [opt["item"] for opt in CORTA_PICO]:
            return CORTA_PICO
        if "CAJA PLASTICA" in name_u or "CAJAS PLASTICAS" in name_u or item_name in [opt["item"] for opt in CAJAS_PLASTICAS]:
            return CAJAS_PLASTICAS
            
    return None

def clean_text(text):
    if not text:
        return ""
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N', 'ü': 'u', 'Ü': 'U', '°': 'o.'
    }
    for orig, rep in replacements.items():
        text = text.replace(orig, rep)
    return text

def split_text_to_fit(pdf, text, width, font_size=8):
    if not text:
        return [""]
    pdf.set_font("Arial", size=font_size)
    words = str(text).split(" ")
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + " " + word if current_line else word
        if pdf.get_string_width(test_line) < (width - 4):
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines if lines else [""]

class BaterconPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="Letter")
        
    def footer(self):
        self.set_y(-11)
        self.set_font("Arial", size=7.5)
        self.set_text_color(113, 128, 150)
        self.cell(0, 5, f"Pagina {self.page_no()} de {{nb}}", 0, 0, "C")

def draw_table_row(pdf, col_texts, col_widths, col_aligns, line_height=5, fill=False):
    col_lines = []
    max_lines = 1
    for i, (text, width) in enumerate(zip(col_texts, col_widths)):
        font_size = 7.5 if i in [3, 7] else 8
        lines = split_text_to_fit(pdf, text, width, font_size=font_size)
        col_lines.append((lines, font_size))
        if len(lines) > max_lines:
            max_lines = len(lines)
            
    row_height = max_lines * line_height
    start_x = pdf.get_x()
    start_y = pdf.get_y()
    
    for i, ((lines, f_size), width, align) in enumerate(zip(col_lines, col_widths, col_aligns)):
        pdf.set_xy(start_x, start_y)
        style = "FD" if fill else "D"
        if fill:
            pdf.set_fill_color(245, 245, 245)
        pdf.rect(start_x, start_y, width, row_height, style)
        
        pad_lines = (max_lines - len(lines)) / 2.0
        text_y = start_y + (pad_lines * line_height)
        
        pdf.set_font("Arial", size=f_size)
        for line_idx, line in enumerate(lines):
            pdf.set_xy(start_x + 1, text_y + (line_idx * line_height))
            pdf.cell(width - 2, line_height, line, border=0, align=align)
            
        start_x += width
        
    pdf.set_xy(10, start_y + row_height)

def draw_metadata_row(pdf, label1, value1, label2, value2, line_height=4.8):
    w_label = 36
    w_val = 62
    val1_lines = split_text_to_fit(pdf, value1, w_val, font_size=8.5)
    val2_lines = split_text_to_fit(pdf, value2, w_val, font_size=8.5) if label2 else [""]
    max_lines = max(len(val1_lines), len(val2_lines))
    row_height = max_lines * line_height
    
    start_x = pdf.get_x()
    start_y = pdf.get_y()
    
    pdf.set_fill_color(240, 240, 240)
    pdf.rect(start_x, start_y, w_label, row_height, "FD")
    pdf.set_xy(start_x + 2, start_y + (row_height - line_height)/2.0)
    pdf.set_font("Arial", style="B", size=8.5)
    pdf.cell(w_label - 4, line_height, label1, border=0, align="L")
    
    pdf.rect(start_x + w_label, start_y, w_val, row_height, "D")
    pdf.set_font("Arial", size=8.5)
    for idx, line in enumerate(val1_lines):
        pdf.set_xy(start_x + w_label + 2, start_y + (idx * line_height))
        pdf.cell(w_val - 4, line_height, line, border=0, align="L")
        
    if label2:
        pdf.set_fill_color(240, 240, 240)
        pdf.rect(start_x + w_label + w_val, start_y, w_label, row_height, "FD")
        pdf.set_xy(start_x + w_label + w_val + 2, start_y + (row_height - line_height)/2.0)
        pdf.set_font("Arial", style="B", size=8.5)
        pdf.cell(w_label - 4, line_height, label2, border=0, align="L")
        
        pdf.rect(start_x + w_label + w_val + w_label, start_y, w_val, row_height, "D")
        pdf.set_font("Arial", size=8.5)
        for idx, line in enumerate(val2_lines):
            pdf.set_xy(start_x + w_label + w_val + w_label + 2, start_y + (idx * line_height))
            pdf.cell(w_val - 4, line_height, line, border=0, align="L")
            
    pdf.set_xy(10, start_y + row_height)

def draw_full_metadata_row(pdf, label, value, line_height=4.8):
    w_label = 36
    w_val = 160
    val_str = str(value) if value is not None else ""
    effective_width = w_val - 4
    val_lines = []
    
    for paragraph in val_str.split('\n'):
        current_line = ""
        for word in paragraph.split(' '):
            test_line = f"{current_line} {word}".strip() if current_line else word
            if pdf.get_string_width(test_line) <= effective_width:
                current_line = test_line
            else:
                if current_line:
                    val_lines.append(current_line)
                while pdf.get_string_width(word) > effective_width:
                    split_idx = 1
                    while pdf.get_string_width(word[:split_idx]) <= effective_width:
                        split_idx += 1
                    val_lines.append(word[:split_idx-1])
                    word = word[split_idx-1:]
                current_line = word
        if current_line or not paragraph:
            val_lines.append(current_line)
            
    if not val_lines:
        val_lines = [""]

    row_height = max(1, len(val_lines)) * line_height
    start_x = pdf.get_x()
    start_y = pdf.get_y()
    
    pdf.set_fill_color(240, 240, 240)
    pdf.rect(start_x, start_y, w_label, row_height, "FD")
    pdf.set_xy(start_x + 2, start_y + (row_height - line_height)/2.0)
    pdf.set_font("Arial", style="B", size=8.5)
    pdf.cell(w_label - 4, line_height, label, border=0, align="L")
    
    pdf.rect(start_x + w_label, start_y, w_val, row_height, "D")
    pdf.set_font("Arial", size=8.5)
    for idx, line in enumerate(val_lines):
        pdf.set_xy(start_x + w_label + 2, start_y + (idx * line_height))
        pdf.cell(w_val - 4, line_height, line, border=0, align="L")
        
    pdf.set_xy(10, start_y + row_height)

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        meipass_path = os.path.join(sys._MEIPASS, relative_path)
        if os.path.exists(meipass_path):
            return meipass_path
    candidates = [
        relative_path,
        os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path),
        os.path.join(os.getcwd(), relative_path),
        os.path.join(os.path.dirname(sys.executable), relative_path)
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return relative_path

def generate_pdf(form_data, selected_items, output_path):
    pdf = BaterconPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=False)  # Manejo manual y exacto de saltos de página
    pdf.set_font("Arial", size=12)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_draw_color(45, 55, 72)
    
    logo_path = None
    temp_logo_created = False
    possible_logos = ["logo_consultora.jpg", "public/logo_consultora.jpg", "assets/images/logo_consultora_1784128845907.jpg"]
    for p in possible_logos:
        resolved = get_resource_path(p)
        if os.path.exists(resolved):
            logo_path = resolved
            break

    if not logo_path and LOGO_BASE64:
        try:
            temp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
            temp_file.write(base64.b64decode(LOGO_BASE64))
            temp_file.close()
            logo_path = temp_file.name
            temp_logo_created = True
        except Exception:
            pass

    # ENCABEZADO PRINCIPAL (PÁGINA 1) - Ancho total: 196mm en hoja Carta (215.9mm)
    pdf.rect(10, 10, 45, 24, "D")
    if logo_path and os.path.exists(logo_path):
        pdf.image(logo_path, x=19.5, y=10.5, w=26)
        pdf.set_font("Arial", style="B", size=9.5)
        pdf.set_text_color(15, 17, 21)
        pdf.set_xy(10, 28)
        pdf.cell(45, 5, "BATERCON", border=0, align="C")
    else:
        pdf.set_font("Arial", style="B", size=13)
        pdf.set_text_color(15, 17, 21)
        pdf.set_xy(10, 10)
        pdf.cell(45, 24, "BATERCON", border=0, align="C")

    if temp_logo_created and logo_path and os.path.exists(logo_path):
        try:
            os.remove(logo_path)
        except Exception:
            pass

    pdf.rect(55, 10, 85, 24, "D")
    pdf.set_font("Arial", style="B", size=11)
    pdf.set_text_color(45, 55, 72)
    pdf.set_xy(55, 16) 
    pdf.multi_cell(85, 6, "FORMULARIO DE CONTROL\nDE EQUIPOS", border=0, align="C")

    pdf.rect(140, 10, 66, 24, "D")
    pdf.set_font("Arial", style="B", size=9.5)
    pdf.set_text_color(229, 62, 62) 
    pdf.set_xy(140, 13.5)
    pdf.cell(66, 5, "PLANILLA N°:", border=0, align="C")
    pdf.set_font("Arial", style="B", size=11.5)
    pdf.set_text_color(15, 17, 21)
    pdf.set_xy(140, 19.5)
    pdf.cell(66, 5, clean_text(form_data['num_planilla']), border=0, align="C")

    # DATOS GENERALES
    pdf.set_xy(10, 37.5)
    pdf.set_font("Arial", style="B", size=8.5)
    pdf.set_text_color(74, 85, 104)
    pdf.cell(196, 5, "DATOS GENERALES DE COMISION", ln=True)
    pdf.set_text_color(15, 17, 21)
    
    meta_line_height = 4.6
    draw_metadata_row(pdf, "Lugar y Fecha:", form_data['lugar_fecha'], "Responsable:", form_data['responsable'], line_height=meta_line_height)
    draw_metadata_row(pdf, "Vehiculo/Placa:", form_data['vehiculo'], "Proyecto:", form_data['proyecto'], line_height=meta_line_height)
    draw_metadata_row(pdf, "Orden de Viaje:", form_data['orden_viaje'], "Empresa:", form_data['empresa'] if form_data['empresa'] else "", line_height=meta_line_height)
    draw_full_metadata_row(pdf, "Destino:", form_data['destino'], line_height=meta_line_height)
    
    if form_data.get("personal"):
        draw_full_metadata_row(pdf, "Personal Asig.:", ", ".join(form_data["personal"]), line_height=meta_line_height)
    
    pdf.ln(2.5)
    pdf.set_font("Arial", style="B", size=8.5)
    pdf.set_text_color(74, 85, 104)
    pdf.cell(196, 5, "DETALLE DE EQUIPOS E INVENTARIO", ln=True)
    pdf.set_text_color(15, 17, 21)
    
    col_widths = [10, 36, 67, 27, 12, 15, 15, 14]
    col_aligns = ["C", "L", "L", "L", "C", "C", "C", "L"]

    def draw_table_header():
        pdf.set_fill_color(229, 62, 62)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", style="B", size=8.0)
        pdf.cell(col_widths[0], 6.5, "N°", border=1, align="C", fill=True)
        pdf.cell(col_widths[1], 6.5, "CATEGORIA", border=1, align="L", fill=True)
        pdf.cell(col_widths[2], 6.5, "DESCRIPCION", border=1, align="L", fill=True)
        pdf.cell(col_widths[3], 6.5, "SERIE", border=1, align="L", fill=True)
        pdf.cell(col_widths[4], 6.5, "CANT", border=1, align="C", fill=True)
        pdf.cell(col_widths[5], 6.5, "SALIDA", border=1, align="C", fill=True)
        pdf.cell(col_widths[6], 6.5, "RETORNO", border=1, align="C", fill=True)
        pdf.cell(col_widths[7], 6.5, "OBS.", border=1, align="C", fill=True, ln=True)
        pdf.set_text_color(15, 17, 21)

    def draw_continuation_header():
        pdf.set_xy(10, 10)
        pdf.set_fill_color(240, 240, 240)
        pdf.set_draw_color(45, 55, 72)
        pdf.rect(10, 10, 130, 9, "FD")
        pdf.set_font("Arial", style="B", size=9)
        pdf.set_text_color(45, 55, 72)
        pdf.set_xy(12, 12)
        pdf.cell(126, 5, "BATERCON - CONTROL DE EQUIPOS (Continuacion)", border=0, align="L")
        
        pdf.rect(140, 10, 66, 9, "D")
        pdf.set_font("Arial", style="B", size=8.5)
        pdf.set_text_color(229, 62, 62)
        pdf.set_xy(140, 11)
        pdf.cell(28, 7, "PLANILLA:", border=0, align="R")
        pdf.set_text_color(15, 17, 21)
        pdf.set_font("Arial", style="B", size=9)
        pdf.set_xy(168, 11)
        pdf.cell(36, 7, clean_text(form_data['num_planilla']), border=0, align="L")
        
        pdf.set_xy(10, 21.5)
        draw_table_header()

    draw_table_header()
    
    num_items = len(selected_items)
    if num_items <= 12:
        row_lh = 5.2
    elif num_items <= 16:
        row_lh = 4.8
    else:
        row_lh = 5.0
        
    for idx, item in enumerate(selected_items, 1):
        fill = (idx % 2 == 0)
        salida_str = "X" if item.get('salida') else ""
        retorno_str = "X" if item.get('retorno') else ""

        if pdf.get_y() + (row_lh * 2) > 260:
            pdf.add_page()
            draw_continuation_header()
            
        draw_table_row(
            pdf,
            [str(idx), item['category'], item['item'], item['serie'], str(item['cant']), salida_str, retorno_str, str(item.get('obs', ''))],
            col_widths,
            col_aligns,
            line_height=row_lh,
            fill=fill
        )
        
    current_y = pdf.get_y()
    available_space = 262 - current_y
    
    if available_space < 56:
        pdf.add_page()
        draw_continuation_header()
        current_y = pdf.get_y() + 4
        available_space = 262 - current_y
        
    gap_sig1 = max(11, min(20, available_space * 0.16))
    gap_sig2 = max(13, min(20, available_space * 0.18))
    
    calc_box_height = available_space - gap_sig1 - gap_sig2 - 10 - 5 - 8
    box_height = max(18, min(48, calc_box_height))
    
    y_sig = current_y + gap_sig1
    pdf.line(20, y_sig, 90, y_sig)
    pdf.line(126, y_sig, 196, y_sig)
    
    pdf.set_font("Arial", style="B", size=8.5)
    pdf.set_xy(20, y_sig + 1.5)
    pdf.cell(70, 4, "Firma del Responsable", align="C")
    pdf.set_xy(126, y_sig + 1.5)
    pdf.cell(70, 4, "Firma de Autorizacion", align="C")
    
    pdf.set_font("Arial", size=7.5)
    pdf.set_xy(20, y_sig + 5.5)
    pdf.cell(70, 3.5, clean_text(form_data['responsable']), align="C")
    pdf.set_xy(126, y_sig + 5.5)
    pdf.cell(70, 3.5, "MAESTRANZA BATERCON", align="C")
    
    y_obs_box = y_sig + 12.5
    pdf.set_xy(10, y_obs_box)
    pdf.set_font("Arial", style="B", size=8.0)
    pdf.set_text_color(74, 85, 104)
    pdf.cell(196, 4.5, "OBSERVACIONES DE SALIDA / RETORNO DE EQUIPO", ln=True)
    pdf.set_text_color(15, 17, 21)
    
    obs_text = form_data.get("observaciones", "")
    pdf.rect(10, pdf.get_y(), 196, box_height, "D")
    
    if obs_text:
        pdf.set_xy(12, pdf.get_y() + 1.5)
        pdf.set_font("Arial", size=8.0)
        pdf.multi_cell(192, 4.0, clean_text(obs_text), border=0)
        
    y_post_obs = y_obs_box + 4.5 + box_height
    y_sig_recep = y_post_obs + gap_sig2
    
    pdf.line(73, y_sig_recep, 143, y_sig_recep)
    pdf.set_font("Arial", style="B", size=8.5)
    pdf.set_xy(73, y_sig_recep + 1.5)
    pdf.cell(70, 4, "Revision / Recepcion de Retorno", align="C")
    
    pdf.set_font("Arial", size=7.5)
    pdf.set_xy(73, y_sig_recep + 5.5)
    pdf.cell(70, 3.5, "MAESTRANZA / CONTROL DE EQUIPOS", align="C")

    pdf.output(output_path)
    return output_path

def guardar_en_carpeta_especifica(nombre_archivo):
    nombre_carpeta = "Planillas_de_Salida"
    if getattr(sys, 'frozen', False):
        ruta_base = os.path.dirname(sys.executable)
    else:
        ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_destino = os.path.join(ruta_base, nombre_carpeta)
    if not os.path.exists(ruta_destino):
        os.makedirs(ruta_destino)
    return os.path.join(ruta_destino, nombre_archivo)

def main(page: ft.Page):
    page.title = "BATERCON - CONTROL DE SALIDA DE EQUIPOS"
    page.bgcolor = "#0F1115"
    page.padding = 20
    page.scroll = "adaptive"
    page.theme_mode = "dark"
    page.vertical_alignment = "start"
    page.horizontal_alignment = "start"
    
    items_state = []
    selected_category_state = "Reflexión de onda (PIT)"

    def show_message(text, is_error=False):
        color = "#E53E3E" if is_error else "green"
        sb = ft.SnackBar(ft.Text(text, color="white"), bgcolor=color)
        sb.open = True
        page.overlay.append(sb)
        page.update()

    logo_kwargs = {"width": 48, "height": 48, "fit": "contain"}
    if LOGO_BASE64:
        sig_img = inspect.signature(ft.Image.__init__)
        if "src_base64" in sig_img.parameters:
            logo_kwargs["src_base64"] = LOGO_BASE64
        else:
            logo_kwargs["src"] = f"data:image/jpeg;base64,{LOGO_BASE64}"
    else:
        logo_kwargs["src"] = "/logo_consultora.jpg"
        
    logo_control = ft.Image(**logo_kwargs)
    
    for cat, list_items in DEFAULT_INVENTARIO.items():
        for item in list_items:
            items_state.append({
                "category": cat,
                "item": item["item"],
                "serie": item["serie"],
                "cant": item["cant"],
                "salida": False,
                "retorno": False,
                "obs": ""
            })
            
    RESPONSABLES_OPTS = [
        "ING. FERNANDO BARRIENTOS",
        "ING. OMAR BARRIENTOS",
        "ING. PAOLA BARRIENTOS",
        "ING. LEONARDO PATZI",
        "ING. ADRIANA POMA A.",
        "TEC. MARCO RIOS",
        "TEC. GERMAN HILARY"
    ]

    VEHICULOS_OPTS = [
        "FORD SCORT 1984 (JUNIOR) 1343-ADA",
        "FORD RANGER 2008 (COQUETA) 2280-LLG",
        "NISSAN FRONTIER 2016 (PITUCA) 4231-PDI",
        "NISSAN FRONTIER 2023 (BICHOTA) 6269-RFF",
        "NISSAN FRONTIER 2024 (TESADORA) 6335-PSX",
        "CHANGAN HORNOR 2026 (ALBA) 6481-FEA",
        "CHANGAN ALSVIN 2024 (PITUFINA) 6335-PZR",
        "CHANGAN HUNTER 2023 (CAZADORA) 6007-NTU",
        "CHANGAN HUNTER 2023 (PUENTERA) 6008-KAS",
        "CHANGAN CS55 PLUS 2024 (---) 6353-XSH",
        "JAC X200i 2026 (AURORA) 6480-STU",
        "Otro (Especificar)"
    ]

    input_num_planilla = ft.TextField(label="Planilla N°", value="    /2026", border_color="#2D3748", focused_border_color="#E53E3E")
    input_lugar_fecha = ft.TextField(label="Lugar y Fecha", value=fecha_formateada, border_color="#2D3748", focused_border_color="#E53E3E")
    input_responsable = ft.Dropdown(
        label="Responsable",
        value="ING. OMAR BARRIENTOS",
        options=[ft.dropdown.Option(r) for r in RESPONSABLES_OPTS],
        border_color="#2D3748",
        focused_border_color="#E53E3E"
    )
    
    input_vehiculo = ft.Dropdown(
        label="Vehiculo/Placa",
        value="FORD SCORT 1984 (JUNIOR) 1343-ADA",
        options=[ft.dropdown.Option(v) for v in VEHICULOS_OPTS],
        border_color="#2D3748",
        focused_border_color="#E53E3E",
        text_size=12,
    )

    input_otro_nombre = ft.TextField(
        label="Nombre / Modelo del Vehículo Especial", 
        value="", 
        border_color="#E53E3E", 
        focused_border_color="red",
        hint_text="Ej: TOYOTA HILUX 2025",
        expand=True
    )
    input_otro_placa = ft.TextField(
        label="Número de Placa", 
        value="", 
        border_color="#E53E3E", 
        focused_border_color="red",
        hint_text="Ej: 5812-HUX",
        expand=True
    )

    otro_vehiculo_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Especifique los datos del vehículo personalizado:", size=11, color="#E53E3E", weight="bold"),
                ft.Row(controls=[input_otro_nombre, input_otro_placa], spacing=10)
            ],
            spacing=5
        ),
        col={"sm": 12},
        visible=False
    )

    def on_vehiculo_change(e):
        otro_vehiculo_container.visible = (input_vehiculo.value == "Otro (Especificar)")
        otro_vehiculo_container.update()
        page.update()
        
    input_vehiculo.on_change = on_vehiculo_change

    input_proyecto = ft.TextField(label="Proyecto", value="", border_color="#2D3748", focused_border_color="#E53E3E")
    input_orden_viaje = ft.TextField(label="Orden de Viaje", value="", border_color="#2D3748", focused_border_color="#E53E3E")
    input_empresa = ft.TextField(label="Empresa", value="", hint_text="", border_color="#2D3748", focused_border_color="#E53E3E")
    input_destino = ft.TextField(label="Destino", value="", border_color="#2D3748", focused_border_color="#E53E3E")
    input_observaciones = ft.TextField(label="Observaciones Generales de Salida / Retorno", multiline=True, min_lines=3, border_color="#2D3748", focused_border_color="#E53E3E")

    personal_dropdowns = [
        ft.Dropdown(
            label=f"Personal Asignado {i}",
            value="",
            options=[ft.dropdown.Option("")] + [ft.dropdown.Option(r) for r in RESPONSABLES_OPTS],
            border_color="#2D3748",
            focused_border_color="#E53E3E"
        )
        for i in range(1, 7)
    ]

    equipment_container = ft.Column(spacing=8)
    txt_totals_label = ft.Text("Equipos Marcados: 0", color="white", size=12, weight="bold")

    def sync_current_screen_controls():
        current_cat = selected_category_state
        cat_items = [x for x in items_state if str(x["category"]).strip().lower() == str(current_cat).strip().lower()]
        for itm in cat_items:
            if itm.get("_cb_salida") and itm["_cb_salida"].value is not None:
                itm["salida"] = bool(itm["_cb_salida"].value)
            if itm.get("_cb_retorno") and itm["_cb_retorno"].value is not None:
                itm["retorno"] = bool(itm["_cb_retorno"].value)
            if itm.get("_widget") and hasattr(itm["_widget"], "value") and itm["_widget"].value is not None:
                itm["item"] = itm["_widget"].value
            if itm.get("_serie") and itm["_serie"].value is not None:
                itm["serie"] = itm["_serie"].value
            if itm.get("_cant") and itm["_cant"].value is not None:
                itm["cant"] = itm["_cant"].value
            if itm.get("_obs") and itm["_obs"].value is not None:
                itm["obs"] = itm["_obs"].value

    def update_totals():
        current_cat = selected_category_state
        cat_items = [x for x in items_state if str(x["category"]).strip().lower() == str(current_cat).strip().lower()]
        selected_count = sum(1 for x in cat_items if x["salida"] or x["retorno"])
        total_cat = len(cat_items)
        txt_totals_label.value = f"Equipos Marcados: {selected_count} / {total_cat}"
        try:
            txt_totals_label.update()
        except Exception:
            pass

    def build_equipment_list():
        equipment_container.controls.clear()
        current_cat = selected_category_state
        category_items = [x for x in items_state if str(x["category"]).strip().lower() == str(current_cat).strip().lower()]
        
        for item in category_items:
            cb_salida = ft.Checkbox(
                value=item["salida"],
                active_color="#E53E3E",
                check_color="white",
                tooltip="Tiqueado de Salida"
            )
            def make_salida_handler(target_item):
                def handler(e):
                    target_item["salida"] = bool(e.control.value)
                    update_totals()
                return handler
            cb_salida.on_change = make_salida_handler(item)

            cb_retorno = ft.Checkbox(
                value=item["retorno"],
                active_color="#3182CE",
                check_color="white",
                tooltip="Tiqueado de Retorno"
            )
            def make_retorno_handler(target_item):
                def handler(e):
                    target_item["retorno"] = bool(e.control.value)
                    update_totals()
                return handler
            cb_retorno.on_change = make_retorno_handler(item)

            input_serie = ft.TextField(
                value=item["serie"],
                hint_text="Serie/ID",
                hint_style=ft.TextStyle(color="#718096", size=11),
                text_style=ft.TextStyle(color="white", size=12, font_family="monospace"),
                bgcolor="#0F1115",
                border_color="#2D3748",
                focused_border_color="#E53E3E",
                height=35,
                width=100,
                content_padding=5,
            )
            def make_serie_handler(target_item):
                def handler(e):
                    target_item["serie"] = e.control.value
                return handler
            input_serie.on_change = make_serie_handler(item)
            
            input_cant = ft.TextField(
                value=item["cant"],
                hint_text="Cant",
                text_style=ft.TextStyle(color="white", size=12, font_family="monospace"),
                bgcolor="#0F1115",
                border_color="#2D3748",
                focused_border_color="#E53E3E",
                height=35,
                width=50,
                content_padding=5,
                text_align="center"
            )
            def make_cant_handler(target_item):
                def handler(e):
                    target_item["cant"] = e.control.value
                return handler
            input_cant.on_change = make_cant_handler(item)

            input_row_obs = ft.TextField(
                value=item["obs"],
                hint_text="Observaciones",
                hint_style=ft.TextStyle(color="#718096", size=10),
                text_style=ft.TextStyle(color="white", size=11),
                bgcolor="#0F1115",
                border_color="#2D3748",
                focused_border_color="#E53E3E",
                height=35,
                width=120,
                content_padding=5,
            )
            def make_obs_handler(target_item):
                def handler(e):
                    target_item["obs"] = e.control.value
                return handler
            input_row_obs.on_change = make_obs_handler(item)

            if item.get("is_custom"):
                item_input = ft.TextField(
                    value=item["item"],
                    hint_text="Nombre del equipo",
                    text_style=ft.TextStyle(color="white", size=11, font_family="sans-serif", weight="bold"),
                    bgcolor="#0F1115",
                    border_color="#2D3748",
                    focused_border_color="#E53E3E",
                    height=35,
                    expand=True,
                    content_padding=5,
                )
                def make_item_name_handler(target_item):
                    def handler(e):
                        target_item["item"] = e.control.value
                    return handler
                item_input.on_change = make_item_name_handler(item)
                item_widget = item_input
            else:
                options = get_dropdown_options(item["category"], item["item"])
                if options:
                    current_val = item.get("item", "")
                    if not any(opt["item"] == current_val for opt in options):
                        options_names = [opt["item"] for opt in options]
                        current_val = options_names[0] if options_names else current_val
                        item["item"] = current_val

                    dropdown_items = [ft.dropdown.Option(opt["item"]) for opt in options]

                    item_dropdown = ft.Dropdown(
                        value=item["item"],
                        options=dropdown_items,
                        bgcolor="#0F1115",
                        border_color="#E53E3E",
                        text_style=ft.TextStyle(color="white", size=11, font_family="sans-serif", weight="bold"),
                        height=35,
                        expand=True,
                    )
                    
                    def make_dropdown_change_handler(target_item, dd_ctrl, serie_input_ctrl, opts):
                        def handler(e):
                            selected_name = e.control.value if (e.control and e.control.value is not None) else e.data
                            if not selected_name:
                                selected_name = dd_ctrl.value

                            target_item["item"] = selected_name
                            dd_ctrl.value = selected_name

                            matched = next((opt for opt in opts if opt.get("item") == selected_name), None)
                            if matched:
                                nueva_serie = matched.get("serie", "")
                                target_item["serie"] = nueva_serie
                                serie_input_ctrl.value = nueva_serie
                                try:
                                    serie_input_ctrl.update()
                                except Exception:
                                    pass
                            page.update()
                        return handler

                    item_dropdown.on_change = make_dropdown_change_handler(item, item_dropdown, input_serie, options)
                    item_widget = item_dropdown
                else:
                    item_widget = ft.Container(
                        expand=True,
                        content=ft.Text(
                            item["item"],
                            color="#E2E8F0",
                            size=11,
                            font_family="sans-serif",
                            weight="bold",
                        )
                    )

            item["_cb_salida"] = cb_salida
            item["_cb_retorno"] = cb_retorno
            item["_widget"] = item_widget
            item["_serie"] = input_serie
            item["_cant"] = input_cant
            item["_obs"] = input_row_obs

            row_card = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Column([ft.Text("Salida", size=8, color="#718096"), cb_salida], horizontal_alignment="center", spacing=0),
                        ft.Column([ft.Text("Retorno", size=8, color="#718096"), cb_retorno], horizontal_alignment="center", spacing=0),
                        ft.VerticalDivider(color="#2D3748", width=1),
                        item_widget,
                        input_serie,
                        input_cant,
                        input_row_obs,
                    ],
                    alignment="spaceBetween",
                    vertical_alignment="center",
                ),
                padding=8,
                bgcolor="#1A202C",
                border=make_border("#2D3748", 1)
            )
            equipment_container.controls.append(row_card)
        
        try:
            if equipment_container.page:
                equipment_container.update()
        except Exception:
            pass  

    category_pills_row = ft.Row(wrap=True, spacing=6)
    def update_category_pills():
        category_pills_row.controls.clear()
        for cat in DEFAULT_INVENTARIO.keys():
            cat_clean = str(cat).strip()
            cat_items = [x for x in items_state if str(x["category"]).strip().lower() == cat_clean.lower()]
            selected_cnt = sum(1 for x in cat_items if x["salida"] or x["retorno"])
            total_cnt = len(cat_items)
            is_active = (cat_clean.lower() == str(selected_category_state).strip().lower())

            def make_pill_click(target_cat):
                return lambda e: switch_category(target_cat)

            border_col = "#E53E3E" if is_active else "#2D3748"
            pill_container = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(cat, color="white" if is_active else "#A0AEC0", size=11, weight="bold"),
                        ft.Container(
                            content=ft.Text(f"{selected_cnt}/{total_cnt}", color="white" if is_active else "#718096", size=10, weight="bold", font_family="monospace"),
                            bgcolor="black" if is_active else "#0F1115",
                            padding=ft.Padding(5, 2, 5, 2),
                            border_radius=4
                        )
                    ],
                    spacing=6,
                    tight=True
                ),
                bgcolor="#E53E3E" if is_active else "#1A202C",
                padding=ft.Padding(10, 6, 10, 6),
                border_radius=8,
                border=make_border(border_col, 1),
                on_click=make_pill_click(cat),
                ink=True
            )
            category_pills_row.controls.append(pill_container)

    def switch_category(new_cat):
        nonlocal selected_category_state
        if not new_cat:
            return
        sync_current_screen_controls()
        selected_category_state = str(new_cat).strip()
        build_equipment_list()
        update_totals()
        update_category_pills()
        try:
            page.update()
        except Exception:
            pass

    def toggle_select_all_category(e):
        sync_current_screen_controls()
        cat_items = [x for x in items_state if str(x["category"]).strip().lower() == str(selected_category_state).strip().lower()]
        all_salida = all(x["salida"] for x in cat_items)
        target_val = not all_salida
        for x in cat_items:
            x["salida"] = target_val
        build_equipment_list()
        update_totals()
        update_category_pills()
        page.update()

    btn_select_all = ft.OutlinedButton(
        "MARCAR / DESMARCAR SALIDAS",
        style=ft.ButtonStyle(
            color="white",
            side=ft.BorderSide(1, "#2D3748"),
            shape=ft.RoundedRectangleBorder(radius=6)
        ),
        on_click=toggle_select_all_category,
        height=36
    )

    def on_add_custom_item(e):
        sync_current_screen_controls()
        current_cat = selected_category_state
        new_custom = {
            "category": current_cat,
            "item": "Nuevo Accesorio Extra",
            "serie": "",
            "cant": "1",
            "salida": True,
            "retorno": False,
            "obs": "",
            "is_custom": True
        }
        current_cat_lower = str(current_cat).strip().lower()
        last_idx = -1
        for idx, itm in enumerate(items_state):
            if str(itm.get("category")).strip().lower() == current_cat_lower:
                last_idx = idx
        if last_idx != -1:
            items_state.insert(last_idx + 1, new_custom)
        else:
            items_state.append(new_custom)

        build_equipment_list()
        update_totals()
        update_category_pills()
        page.update()
        
    btn_add_custom = ft.FilledButton(
        "AGREGAR EQUIPO EXTRA",
        icon="add",
        style=ft.ButtonStyle(
            color="white",
            bgcolor="#E53E3E",
            elevation=2,
            shape=ft.RoundedRectangleBorder(radius=6)
        ),
        on_click=on_add_custom_item,
        height=36
    )
    
    def on_submit(e):
        sync_current_screen_controls()
        
        items_seleccionados = [x for x in items_state if x.get("salida", False) or x.get("retorno", False)]
        if not items_seleccionados:
            show_message("Error: Marque al menos un equipo en salida o retorno.", is_error=True)
            return
        
        if input_vehiculo.value == "Otro (Especificar)":
            nombre_esp = input_otro_nombre.value.strip()
            placa_esp = input_otro_placa.value.strip()
            if nombre_esp or placa_esp:
                vehiculo_final = f"{nombre_esp} - {placa_esp}".strip(" -")
            else:
                vehiculo_final = "Especificar: "
        else:
            vehiculo_final = input_vehiculo.value
        
        form_data = {
            "num_planilla": input_num_planilla.value,
            "lugar_fecha": input_lugar_fecha.value,
            "responsable": input_responsable.value,
            "vehiculo": vehiculo_final,
            "proyecto": input_proyecto.value,
            "orden_viaje": input_orden_viaje.value,
            "empresa": input_empresa.value,
            "destino": input_destino.value,
            "observaciones": input_observaciones.value,
            "personal": [dd.value for dd in personal_dropdowns if dd.value]
        }
    
        clean_num_planilla = input_num_planilla.value.strip().replace("/", "-").replace("\\", "-").replace(":", "-").replace("*", "-").replace("?", "-").replace("\"", "-").replace("<", "-").replace(">", "-").replace("|", "-")
        if not clean_num_planilla: 
            clean_num_planilla = "PLANILLA"
        
        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        filename = f"Planilla_{clean_num_planilla}_{timestamp}.pdf"
    
        ruta_final = guardar_en_carpeta_especifica(filename)
    
        try:
            generate_pdf(form_data, items_seleccionados, ruta_final)
            show_message(f"Guardado exitosamente en: {ruta_final}")
            
            for itm in items_state:
                itm["salida"] = False
                itm["retorno"] = False
                itm["obs"] = ""
            input_observaciones.value = ""
            build_equipment_list()
            update_totals()
            update_category_pills()
            page.update()

        except Exception as ex:
            show_message(f"Error al guardar: {str(ex)}", is_error=True)

    btn_generate = ft.ElevatedButton(
        "GENERAR PLANILLA PDF",
        icon="picture_as_pdf",
        style=ft.ButtonStyle(
            color="white",
            bgcolor="#2E7D32",
            elevation=3,
            shape=ft.RoundedRectangleBorder(radius=6)
        ),
        on_click=on_submit,
        height=48
    )

    header_block = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=logo_control,
                            bgcolor="white",
                            padding=4,
                            border_radius=4,
                            border=make_border("#E53E3E", 1)
                        ),
                        ft.Container(
                            content=ft.Text("BATERCON", color="white", weight="bold", size=24),
                            bgcolor="#E53E3E",
                            padding=ft.Padding(left=8, top=15, right=8, bottom=15)
                        ),
                    ],
                    spacing=10
                ),
                ft.Column(
                    controls=[
                        ft.Text("BARRIENTOS TERÁN CONSULTORES", color="white", size=14, weight="bold"),
                        ft.Text("SISTEMA DE INVENTARIO ", color="#E53E3E", size=10, weight="bold")
                    ],
                    spacing=2
                )
            ],
            alignment="spaceBetween"
        ),
        padding=10,
        bgcolor="#1A202C",
        border=ft.Border(bottom=ft.BorderSide(2, "#E53E3E"))
    )

    form_grid = ft.Column(
        controls=[
            ft.Text("DATOS GENERALES DE LA COMISIÓN", size=12, weight="bold", color="#E2E8F0"),
            ft.ResponsiveRow(
                controls=[
                    ft.Container(input_num_planilla, col={"sm": 6, "md": 4}),
                    ft.Container(input_lugar_fecha, col={"sm": 6, "md": 4}),
                    ft.Container(input_responsable, col={"sm": 6, "md": 4}),
                    ft.Container(input_vehiculo, col={"sm": 6, "md": 4}),
                    otro_vehiculo_container,
                    ft.Container(input_proyecto, col={"sm": 6, "md": 4}),
                    ft.Container(input_orden_viaje, col={"sm": 6, "md": 4}),
                    ft.Container(input_empresa, col={"sm": 6, "md": 4}),
                    ft.Container(input_destino, col={"sm": 12, "md": 8}),
                ]
            )
        ],
        spacing=10
    )

    checklist_block = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Text("Lista de Equipamiento e Inventario", size=14, weight="bold", color="#E2E8F0"),
                    txt_totals_label
                ],
                alignment="spaceBetween"
            ),
            category_pills_row,
            ft.Row(
                controls=[
                    ft.Text("ACCESORIOS EN LA CATEGORÍA SELECCIONADA", size=11, color="#718096", font_family="monospace"),
                    ft.Row(
                        controls=[
                            btn_select_all,
                            btn_add_custom
                        ],
                        spacing=8
                    )
                ],
                alignment="spaceBetween"
            ),
            equipment_container
        ],
        spacing=10
    )

    personal_grid = ft.ResponsiveRow(
        controls=[
            ft.Container(dd, col={"sm": 6, "md": 4}) for dd in personal_dropdowns
        ]
    )

    personal_block = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("PERSONAL ASIGNADO EN COMISIÓN (Hasta 6 personas)", size=12, weight="bold", color="#E2E8F0"),
                personal_grid
            ],
            spacing=10
        ),
        padding=15,
        bgcolor="#1A202C",
        border=make_border("#2D3748", 1)
    )

    footer_actions = ft.Container(
        content=ft.Column(
            controls=[
                input_observaciones,
                ft.Row(controls=[btn_generate], alignment="end")
            ],
            spacing=10
        ),
        padding=15,
        bgcolor="#1A202C",
        border=make_border("#2D3748", 1)
    )

    page.add(
        header_block,
        ft.Divider(height=10, color="transparent"),
        form_grid,
        ft.Divider(height=15, color="#2D3748"),
        checklist_block,
        ft.Divider(height=15, color="#2D3748"),
        personal_block,
        ft.Divider(height=15, color="#2D3748"),
        footer_actions
    )

    build_equipment_list()
    update_totals()
    update_category_pills()

if __name__ == "__main__":
    ft.app(target=main, assets_dir="public")