from ultralytics import YOLO

def load_model(model_path):
    model = YOLO(model_path)
    return model


def infer(model, image_path):
    results = model.predict(source=image_path, save=True)
    return results


def process_results(results):
    detected_objects = results[0].boxes
    if detected_objects is None:
        return 0, []

    num_objects = len(detected_objects)

    confidences = detected_objects.conf.tolist()  # 정확도 리스트

    return num_objects, confidences


def detect_phone_yolo(image_data):
    model_path = "best.pt"
    model = load_model(model_path)

    predictions = infer(model, image_data)

    return process_results(predictions)