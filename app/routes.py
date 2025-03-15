# routes.py
from flask import Flask, render_template, request, Blueprint
from diffusers import StableDiffusionPipeline
from .forms import imageForm  # Importar o formulário
import torch
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/generated_images/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Carregue o modelo
device = "cuda" if torch.cuda.is_available() else "cpu"
model_id = "CompVis/stable-diffusion-v1-4"
if device == "cpu":
    print("Aviso: CUDA não detectado. O desempenho será lento.")
pipe = StableDiffusionPipeline.from_pretrained(model_id, low_cpu_mem_usage=True).to(device)


main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
def generate_image():
    form = imageForm()
    if request.method == 'POST' and form.validate_on_submit():
        
        text = form.text.data.strip()
        
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{text.replace(' ', '_')}.png")
        try:
            # Geração de imagem
            image = pipe(text).images[0]
        except MemoryError:
                        return "Erro: Falta de memória. Tente usar um prompt menor ou reinicie o sistema."

        image.save(image_path)

        return render_template("result.html", image_url=image_path)
    
    return render_template("index.html", form=form)