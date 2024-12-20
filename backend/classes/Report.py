import sqlite3
from typing import get_type_hints
from backend.classes.utils import verify_type
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
import os


class Report:
    def __init__(self, file_location: str, agreement: str) -> None:
        verify_type(get_type_hints(Report.__init__), locals())
        self.__images_location: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "interface",
        "images"
        ).replace("\\", "/")
        self.__file_location: str = file_location
        self.__agreement: str = agreement
        self.__horizontal_size: int = 595
        self.__vertical_size: int = 842
        self.__pdf: canvas.Canvas | None = None
        self.__standard_paragraph_style = ParagraphStyle(name='Normal', fontName='arial', fontSize=8, alignment=TA_CENTER)
        self.__standard_paragraph_style_bold = ParagraphStyle(name='Normal', fontName='arialbd', fontSize=8, alignment=TA_CENTER)
        self.__left_col_width : list[float] = [49, 28.448, 25.2, 25.2, 25.2, 25.2, 25.2]
        self.__right_col_width: list[float] = [85.78125, 30.672, 25.2, 25.2, 25.2, 25.2, 25.2]
        self.__sample_info_map = {
            "Ca2+ cmolcdm-3": "calcium",
            "Mg² cmolcdm-3": "magnesium",
            "K cmolcdm-3": "potassium",
            "MO gdm-3": "organic_matter",
            "P mgdm-3": "phosphorus",
            "pH-CaCl2": "ph",
            "Al3+ cmolcdm-3": "aluminum",
            "H+Al cmolcdm-3": "h_al",
            "Índice SMP": "smp",
            "Cu mgdm-3": "copper",
            "Zn mgdm-3": "zinc",
            "Mn mgdm-3": "manganese",
            "Fe mgdm-3": "iron",
            "Soma de Bases cmolcdm-3": "base_sum",
            "CTC efetiva (t) cmolcdm-3": "effective_ctc",
            "CTC Potencial (T) cmolcdm-3": "ctc",
            "Saturação por bases (V)%": "v_percent",
            "Saturação por alumínio (m)%": "aluminum_saturation",
        }

    def add_fonts(self) -> None:
        pdfmetrics.registerFont(TTFont('arial', 'fonts/arial.ttf'))
        pdfmetrics.registerFont(TTFont('arialbd', 'fonts/arialbd.ttf'))
        pdfmetrics.registerFont(TTFont('arialbi', 'fonts/arialbi.ttf'))
        pdfmetrics.registerFont(TTFont('ariali', 'fonts/ariali.ttf'))
        pdfmetrics.registerFont(TTFont('arilbk', 'fonts/ariblk.ttf'))

    def setup_pdf(self, number: int, path: str) -> canvas.Canvas:
        self.add_fonts()
        pdf: canvas.Canvas = canvas.Canvas(f'{path}')
        pdf.setTitle(f'Laudo - {number}')
        return pdf

    def draw_header(self) -> None:
        self.__pdf.setStrokeColor('yellow')
        self.__pdf.line(30, 745, 560, 745)
        self.__pdf.setStrokeColor('black')
        self.__pdf.line(30, 750, 560, 750)
        self.__pdf.setFont('arialbd', 14)
        self.__pdf.drawCentredString(self.__horizontal_size / 2, 725, 'Laudo de Análise de Solo')
        self.__pdf.drawImage(f'{self.__images_location}/UTFPR_logo.svg.png', 65, 725, 100, 100, preserveAspectRatio=True, mask='auto')
        self.__pdf.setFont('arialbd', 10)
        self.__pdf.drawCentredString(self.__horizontal_size / 2, 785, 'LABSOLOS - Laboratório de Solos da UTFPR')
        self.__pdf.setFont('arial', 10)
        self.__pdf.drawCentredString(self.__horizontal_size / 2, 772, 'Universidade Tecnólogica Federal do Paraná')
        self.__pdf.drawCentredString(self.__horizontal_size / 2, 759, 'Campus Pato Branco')
        self.__pdf.drawImage(f'{self.__images_location}/logo_lab.png', 410, 730, 125, 125, preserveAspectRatio=True, mask='auto')
        self.__pdf.setFont('arial', 8)

    def draw_square(self, pos_horizontal1: int, pos_horizontal2: int, pos_vertical1: int,
                    pos_vertical2: int) -> None:
        self.__pdf.line(pos_horizontal1, pos_vertical1, pos_horizontal2, pos_vertical1)
        self.__pdf.line(pos_horizontal1, pos_vertical1, pos_horizontal1, pos_vertical2)
        self.__pdf.line(pos_horizontal1, pos_vertical2, pos_horizontal2, pos_vertical2)
        self.__pdf.line(pos_horizontal2, pos_vertical1, pos_horizontal2, pos_vertical2)

    def write_main_info_square(self, info: sqlite3.Row, report_id: int) -> None:
        x_start: int = 75
        x_end: int = 515
        y_start: int = 710
        acceptable_width: int = x_end - x_start
        self.__pdf.setFont('arial', 10)
        current_x: float = x_start
        current_y: int = y_start
        document_text: str = f"CPF: {info['document_number']}" if info["document_type"] == "cpf" else f"CNPJ: {info['document_number']}"
        texts_to_draw: list[str] = [
        f"Solicitante: {info['requester_name']} ?{document_text}",
        f"Propriedade: {info['property_name']} ?Município: {info['city']} ?UF: {info['state']} ?Matrícula: {info['registration_number']}",
        f"Talhão: {info['sample_description']} ?Convênio: {self.__agreement} ?Profundidade: {info['depth']}cm ?Área: {info['total_area']}m²",
        f"Laudo: {report_id} ?Amostra: {info['sample_number']} ?Data: {info['collection_date']}",
        ]

        def justify_text(text: str, max_width: int) -> str:
            words = text.split("?")
            words = [word for word in words if word != ' ' and word != '']
            if len(words) == 1:
                return words[0]
            words_width = sum(pdfmetrics.stringWidth(word, 'arial', 10) for word in words)
            space_width = pdfmetrics.stringWidth(' ', 'arial', 10)
            available_spaces = ((max_width - words_width) / space_width) - 2
            space_step = int(available_spaces//(len(words) - 1))
            justified_line = words[0]
            for i in range(1, len(words)):
                justified_line += ' ' + ' ' * space_step + words[i]
            return justified_line

        def break_line(text):
            fields: list[str] = text.split("?")
            current_text = fields[0]
            for j in range(1, len(fields)):
                if pdfmetrics.stringWidth(current_text + fields[j], 'arial', 10) > acceptable_width:
                    break
                else:
                    current_text += fields[j]
            return {'current_line': current_text, 'next_line': text[len(current_text):]}

        def fit_text_size(text, current_y):
            breaked_lines: dict[str, str] = break_line(text)
            self.__pdf.drawString(x_start, current_y, justify_text(breaked_lines['current_line'], x_end-x_start))
            current_y -= 12
            while pdfmetrics.stringWidth(breaked_lines['next_line'], 'arial', 10) > acceptable_width:
                breaked_lines: dict[str, str] = break_line(breaked_lines['next_line'])
                self.__pdf.drawString(x_start, current_y, justify_text(breaked_lines['current_line'], x_end-x_start))
                current_y -= 12
            if breaked_lines['next_line']:
                self.__pdf.drawString(x_start, current_y, justify_text(breaked_lines['next_line'], x_end-x_start))
                current_y -= 12
            return current_y

        for line in texts_to_draw:
            text_size: float = pdfmetrics.stringWidth(line, 'arial', 10)
            if text_size + current_x > x_end:
                current_y = fit_text_size(line, current_y)
            else:
                self.__pdf.drawString(x_start, current_y, justify_text(line, x_end-x_start))
                current_y -= 12
        self.draw_square(x_start - 5, x_end + 5, y_start + 10, current_y+2)
        return current_y - 5

    def draw_footer(self, coord_y):
        self.draw_square(70, 520, coord_y+35, coord_y)
        self.__pdf.setFont('arial', 8)
        self.__pdf.drawCentredString(self.__horizontal_size / 2, coord_y + 25,
                              f"Laboratório de Análise de Solo  - UTFPR")
        self.__pdf.drawCentredString(self.__horizontal_size / 2, coord_y + 15,
                              f"Via do conhecimento, KM 01, caixa postal 57, CEP 85503-390, Pato Branco - PR")
        self.__pdf.drawCentredString(self.__horizontal_size / 2, coord_y + 5,
                              f"Telefone/WhatsApp: (46) 3220-2539, E-mail: labsolos-pb@utfpr.edu.br")

    def find_line(self, element, value, reference):
        reference = reference[self.__sample_info_map[element]]
        if value < reference["very low"]:
            return 1
        elif value < reference["low"]:
            return 2
        elif value < reference["medium"]:
            return 3
        elif value < reference["high"]:
            return 4
        else:
            return 5

    def draw_ruler(self):
        self.__pdf.drawString(100, 810, 'x100')
        self.__pdf.drawString(200, 810, 'x200')
        self.__pdf.drawString(300, 810, 'x300')
        self.__pdf.drawString(400, 810, 'x400')
        self.__pdf.drawString(500, 810, 'x500')
        self.__pdf.drawString(10, 100, 'y100')
        self.__pdf.drawString(10, 200, 'y200')
        self.__pdf.drawString(10, 300, 'y300')
        self.__pdf.drawString(10, 400, 'y400')
        self.__pdf.drawString(10, 500, 'y500')
        self.__pdf.drawString(10, 600, 'y600')
        self.__pdf.drawString(10, 700, 'y700')
        self.__pdf.drawString(10, 800, 'y800')

    def draw_table(self, data, coord_x, coord_y, colwidths, reference) -> None:
        for row in data:
            if row[1] == 'None':
                data.remove(row)

        style = TableStyle([
            ('BACKGROUND', (0, 0), (6, 0), colors.lightgrey),
            ('SPAN', (0, 0), (1, 0)),
            ('SPAN', (2, 0), (6, 0)),
            ('FONTNAME', (0, 0), (6, 0), 'arialbd'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 3),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8)
        ])
        standard_size = 0.3
        table = Table(data, style=style,
                      colWidths=colwidths if colwidths is not None else [None, None, standard_size * inch,
                                                                         standard_size * inch, standard_size * inch
                          , standard_size * inch, standard_size * inch])
        table.wrapOn(self.__pdf, 0, 0)
        table.drawOn(self.__pdf, coord_x, coord_y)
        current_y = coord_y
        start_x = coord_x + table._colWidths[0] + table._colWidths[1]
        self.__pdf.setLineWidth(3)
        self.__pdf.setStrokeColor(colors.gray)
        for j in range(len(data) - 1, 0 - 1, -1):
            if isinstance(data[j][0], str) or data[j][0].getPlainText() not in self.__sample_info_map.keys():
                continue
            current_y = current_y + table._rowHeights[j]/2
            self.__pdf.line(start_x, current_y, start_x + 25.2*self.find_line(data[j][0].getPlainText(), float(data[j][1]), reference), current_y)
            current_y = current_y + table._rowHeights[j]/2
        self.__pdf.setLineWidth(1)
        self.__pdf.setStrokeColor(colors.black)

    def draw_pie_graph_table(self, coord_x, coord_y) -> None:
        data = [['Índice de Saturação'],
                ['']]
        style = TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), colors.lightgrey),
            ('FONTNAME', (0, 0), (0, 0), 'arialbd'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 3),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8)
        ])
        table = Table(data, style=style, colWidths=[242.45324999999994], rowHeights=[None, 1.5 * inch])
        table.wrapOn(self.__pdf, 0, 0)
        table.drawOn(self.__pdf, coord_x, coord_y)


    def draw_granulometric_table(self, coord_x, coord_y, sample_values) -> None:
        data = [['ANÁLISE GRANULOMÉTRICA(g kg^-1)**'],
                ['Areia', 'Silte', 'Argila', 'Classe AD'],
                [f"{sample_values['sand']}", f"{sample_values['silte']}", f"{sample_values['clay']}", f"{sample_values['classification']}"]]
        style = TableStyle([
            ('BACKGROUND', (0, 0), (3, 0), colors.lightgrey),
            ('SPAN', (0, 0), (3, 0)),
            ('FONTNAME', (0, 0), (3, 0), 'arialbd'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 3),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8)
        ])
        table = Table(data, style=style, colWidths=242.45324999999994 / 4)
        table.wrapOn(self.__pdf, 0, 0)
        table.drawOn(self.__pdf, coord_x, coord_y)


    def draw_extractor_graph(self, coord_x, coord_y) -> None:
        data = [['EXTRATORES'],
                ['Ca, Mg e Al', 'KCl 1M'],
                ['MO', 'Combustão úmida'],
                ['P, K, Cu, Fe, Zn e Mn', 'Mehlich-1'],
                ['pH em CaCl2 ou H20', 'Proporção 1:2.5']]
        style = TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
            ('SPAN', (0, 0), (1, 0)),
            ('FONTNAME', (0, 0), (1, 0), 'arialbd'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 3),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8)
        ])
        table = Table(data, style=style, colWidths=242.45324999999994 / 2)
        table.wrapOn(self.__pdf, 0, 0)
        table.drawOn(self.__pdf, coord_x, coord_y)




    def draw_tables(self, sample_values: sqlite3.Row, reference):
        data_table_one = [['BÁSICA', '', 'Classe de Interpretação*'],
                          ['Elemento', 'Teor', 'MB', 'B', 'M', 'A', 'MA'],
                          [Paragraph('Ca<sup>2+</sup> cmolcdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["calcium"]}'],
                          [Paragraph('Mg² cmolcdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["magnesium"]}'],
                          [Paragraph('K cmolcdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["potassium"]}'],
                          [Paragraph('MO gdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["organic_matter"]}'],
                          [Paragraph('P mgdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["phosphorus"]}']]
        self.draw_table(data_table_one, 70, 480, self.__left_col_width, reference)
        data_table_two = [['REAÇÃO DO SOLO', '', 'Classe de Interpretação*'],
                          ['Parâmetro', 'Valor', 'MB', 'B', 'M', 'A', 'MA'],
                          [Paragraph('pH-CaCl2', style=self.__standard_paragraph_style), f'{sample_values["ph"]}'],
                          [Paragraph('Al<sup>3+</sup> cmolcdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["aluminum"]}'],
                          [Paragraph('H+Al cmolcdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["h_al"]}'],
                          [Paragraph('Índice SMP', style=self.__standard_paragraph_style), f'{sample_values["smp"]}']]
        self.draw_table(data_table_two, 278, 534, self.__right_col_width, reference)
        data_table_three = [['MICRONUTRIENTES', '', 'Classe de Interpretação*'],
                            ['Elemento', 'Teor', 'MB', 'B', 'M', 'A', 'MA'],
                            [Paragraph('Cu mgdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["copper"]}'],
                            [Paragraph('Zn mgdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["zinc"]}'],
                            [Paragraph('Mn mgdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["manganese"]}'],
                            [Paragraph('Fe mgdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["iron"]}']
                            ]
        self.draw_table(data_table_three, 278, 426, self.__right_col_width, reference)
        data_table_four = [
            [Paragraph('PARÂMETROS CALCULADOS', style=self.__standard_paragraph_style_bold), '', 'Classe de Interpretação*'],
            ['Parâmetro', 'Valor', 'MB', 'B', 'M', 'A', 'MA'],
            [Paragraph('Soma de Bases cmolcdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["base_sum"]}'],
            [Paragraph('CTC efetiva (t) cmolcdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["effective_ctc"]}'],
            [Paragraph('CTC Potencial (T) cmolcdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["ctc"]}'],
            [Paragraph('Saturação por bases (V)%', style=self.__standard_paragraph_style), f'{sample_values["v_percent"]}'],
            [Paragraph('Saturação por alumínio (m)%', style=self.__standard_paragraph_style), f'{sample_values["aluminum_saturation"]}']
        ]
        self.draw_table(data_table_four, 70, 186, self.__left_col_width, reference)
        self.draw_pie_graph_table(278, 300)
        self.draw_granulometric_table(278, 246, sample_values)
        self.draw_extractor_graph(278, 156)
        self.__pdf.drawImage(f'{self.__images_location}/ctc_and_values.png', 278 + 65, 305, 108, 108, preserveAspectRatio=True, mask='auto')

    def draw_signature_space(self, coord_x, coord_y, table_size):
        self.__pdf.setFont('arialbd', 10)
        self.__pdf.line(coord_x, coord_y, coord_x + table_size, coord_y)
        self.__pdf.drawCentredString(table_size / 2 + 70, coord_y - 11, 'Assinatura')

    def write_explanation(self, coord_y):
        self.__pdf.setFont('arial', 7)
        self.__pdf.drawCentredString(self.__horizontal_size / 2, coord_y,
                              '* Baseado no Manual de Adubação e calagem para o estado do Paraná (NEPAR-BCS, 2019)')
        self.__pdf.drawCentredString(self.__horizontal_size / 2, coord_y - 10, '** De acordo com o Zoneamento Agrícola de Risco Climático'
                                     ' (ZARC), IN SPA/MAPA nº 01 de 21 de junho de 2022, do MAPA')

    def generate_pdf(self, report_data: sqlite3.Row, path_to_save: str, report_id: int, sample_values: sqlite3.Row, reference: dict[str, dict[str, float]]) -> None:
        self.__pdf = self.setup_pdf(report_id, path_to_save)
        self.draw_header()
        self.write_main_info_square(report_data, report_id)
        self.draw_footer(40)
        self.draw_tables(sample_values, reference)
        self.draw_signature_space(70, 156, 203.44799999999998)
        self.write_explanation(90)
        self.__pdf.save()


