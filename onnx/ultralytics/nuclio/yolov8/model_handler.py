# Copyright (C) 2023 CVAT.ai Corporation
#
# SPDX-License-Identifier: MIT

# Command to Export YoloV8 onnx model:
# yolo model=yolov8m.pt mode=export format=onnx simplify=True

import cv2
import numpy as np
import onnxruntime as ort


def non_max_suppression(boxes, scores, threshold):
    """Returns a list of indexes of objects passing the NMS.
    Args:
      objects: result candidates.
      threshold: the threshold of overlapping IoU to merge the boxes.
    Returns:
      A list of indexes containings the objects that pass the NMS.
    """
    if len(boxes) == 1:
        return [0]

    idxs = np.argsort(scores)


    xmins = boxes[:, 0]
    ymins = boxes[:, 1]
    xmaxs = boxes[:, 2]
    ymaxs = boxes[:, 3]

    areas = (xmaxs - xmins) * (ymaxs - ymins)

    selected_idxs = []
    while idxs.size != 0:
        selected_idx = idxs[-1]
        selected_idxs.append(selected_idx)

        overlapped_xmins = np.maximum(xmins[selected_idx], xmins[idxs[:-1]])
        overlapped_ymins = np.maximum(ymins[selected_idx], ymins[idxs[:-1]])
        overlapped_xmaxs = np.minimum(xmaxs[selected_idx], xmaxs[idxs[:-1]])
        overlapped_ymaxs = np.minimum(ymaxs[selected_idx], ymaxs[idxs[:-1]])

        w = np.maximum(0, overlapped_xmaxs - overlapped_xmins)
        h = np.maximum(0, overlapped_ymaxs - overlapped_ymins)

        intersections = w * h
        unions = areas[idxs[:-1]] + areas[selected_idx] - intersections
        ious = intersections / unions

        idxs = np.delete(
            idxs, np.concatenate(([len(idxs) - 1], np.where(ious > threshold)[0])))

    return selected_idxs


class OnnxDetectors:

    def __init__(self):
        self.model = None
        self.labelmap = None
        self.input_shape = None
        self.input_names = None
        self.output_names = None
        

    def set_labelmap(self, labelmap: dict):
        self.labelmap = labelmap

    def get_input_details(self):
        model_inputs = self.model.get_inputs()
        self.input_names = [model_inputs[i].name for i in range(len(model_inputs))]
        input_image_shape = model_inputs[0].shape
        self.input_shape = (input_image_shape[2], input_image_shape[3])

    def get_output_details(self):
        model_outputs = self.model.get_outputs()
        self.output_names = [model_outputs[i].name for i in range(len(model_outputs))]

    def _get_scaled_coords(self, xyxy, output_image, pad):
        """
        Converts raw prediction bounding box to orginal
        image coordinates.

        Args:
          xyxy: array of boxes
          output_image: np array
          pad: padding due to image resizing (pad_w, pad_h)
        """
        pad_w, pad_h = pad
        in_h, in_w = self.input_shape
        out_h, out_w, _ = output_image.shape

        ratio_w = out_w / (in_w - pad_w)
        ratio_h = out_h / (in_h - pad_h)

        xyxy[:, 0] *= ratio_w
        xyxy[:, 1] *= ratio_h
        xyxy[:, 2] *= ratio_w
        xyxy[:, 3] *= ratio_h

        xyxy[:, 0] = np.clip(xyxy[:, 0], 0, out_w)
        xyxy[:, 1] = np.clip(xyxy[:, 1], 0, out_h)
        xyxy[:, 2] = np.clip(xyxy[:, 2], 0, out_w)
        xyxy[:, 3] = np.clip(xyxy[:, 3], 0, out_h)

        return xyxy.astype(int)

    def _process_predictions(self, boxes, output_image, pad):
        """
        Process predictions and optionally output an image with annotations
        """
        if len(boxes):
            boxes = self._get_scaled_coords(boxes, output_image, pad)
        return boxes

    @staticmethod
    def _resize_and_pad(image, desired_size):
        old_size = image.shape[:2]
        ratio = float(desired_size / max(old_size))
        new_size = tuple([int(x * ratio) for x in old_size])
        delta_w = desired_size - new_size[1]
        delta_h = desired_size - new_size[0]

        # new_size should be in (width, height) format
        image = cv2.resize(image, (new_size[1], new_size[0]))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pad = (delta_w, delta_h)

        color = [100, 100, 100]
        new_im = cv2.copyMakeBorder(image, 0, delta_h, 0, delta_w, cv2.BORDER_CONSTANT,
                                    value=color)
        return new_im, pad

    def _get_image_tensor(self, img):
        """
        Reshapes an input image into a square with sides max_size
        """
        new_im, pad = self._resize_and_pad(img, self.input_shape[0])
        new_im = np.asarray(new_im, dtype=np.float32)
        return img, new_im, pad


class ModelHandler(OnnxDetectors):

    def __init__(self, labels, conf_thresh=0.4, iou_thresh=0.5, max_det=300):
        super().__init__()
        self.conf_thresh = conf_thresh
        self.iou_thresh = iou_thresh
        self.max_det = max_det
        self.labels = labels
        self.is_inititated = False
        self.load_network(model_path="yolov8m.onnx")

    def load_network(self, model_path: str):
        self.model = ort.InferenceSession(model_path)
        self.get_input_details()
        self.get_output_details()
        self.is_inititated = True
        
        
    def xywh2xyxy(self, x):
        # Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
        y = np.copy(x)
        y[:, 0] = x[:, 0] - x[:, 2] / 2  # top left x
        y[:, 1] = x[:, 1] - x[:, 3] / 2  # top left y
        y[:, 2] = x[:, 0] + x[:, 2] / 2  # bottom right x
        y[:, 3] = x[:, 1] + x[:, 3] / 2  # bottom right y
        return y

    def _infer(self, img: np.ndarray):

        full_image, net_image, pad = self._get_image_tensor(img)
        net_image = net_image.transpose((2, 0, 1))

        net_image /= 255
        net_image = np.expand_dims(net_image, 0)
        output = self.model.run(self.output_names, {self.model.get_inputs()[0].name: net_image})[0]

        output = np.asarray(output)
        predictions = np.squeeze(output[0]).T

        scores = np.max(predictions[:, 4:], axis=1)
        predictions = predictions[scores > 0.1, :]
        scores = scores[scores > 0.1]
        class_ids = np.argmax(predictions[:, 4:], axis=1)
        boxes = predictions[:, :4]

        boxes = self.xywh2xyxy(boxes)
        boxes = self._process_predictions(boxes, full_image, pad)

        valid = non_max_suppression(boxes, scores, self.iou_thresh)  # NMS

        boxes = boxes[valid]
        class_ids = class_ids[valid]
        confidences = scores[valid]
   
        return boxes, class_ids, confidences
        
    def infer(self, image, threshold):
        image = np.array(image)
        image = image[:, :, ::-1].copy()
        h, w, _ = image.shape
        boxes, labels, scores = self._infer(image)

        results = []

        for label, score, box in zip(labels, scores, boxes):
            label = int(label)
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
