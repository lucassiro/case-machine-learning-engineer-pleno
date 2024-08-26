from pickle import load


def load_model():
    try:
        with open("src/models/model.pkl", "rb") as f:
            model = load(f)

            return model
    except Exception:
        return None
