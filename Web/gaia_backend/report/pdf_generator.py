"""
Gerador de PDF de laudos para o sistema web
Versão standalone sem dependências de PySide6
"""
import os
import sys
import json
from io import BytesIO
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Table, TableStyle, Paragraph, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor
import matplotlib
matplotlib.use('Agg')  # Backend sem GUI
import matplotlib.pyplot as plt
import math


class WebReportGenerator:
    """Gerador de PDFs standalone para o sistema web"""
    
    @staticmethod
    def generate_pdf_for_sample(sample_id, agreement="Sistema Web"):
        """
        Gera PDF para uma amostra específica usando apenas reportlab
        
        Args:
            sample_id: ID da amostra
            agreement: Texto do convênio
            
        Returns:
            BytesIO com o conteúdo do PDF ou None se falhar
        """
        from .models import Amostra
        
        try:
            # Buscar amostra
            amostra = Amostra.objects.select_related(
                'propriedade',
                'propriedade__endereco',
                'propriedade__proprietario_pessoa',
                'propriedade__proprietario_empresa'
            ).get(id=sample_id)
            
            propriedade = amostra.propriedade
            endereco = propriedade.endereco if propriedade.endereco else None
            
            # Buffer para o PDF
            buffer = BytesIO()
            pdf = canvas.Canvas(buffer)
            pdf.setTitle(f'Laudo Amostra {amostra.numero_amostra}')
            
            # Desenhar conteúdo básico (versão simplificada)
            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawCentredString(300, 800, "LAUDO DE ANÁLISE DE SOLO")
            
            pdf.setFont("Helvetica", 10)
            y = 750
            
            # Informações do solicitante
            if propriedade.proprietario_pessoa:
                pdf.drawString(50, y, f"Solicitante: {propriedade.proprietario_pessoa.name}")
                y -= 15
                pdf.drawString(50, y, f"CPF: {propriedade.proprietario_pessoa.cpf}")
            elif propriedade.proprietario_empresa:
                pdf.drawString(50, y, f"Solicitante: {propriedade.proprietario_empresa.name}")
                y -= 15
                pdf.drawString(50, y, f"CNPJ: {propriedade.proprietario_empresa.cnpj}")
            
            y -= 20
            pdf.drawString(50, y, f"Propriedade: {propriedade.name}")
            y -= 15
            
            if endereco:
                pdf.drawString(50, y, f"Município: {endereco.cidade} - {endereco.estado}")
                y -= 15
            
            pdf.drawString(50, y, f"Matrícula: {propriedade.registration_number}")
            y -= 15
            pdf.drawString(50, y, f"Convênio: {agreement}")
            y -= 15
            pdf.drawString(50, y, f"Amostra: {amostra.numero_amostra}")
            y -= 15
            pdf.drawString(50, y, f"Data: {amostra.data_coleta}")
            
            y -= 30
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(50, y, "RESULTADOS DA ANÁLISE")
            y -= 20
            
            pdf.setFont("Helvetica", 10)
            resultados = [
                ("pH", amostra.ph),
                ("Fósforo (P)", amostra.fosforo),
                ("Potássio (K)", amostra.potassio),
                ("Matéria Orgânica", amostra.materia_organica),
                ("Cálcio (Ca)", amostra.calcio),
                ("Magnésio (Mg)", amostra.magnesio),
                ("Alumínio (Al)", amostra.aluminio),
                ("Argila", amostra.argila),
                ("Silte", amostra.silte),
                ("Areia", amostra.areia),
            ]
            
            for nome, valor in resultados:
                if valor is not None:
                    pdf.drawString(50, y, f"{nome}: {valor}")
                    y -= 15
                    if y < 100:
                        pdf.showPage()
                        y = 800
            
            pdf.save()
            buffer.seek(0)
            return buffer
            
        except Exception as e:
            print(f"Erro ao gerar PDF: {e}")
            import traceback
            traceback.print_exc()
            return None
