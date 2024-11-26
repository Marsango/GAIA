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
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),  # Navigate up to GAIA
        "interface",
        "images"
        ).replace("\\", "/")
        self.__file_location: str = file_location
        self.__technician: str = technician
        self.horizontal_size: int = 595
        self.vertical_size: int = 842
        self.pdf: canvas.Canvas = self.setup_pdf()

    def add_fonts(self) -> None:
        pdfmetrics.registerFont(TTFont('arial', 'fonts/arial.ttf'))
        pdfmetrics.registerFont(TTFont('arialbd', 'fonts/arialbd.ttf'))
        pdfmetrics.registerFont(TTFont('arialbi', 'fonts/arialbi.ttf'))
        pdfmetrics.registerFont(TTFont('ariali', 'fonts/ariali.ttf'))
        pdfmetrics.registerFont(TTFont('arilbk', 'fonts/ariblk.ttf'))

    def setup_pdf(self) -> canvas.Canvas:
        self.add_fonts()
        pdf: canvas.Canvas = canvas.Canvas(f'Laudo.pdf')
        pdf.setTitle(f'Laudo - 001')
        return pdf

    def draw_header(self) -> None:
        self.pdf.setStrokeColor('yellow')
        self.pdf.line(30, 745, 560, 745)
        self.pdf.setStrokeColor('black')
        self.pdf.line(30, 750, 560, 750)
        self.pdf.setFont('arialbd', 14)
        self.pdf.drawCentredString(self.horizontal_size / 2, 725, 'Laudo de Análise de Solo')
        self.pdf.drawImage(f'{self.__images_location}/UTFPR_logo.svg.png', 65, 725, 100, 100, preserveAspectRatio=True, mask='auto')
        self.pdf.setFont('arialbd', 10)
        self.pdf.drawCentredString(self.horizontal_size / 2, 785, 'LABSOLOS - Laboratório de Solos da UTFPR')
        self.pdf.setFont('arial', 10)
        self.pdf.drawCentredString(self.horizontal_size / 2, 772, 'Universidade Tecnólogica Federal do Paraná')
        self.pdf.drawCentredString(self.horizontal_size / 2, 759, 'Campus Pato Branco')
        self.pdf.drawImage(f'{self.__images_location}/logo_lab-no-bg.png', 410, 730, 125, 125, preserveAspectRatio=True, mask='auto')
        self.pdf.setFont('arial', 8)

    def draw_square(self, pos_horizontal1: int, pos_horizontal2: int, pos_vertical1: int,
                    pos_vertical2: int) -> None:
        self.pdf.line(pos_horizontal1, pos_vertical1, pos_horizontal2, pos_vertical1)
        self.pdf.line(pos_horizontal1, pos_vertical1, pos_horizontal1, pos_vertical2)
        self.pdf.line(pos_horizontal1, pos_vertical2, pos_horizontal2, pos_vertical2)
        self.pdf.line(pos_horizontal2, pos_vertical1, pos_horizontal2, pos_vertical2)

    def write_main_info_square(self) -> None:
        self.draw_square(70, 520, 720, 665)
        self.pdf.setFont('arial', 10)
        self.pdf.drawString(75, 710, f"Solicitante: Fulano")
        self.pdf.drawString(75, 700, f"Endereço: Av. das flores 224")
        self.pdf.drawString(75, 690, f"Propriedade: Fazenda São Francisco")
        self.pdf.drawString(75, 680, f"Talhão: 001")
        self.pdf.drawString(75, 670, f"Técnico: Gustavo")
        self.pdf.drawString(400, 710, f"Laudo: 001")
        self.pdf.drawString(400, 700, f"Amostra: 001")
        self.pdf.drawString(400, 690, f"Data: 11/11/2024")
        self.pdf.drawString(400, 680, f"Profundidade: 20 cm")
        self.pdf.drawString(400, 670, f"Nº Matrícula: 102")

    def draw_footer(self):
        self.draw_square(70, 520, 55, 20)
        self.pdf.setFont('arial', 8)
        self.pdf.drawCentredString(self.horizontal_size / 2, 45,
                              f"Laboratório de Análise de Solo  - UTFPR")
        self.pdf.drawCentredString(self.horizontal_size / 2, 35,
                              f"Via do conhecimento, KM 01, caixa postal 57, CEP 85503-390, Pato Branco - PR")
        self.pdf.drawCentredString(self.horizontal_size / 2, 25,
                              f"Telefone/WhatsApp: (46) 3220-2539, E-mail: labsolos-pb@utfpr.edu.br")

    def draw_ruler(self):
        self.pdf.drawString(100, 810, 'x100')
        self.pdf.drawString(200, 810, 'x200')
        self.pdf.drawString(300, 810, 'x300')
        self.pdf.drawString(400, 810, 'x400')
        self.pdf.drawString(500, 810, 'x500')
        self.pdf.drawString(10, 100, 'y100')
        self.pdf.drawString(10, 200, 'y200')
        self.pdf.drawString(10, 300, 'y300')
        self.pdf.drawString(10, 400, 'y400')
        self.pdf.drawString(10, 500, 'y500')
        self.pdf.drawString(10, 600, 'y600')
        self.pdf.drawString(10, 700, 'y700')
        self.pdf.drawString(10, 800, 'y800')

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
        table.wrapOn(self.pdf, 0, 0)
        table.drawOn(self.pdf, coord_x, coord_y)
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
        table.wrapOn(self.pdf, 0, 0)
        table.drawOn(self.pdf, coord_x, coord_y)
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
        table.wrapOn(self.pdf, 0, 0)
        table.drawOn(self.pdf, coord_x, coord_y)
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
        table.wrapOn(self.pdf, 0, 0)
        table.drawOn(self.pdf, coord_x, coord_y)
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
        table.wrapOn(self.pdf, 0, 0)
        table.drawOn(self.pdf, coord_x, coord_y)
        w, h = table.wrap(0, 0)
        print(f'col: {w}, row:{h}')

    def generate_pdf(self) -> None:
        self.draw_header()
        self.write_main_info_square()
        self.draw_footer()
        standard_paragraph_style = ParagraphStyle(
            name='Normal',
            fontName='arial',
            fontSize=8,
            alignment=TA_CENTER
        )
        standard_paragraph_style_bold = ParagraphStyle(
            name='Normal',
            fontName='arialbd',
            fontSize=8,
            alignment=TA_CENTER
        )
        data_table_one = [['BÁSICA', '', 'Classe de Interpretação*'],
                          ['Elemento', 'Teor', 'MB', 'B', 'M', 'A', 'MA'],
                          [Paragraph('Ca<sup>2+</sup> cmolcdm<sup>-3</sup>', style=standard_paragraph_style), '4.2'],
                          [Paragraph('Mg² cmolcdm<sup>-3</sup>', style=standard_paragraph_style), '1.3'],
                          [Paragraph('K cmolcdm<sup>-3</sup>³', style=standard_paragraph_style), '0.25'],
                          [Paragraph('MO gdm<sup>-3</sup>', style=standard_paragraph_style), '50.9'],
                          [Paragraph('P mgdm<sup>-3</sup>', style=standard_paragraph_style), '9.2']]
        self.draw_table(data_table_one, 70, 480, [49, 28.448, 25.2, 25.2, 25.2, 25.2, 25.2])
        data_table_two = [['REAÇÃO DO SOLO', '', 'Classe de Interpretação*'],
                          ['Parâmetro', 'Valor', 'MB', 'B', 'M', 'A', 'MA'],
                          [Paragraph('pH-CaCl2', style=standard_paragraph_style), '4.4'],
                          [Paragraph('Al<sup>3+</sup> cmolcdm<sup>-3</sup>', style=standard_paragraph_style), '0.56'],
                          [Paragraph('H+Al cmolcdm<sup>-3</sup>', style=standard_paragraph_style), '12.1'],
                          [Paragraph('Índice SMP', style=standard_paragraph_style), '5.0'], ]
        self.draw_table(data_table_two, 278, 534, None)
        data_table_three = [['MICRONUTRIENTES', '', 'Classe de Interpretação*'],
                            ['Elemento', 'Teor', 'MB', 'B', 'M', 'A', 'MA'],
                            [Paragraph('Cu mgdm<sup>-3</sup>', style=standard_paragraph_style), '7.6'],
                            [Paragraph('Zn mgdm<sup>-3</sup>', style=standard_paragraph_style), '68.7'],
                            [Paragraph('Mn mgdm<sup>-3</sup>', style=standard_paragraph_style), '72.0'],
                            [Paragraph('Fe mgdm<sup>-3</sup>', style=standard_paragraph_style), '68.7'],
                            ]
        self.draw_table(data_table_three, 278, 426, [85.78125, 30.672, 25.2, 25.2, 25.2, 25.2, 25.2])
        data_table_four = [
            [Paragraph('PARÂMETROS CALCULADOS', style=standard_paragraph_style_bold), '', 'Classe de Interpretação*'],
            ['Parâmetro', 'Valor', 'MB', 'B', 'M', 'A', 'MA'],
            [Paragraph('Soma de Bases cmolcdm<sup>-3</sup>', style=standard_paragraph_style), '5.75'],
            [Paragraph('CTC efetiva (t) cmolcdm<sup>-3</sup>', style=standard_paragraph_style), '6.31'],
            [Paragraph('CTC Potencial (T) cmolcdm<sup>-3</sup>', style=standard_paragraph_style), '17.85'],
            [Paragraph('Saturação por bases (V)%', style=standard_paragraph_style), '32.2'],
            [Paragraph('Saturação por alumínio (m)%', style=standard_paragraph_style), '8.9']
        ]
        self.draw_table(data_table_four, 70, 186, [49, 28.448, 25.2, 25.2, 25.2, 25.2, 25.2])
        self.draw_pie_graph_table(278, 300)
        self.draw_granulometric_table(278, 246)
        self.draw_extractor_graph(278, 156)
        self.pdf.line(278, 103, 278 + 242.45324999999994, 103)
        self.pdf.drawImage(f'{self.__images_location}/ctc_and_values.png', 278 + 65, 305, 108, 108, preserveAspectRatio=True, mask='auto')
        self.pdf.setFont('arialbd', 10)
        self.pdf.drawCentredString(399.22662499999997, 90, 'Assinatura')
        self.pdf.setFont('arial', 7)
        self.draw_explanation_table( 70, 66)
        # pdf.drawString(70, 190,
        #                       '* Baseado no Manual de Adubação e calagem para o')
        # pdf.drawString(73, 180, ' estado do Paraná (NEPAR-BCS, 2019)')
        # pdf.drawString(70, 170, '** De acordo com o Programa Nacional de Zoneamento')
        # pdf.drawString(73, 160, ' Agrícola de Risco Climático (ZARC), regido pela Instrução')
        # pdf.drawString(73, 150, ' Normativa – IN SPA/MAPA nº 01, de 21 de junho')
        # pdf.drawString(73, 140, ' de 2022, da Secretaria de Política Agrícola do MAPA.')
        self.pdf.save()


if __name__ == '__main__':
    report = Report('a', 'b')
    report.generate_pdf()