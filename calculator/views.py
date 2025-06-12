import os
import numpy as np
from django.shortcuts import render
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from django.conf import settings
# Load model once
model = load_model(os.path.join(settings.BASE_DIR, 'brain_tumor_detection_model.h5'))
def predict_image(request):
    prediction = None
    if request.method == 'POST' and request.FILES.get('image'):
        img = request.FILES['image']
        file_path = os.path.join(settings.MEDIA_ROOT, img.name)
        with open(file_path, 'wb+') as destination:
            for chunk in img.chunks():
                destination.write(chunk)
        # Preprocess image
        img_loaded = image.load_img(file_path, target_size=(150, 150))
        img_array = image.img_to_array(img_loaded)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0  # Normalize
        # Predict
        prediction_prob = model.predict(img_array)[0][0]
        prediction = "Tumor Detected" if prediction_prob > 0.5 else "No Tumor Detected"
    return render(request, 'predict.html', {
        'prediction': prediction,
    })
