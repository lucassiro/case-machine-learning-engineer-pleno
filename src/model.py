from pickle import dump, load

model_path = "src/models/model.pkl"

def load_model():
    try:
        with open(model_path, "rb") as f:
            model = load(f)

            return model
    except Exception:
        return None


def save_model(model):
    with open(model_path, "wb") as f:
        dump(model, f)
