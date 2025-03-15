# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class imageForm(FlaskForm):
    text = StringField(
        'Texto para a imagem', 
        validators=[DataRequired()],
        render_kw={"placeholder": "Digite aqui o texto para gerar a imagem"}
    )

