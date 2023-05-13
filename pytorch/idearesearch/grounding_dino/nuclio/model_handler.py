from PIL import Image
import numpy as np
import torch
from torchvision.ops import box_convert
import groundingdino.datasets.transforms as T
from groundingdino.util.inference import load_model, load_image, predict



class ModelHandler:
    def __init__(self, labels):
        self.model = None
        self.text_promt = " . "
        self.load_network(model_config_path="", model_checkpoint_path="")
        self.labels = labels
        class_name_list = []
        for k, v in labels.items():
            class_name_list.append(v)
        self.text_promt = self.text_promt.join(class_name_list)

    def load_network(self, model_config_path, model_checkpoint_path):
        try:
            self.model = load_model(model_config_path=model_config_path, model_checkpoint_path=model_checkpoint_path,
                                    device="cpu")

            self.is_inititated = True
        except Exception as e:
            raise Exception(f"Cannot load model {model_checkpoint_path}: {e}")

    def preprocess(self, image_source):
        transform = T.Compose(
            [
                T.RandomResize([800], max_size=1333),
                T.ToTensor(),
                T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        )
        image = np.asarray(image_source)
        image_transformed, _ = transform(image_source, None)
        return image, image_transformed

    def infer(self, image, threshold):
        image, image_transformed = self.preprocess(image)

        boxes, logits, phrases = predict(
            model=self.model,
            image=image,
            caption=self.text_promt,
            box_threshold=threshold,
            text_threshold=threshold,
            device="cpu"
        )
        logits = logits.detach().numpy()

        h, w, _ = image.shape
        boxes = boxes * torch.Tensor([w, h, w, h])
        xyxy = box_convert(boxes=boxes, in_fmt="cxcywh", out_fmt="xyxy").numpy()
        phrases = np.asarray(phrases)
        valid = np.where(phrases != '')[0]

        scores = logits[valid]
        boxes = xyxy[valid]
        labels = phrases[valid]

        results = []
        if boxes.shape[0]>0:

            for label, score, box in zip(labels, scores, boxes):
                if label in ["", None]:
                    continue

                if score >= threshold:
                    xtl = max(int(box[0]), 0)
                    ytl = max(int(box[1]), 0)
                    xbr = min(int(box[2]), w)
                    ybr = min(int(box[3]), h)

                    results.append({
                        "confidence": str(score),
                        "label": self.labels.get(label, "unknown"),
                        "points": [xtl, ytl, xbr, ybr],
                        "type": "rectangle",
                    })

        return results