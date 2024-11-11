from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    """ Rendre un template HTML en PDF et renvoyer une réponse HTTP avec le PDF """
    # Récupérer le template
    template = get_template(template_src)
    
    # Rendre le template avec le contexte
    html = template.render(context_dict)
    
    # Créer un flux mémoire pour stocker le fichier PDF
    result = BytesIO()
    
    # Convertir le HTML en PDF
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    # Si l'opération a réussi, renvoyer le PDF généré
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    
    # En cas d'erreur, retourner None
    return None
