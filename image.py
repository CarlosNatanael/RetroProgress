from PIL import Image

# Abrir a imagem original
imagem_original = Image.open("icone.png")

# Redimensionar com antialiasing para preservar qualidade
imagem_redimensionada = imagem_original.resize((256, 256), Image.LANCZOS)

# Salvar a nova imagem
imagem_redimensionada.save("icon.ico")