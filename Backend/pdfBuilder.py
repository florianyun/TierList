from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import requests
import os
from models import Element
from typing import List

def build_pdf(elements : List[Element], pdf_filename):
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    story = []
    styles = getSampleStyleSheet()

    for element in elements:
        story.append(Paragraph(element.titre, styles['Title']))
        story.append(Paragraph(element.groupe, styles['Normal']))
        if element.source:
            response = requests.get(element.source)
            if response.status_code == 200:
                # Sauvegardez l'image téléchargée temporairement
                with open("temp_image.png", "wb") as img_file:
                    img_file.write(response.content)
                story.append(Spacer(1, 12))  # Espace entre le texte et l'image
                story.append(Image("temp_image.png", width=200, height=200))
            else:
                # Gérez le cas où le téléchargement de l'image a échoué
                story.append(Paragraph("Image indisponible", styles['Normal']))

    doc.build(story)
    os.remove("temp_image.png")