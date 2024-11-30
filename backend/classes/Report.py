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
    def __init__(self, file_location: str, technician: str) -> None:
        verify_type(get_type_hints(Report.__init__), locals())
        self.__images_location: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "interface",
        "images"
        ).replace("\\", "/")
        self.__file_location: str = file_location
        self.__technician: str = technician
        self.__horizontal_size: int = 595
        self.__vertical_size: int = 842
        self.__pdf: canvas.Canvas | None = None
        self.__standard_paragraph_style = ParagraphStyle(name='Normal', fontName='arial', fontSize=8, alignment=TA_CENTER)
        self.__standard_paragraph_style_bold = ParagraphStyle(name='Normal', fontName='arialbd', fontSize=8, alignment=TA_CENTER)

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
        self.__pdf.drawImage(f'{self.__images_location}/logo_lab-no-bg.png', 410, 730, 125, 125, preserveAspectRatio=True, mask='auto')
        self.__pdf.setFont('arial', 8)

    def draw_square(self, pos_horizontal1: int, pos_horizontal2: int, pos_vertical1: int,
                    pos_vertical2: int) -> None:
        self.__pdf.line(pos_horizontal1, pos_vertical1, pos_horizontal2, pos_vertical1)
        self.__pdf.line(pos_horizontal1, pos_vertical1, pos_horizontal1, pos_vertical2)
        self.__pdf.line(pos_horizontal1, pos_vertical2, pos_horizontal2, pos_vertical2)
        self.__pdf.line(pos_horizontal2, pos_vertical1, pos_horizontal2, pos_vertical2)

    def write_main_info_square(self, info: sqlite3.Row, report_id: int) -> None:
        self.draw_square(70, 520, 720, 665)
        self.__pdf.setFont('arial', 10)
        self.__pdf.drawString(75, 710, f"Solicitante: {info['requester_name']}")
        self.__pdf.drawString(75, 700, f"Endereço: {info['address']}")
        self.__pdf.drawString(75, 690, f"Propriedade: {info['property_name']}")
        self.__pdf.drawString(75, 680, f"Talhão: {info['sample_number']}") #mudar conforme andressa pediu
        self.__pdf.drawString(75, 670, f"Convênio: {self.__technician}")
        self.__pdf.drawString(400, 710, f"Laudo: {report_id}") # mudar conforme andressa pediu
        self.__pdf.drawString(400, 700, f"Descrição: {info['sample_description']}")
        self.__pdf.drawString(400, 690, f"Data: {info['collection_date']}")
        self.__pdf.drawString(400, 680, f"Profundidade: {info['depth']} cm")
        self.__pdf.drawString(400, 670, f"Nº Matrícula: {info['registration_number']}")

    def draw_footer(self, coord_y):
        self.draw_square(70, 520, coord_y+35, coord_y)
        self.__pdf.setFont('arial', 8)
        self.__pdf.drawCentredString(self.__horizontal_size / 2, coord_y + 25,
                              f"Laboratório de Análise de Solo  - UTFPR")
        self.__pdf.drawCentredString(self.__horizontal_size / 2, coord_y + 15,
                              f"Via do conhecimento, KM 01, caixa postal 57, CEP 85503-390, Pato Branco - PR")
        self.__pdf.drawCentredString(self.__horizontal_size / 2, coord_y + 5,
                              f"Telefone/WhatsApp: (46) 3220-2539, E-mail: labsolos-pb@utfpr.edu.br")

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

    def draw_table(self, data, coord_x, coord_y, colwidths) -> None:
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
        standard_size = 0.35
        table = Table(data, style=style,
                      colWidths=colwidths if colwidths is not None else [None, None, standard_size * inch,
                                                                         standard_size * inch, standard_size * inch
                          , standard_size * inch, standard_size * inch])
        table.wrapOn(self.__pdf, 0, 0)
        table.drawOn(self.__pdf, coord_x, coord_y)
        w, h = table.wrap(0, 0)
        print(f'col: {w}, row:{h}')

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
        w, h = table.wrap(0, 0)
        print(f'col: {w}, row:{h}')
        print(table._rowHeights)
        print(table._colWidths)

    def draw_granulometric_table(self, coord_x, coord_y) -> None:
        data = [['ANÁLISE GRANULOMÉTRICA(g kg^-1)**'],
                ['Areia', 'Slite', 'Argila', 'Classe AD'],
                ['41', '130', '829', 'AD3']]
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
        w, h = table.wrap(0, 0)
        print(f'col: {w}, row:{h}')

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
        w, h = table.wrap(0, 0)
        print(f'col: {w}, row:{h}')

    def draw_explanation_table(self, coord_x, coord_y) -> None:
        standard_paragraph_style = ParagraphStyle(
            name='Normal',
            fontName='arial',
            fontSize=6,
            alignment=TA_CENTER
        )
        data = [['EMBASAMENTO'],
                [Paragraph('* Baseado no Manual de Adubação e calagem para o estado do Paraná (NEPAR-BCS, 2019)',
                           style=standard_paragraph_style),
                 Paragraph('** De acordo com o Programa Nacional de Zoneamento Agrícola de Risco Climático (ZARC), '
                           'regido pela Instrução Normativa – IN SPA/MAPA nº 01, de 21 de junho  de 2022, da Secretaria '
                           'de Política Agrícola do MAPA.', style=standard_paragraph_style)]]
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
        table = Table(data, style=style, colWidths=203.44799999999998 / 2)
        table.wrapOn(self.__pdf, 0, 0)
        table.drawOn(self.__pdf, coord_x, coord_y)
        w, h = table.wrap(0, 0)
        print(f'col: {w}, row:{h}')

    def draw_tables(self, sample_values: sqlite3.Row):
        data_table_one = [['BÁSICA', '', 'Classe de Interpretação*'],
                          ['Elemento', 'Teor', 'MB', 'B', 'M', 'A', 'MA'],
                          [Paragraph('Ca<sup>2+</sup> cmolcdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["calcium"]}'],
                          [Paragraph('Mg² cmolcdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["magnesium"]}'],
                          [Paragraph('K cmolcdm<sup>-3</sup>³', style=self.__standard_paragraph_style), f'{sample_values["potassium"]}'],
                          [Paragraph('MO gdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["organic_matter"]}'],
                          [Paragraph('P mgdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["phosphorus"]}']]
        self.draw_table(data_table_one, 70, 480, [49, 28.448, 25.2, 25.2, 25.2, 25.2, 25.2])
        data_table_two = [['REAÇÃO DO SOLO', '', 'Classe de Interpretação*'],
                          ['Parâmetro', 'Valor', 'MB', 'B', 'M', 'A', 'MA'],
                          [Paragraph('pH-CaCl2', style=self.__standard_paragraph_style), f'{sample_values["ph"]}'],
                          [Paragraph('Al<sup>3+</sup> cmolcdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["aluminum"]}'],
                          [Paragraph('H+Al cmolcdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["h_al"]}'],
                          [Paragraph('Índice SMP', style=self.__standard_paragraph_style), f'{sample_values["smp"]}'], ]
        self.draw_table(data_table_two, 278, 534, None)
        data_table_three = [['MICRONUTRIENTES', '', 'Classe de Interpretação*'],
                            ['Elemento', 'Teor', 'MB', 'B', 'M', 'A', 'MA'],
                            [Paragraph('Cu mgdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["copper"]}'],
                            [Paragraph('Zn mgdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["zinc"]}'],
                            [Paragraph('Mn mgdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["manganese"]}'],
                            [Paragraph('Fe mgdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["iron"]}'],
                            ]
        self.draw_table(data_table_three, 278, 426, [85.78125, 30.672, 25.2, 25.2, 25.2, 25.2, 25.2])
        data_table_four = [
            [Paragraph('PARÂMETROS CALCULADOS', style=self.__standard_paragraph_style_bold), '', 'Classe de Interpretação*'],
            ['Parâmetro', 'Valor', 'MB', 'B', 'M', 'A', 'MA'],
            [Paragraph('Soma de Bases cmolcdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["base_sum"]}'],
            [Paragraph('CTC efetiva (t) cmolcdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["effective_ctc"]}'],
            [Paragraph('CTC Potencial (T) cmolcdm<sup>-3</sup>', style=self.__standard_paragraph_style), f'{sample_values["ctc"]}'],
            [Paragraph('Saturação por bases (V)%', style=self.__standard_paragraph_style), f'{round(sample_values["v_percent"], 2)}'],
            [Paragraph('Saturação por alumínio (m)%', style=self.__standard_paragraph_style), f'{round(sample_values["aluminum_saturation"], 2)}']
        ]
        self.draw_table(data_table_four, 70, 186, [49, 28.448, 25.2, 25.2, 25.2, 25.2, 25.2])
        self.draw_pie_graph_table(278, 300)
        self.draw_granulometric_table(278, 246)
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

    def generate_pdf(self, report_data: sqlite3.Row, path_to_save: str, report_id: int, sample_values: sqlite3.Row) -> None:
        self.__pdf = self.setup_pdf(report_id, path_to_save)
        self.draw_header()
        self.write_main_info_square(report_data, report_id)
        self.draw_footer(40)
        self.draw_tables(sample_values)
        self.draw_signature_space(70, 156, 203.44799999999998)
        self.write_explanation(90)
        self.__pdf.save()


if __name__ == '__main__':
    report = Report('a', 'b')
    report.generate_pdf('b')