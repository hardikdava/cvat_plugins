# cvat_plugins
This reposity contains some serverless functionality for semi-auto annotations.



## Start Container:

Execute one of the following command from cvat root directory

**Deploy CPU container:**
```bash
./serverless/deploy_cpu.sh serverless/pytorch/ultralytics/yolov5
```

**Deploy GPU container:**
```bash
./serverless/deploy_gpu.sh serverless/pytorch/ultralytics/yolov5
```

## Getting Logs of Container:

**Method-1**

Find docker id from
```
docker container ls
```
Getting the logs 
```
docker container logs {docker-id}
docker container rm {docker-id} -f # For realtime logs
```

**Method-2**

Find docker name from `function.yaml` or `function-gpu.yaml`

Getting the logs 
```
docker container logs {docker-name}
docker container rm {docker-name} -f # For realtime logs
```


## Stop Container:


**Method-1**

Find docker id from
```
docker container ls
```
Stop and remove container
```
docker container stop {docker-id}
docker container rm {docker-id}
```

**Method-2**

Find docker name from `function.yaml` or `function-gpu.yaml`

Stop and remove container
```
docker container stop {docker-name}
docker container rm {docker-name}
```



## Types of Annotation Format:

**Detector :**

| name | Data-Type | Format |
|--|--|--|
|confidence  |string  |between 0-1|
|label  |string|labels.get(class_id, "unknown")|
|type  |string  |Fixed value=rectangle|
|points  |list|[x1, y1, x2, y2]|



**Segmentation :**
| name | Data-Type | Format |
|--|--|--|
|confidence  |string  |between 0-1|
|label  |string|labels.get(class_id, "unknown")|
|type  |string  |Fixed value=mask|
|points  |list|a list of points representing a single polygon (x1, y1, x2, y2, x3, y3, ..., xn, yn), |
|mask | list | a list of 0 and 1 representing a binary mask cropped around the object, with the last four elements representing the top left and bottom right coordinates of the object's bounding box, (x_top_left, y_top_left, x_bottom_right, y_bottom_right) |

<!---

**Pose Estimation :**


cvat label raw:


```
[
  {
    "name": "human-pose",
    "id": 22,
    "color": "#47390e",
    "type": "skeleton",
    "sublabels": [
      {
        "name": "0",
        "attributes": [],
        "type": "points",
        "color": "#7d050a",
        "id": 23
      },
      {
        "name": "1",
        "attributes": [],
        "type": "points",
        "color": "#d12345",
        "id": 24
      },
      {
        "name": "2",
        "attributes": [],
        "type": "points",
        "color": "#350dea",
        "id": 25
      },
      {
        "name": "3",
        "attributes": [],
        "type": "points",
        "color": "#479ffe",
        "id": 26
      },
      {
        "name": "4",
        "attributes": [],
        "type": "points",
        "color": "#4a649f",
        "id": 27
      },
      {
        "name": "5",
        "attributes": [],
        "type": "points",
        "color": "#478144",
        "id": 28
      },
      {
        "name": "6",
        "attributes": [],
        "type": "points",
        "color": "#57236b",
        "id": 29
      },
      {
        "name": "7",
        "attributes": [],
        "type": "points",
        "color": "#1cdda5",
        "id": 30
      },
      {
        "name": "8",
        "attributes": [],
        "type": "points",
        "color": "#e2bc6e",
        "id": 31
      },
      {
        "name": "9",
        "attributes": [],
        "type": "points",
        "color": "#f067db",
        "id": 32
      },
      {
        "name": "10",
        "attributes": [],
        "type": "points",
        "color": "#63bbfa",
        "id": 33
      },
      {
        "name": "11",
        "attributes": [],
        "type": "points",
        "color": "#22b16f",
        "id": 34
      },
      {
        "name": "12",
        "attributes": [],
        "type": "points",
        "color": "#daddec",
        "id": 35
      },
      {
        "name": "13",
        "attributes": [],
        "type": "points",
        "color": "#2ac791",
        "id": 36
      },
      {
        "name": "14",
        "attributes": [],
        "type": "points",
        "color": "#de22a0",
        "id": 37
      },
      {
        "name": "15",
        "attributes": [],
        "type": "points",
        "color": "#a7a570",
        "id": 38
      },
      {
        "name": "16",
        "attributes": [],
        "type": "points",
        "color": "#74db1b",
        "id": 39
      }
    ],
    "svg": "<line x1=&quot;65.844482421875&quot; y1=&quot;64.453125&quot; x2=&quot;59.82441329956055&quot; y2=&quot;83.85111999511719&quot; stroke=&quot;black&quot; data-type=&quot;edge&quot; data-node-from=&quot;15&quot; stroke-width=&quot;0.5&quot; data-node-to=&quot;17&quot;></line><line x1=&quot;27.21571922302246&quot; y1=&quot;64.95479583740234&quot; x2=&quot;30.72742462158203&quot; y2=&quot;85.02169036865234&quot; stroke=&quot;black&quot; data-type=&quot;edge&quot; data-node-from=&quot;14&quot; stroke-width=&quot;0.5&quot; data-node-to=&quot;16&quot;></line><line x1=&quot;28.386287689208984&quot; y1=&quot;48.23238754272461&quot; x2=&quot;67.34949493408203&quot; y2=&quot;48.06516647338867&quot; stroke=&quot;black&quot; data-type=&quot;edge&quot; data-node-from=&quot;12&quot; stroke-width=&quot;0.5&quot; data-node-to=&quot;13&quot;></line><line x1=&quot;27.21571922302246&quot; y1=&quot;23.98489761352539&quot; x2=&quot;71.02842712402344&quot; y2=&quot;23.316001892089844&quot; stroke=&quot;black&quot; data-type=&quot;edge&quot; data-node-from=&quot;6&quot; stroke-width=&quot;0.5&quot; data-node-to=&quot;7&quot;></line><line x1=&quot;71.02842712402344&quot; y1=&quot;23.316001892089844&quot; x2=&quot;67.34949493408203&quot; y2=&quot;48.06516647338867&quot; stroke=&quot;black&quot; data-type=&quot;edge&quot; data-node-from=&quot;7&quot; stroke-width=&quot;0.5&quot; data-node-to=&quot;13&quot;></line><line x1=&quot;28.386287689208984&quot; y1=&quot;48.23238754272461&quot; x2=&quot;27.21571922302246&quot; y2=&quot;64.95479583740234&quot; stroke=&quot;black&quot; data-type=&quot;edge&quot; data-node-from=&quot;12&quot; stroke-width=&quot;0.5&quot; data-node-to=&quot;14&quot;></line><line x1=&quot;27.21571922302246&quot; y1=&quot;23.98489761352539&quot; x2=&quot;28.386287689208984&quot; y2=&quot;48.23238754272461&quot; stroke=&quot;black&quot; data-type=&quot;edge&quot; data-node-from=&quot;6&quot; stroke-width=&quot;0.5&quot; data-node-to=&quot;12&quot;></line><line x1=&quot;67.34949493408203&quot; y1=&quot;48.06516647338867&quot; x2=&quot;65.844482421875&quot; y2=&quot;64.453125&quot; stroke=&quot;black&quot; data-type=&quot;edge&quot; data-node-from=&quot;13&quot; stroke-width=&quot;0.5&quot; data-node-to=&quot;15&quot;></line><line x1=&quot;62.834449768066406&quot; y1=&quot;36.526702880859375&quot; x2=&quot;54.64046859741211&quot; y2=&quot;38.86783981323242&quot; stroke=&quot;black&quot; data-type=&quot;edge&quot; data-node-from=&quot;9&quot; stroke-width=&quot;0.5&quot; data-node-to=&quot;11&quot;></line><line x1=&quot;71.02842712402344&quot; y1=&quot;23.316001892089844&quot; x2=&quot;62.834449768066406&quot; y2=&quot;36.526702880859375&quot; stroke=&quot;black&quot; data-type=&quot;edge&quot; data-node-from=&quot;7&quot; stroke-width=&quot;0.5&quot; data-node-to=&quot;9&quot;></line><line x1=&quot;61.998329162597656&quot; y1=&quot;12.446435928344727&quot; x2=&quot;71.02842712402344&quot; y2=&quot;23.316001892089844&quot; stroke=&quot;black&quot; data-type=&quot;edge&quot; data-node-from=&quot;5&quot; stroke-width=&quot;0.5&quot; data-node-to=&quot;7&quot;></line><line x1=&quot;35.74414825439453&quot; y1=&quot;37.362823486328125&quot; x2=&quot;46.27926254272461&quot; y2=&quot;39.36951446533203&quot; stroke=&quot;black&quot; data-type=&quot;edge&quot; data-node-from=&quot;8&quot; stroke-width=&quot;0.5&quot; data-node-to=&quot;10&quot;></line><line x1=&quot;27.21571922302246&quot; y1=&quot;23.98489761352539&quot; x2=&quot;35.74414825439453&quot; y2=&quot;37.362823486328125&quot; stroke=&quot;black&quot; data-type=&quot;edge&quot; data-node-from=&quot;6&quot; stroke-width=&quot;0.5&quot; data-node-to=&quot;8&quot;></line><line x1=&quot;34.239131927490234&quot; y1=&quot;11.777539253234863&quot; x2=&quot;27.21571922302246&quot; y2=&quot;23.98489761352539&quot; stroke=&quot;black&quot; data-type=&quot;edge&quot; data-node-from=&quot;4&quot; stroke-width=&quot;0.5&quot; data-node-to=&quot;6&quot;></line><line x1=&quot;42.934783935546875&quot; y1=&quot;10.272522926330566&quot; x2=&quot;34.239131927490234&quot; y2=&quot;11.777539253234863&quot; stroke=&quot;black&quot; data-type=&quot;edge&quot; data-node-from=&quot;2&quot; stroke-width=&quot;0.5&quot; data-node-to=&quot;4&quot;></line><line x1=&quot;55.14213943481445&quot; y1=&quot;9.436402320861816&quot; x2=&quot;61.998329162597656&quot; y2=&quot;12.446435928344727&quot; stroke=&quot;black&quot; data-type=&quot;edge&quot; data-node-from=&quot;3&quot; stroke-width=&quot;0.5&quot; data-node-to=&quot;5&quot;></line><line x1=&quot;55.14213943481445&quot; y1=&quot;9.436402320861816&quot; x2=&quot;42.934783935546875&quot; y2=&quot;10.272522926330566&quot; stroke=&quot;black&quot; data-type=&quot;edge&quot; data-node-from=&quot;3&quot; stroke-width=&quot;0.5&quot; data-node-to=&quot;2&quot;></line><line x1=&quot;48.11872863769531&quot; y1=&quot;14.118677139282227&quot; x2=&quot;55.14213943481445&quot; y2=&quot;9.436402320861816&quot; stroke=&quot;black&quot; data-type=&quot;edge&quot; data-node-from=&quot;1&quot; stroke-width=&quot;0.5&quot; data-node-to=&quot;3&quot;></line><line x1=&quot;48.11872863769531&quot; y1=&quot;14.118677139282227&quot; x2=&quot;42.934783935546875&quot; y2=&quot;10.272522926330566&quot; stroke=&quot;black&quot; data-type=&quot;edge&quot; data-node-from=&quot;1&quot; stroke-width=&quot;0.5&quot; data-node-to=&quot;2&quot;></line><circle r=&quot;1.5&quot; stroke=&quot;black&quot; fill=&quot;#b3b3b3&quot; cx=&quot;48.11872863769531&quot; cy=&quot;14.118677139282227&quot; stroke-width=&quot;0.1&quot; data-type=&quot;element node&quot; data-element-id=&quot;1&quot; data-node-id=&quot;1&quot; data-label-id=&quot;23&quot;></circle><circle r=&quot;1.5&quot; stroke=&quot;black&quot; fill=&quot;#b3b3b3&quot; cx=&quot;42.934783935546875&quot; cy=&quot;10.272522926330566&quot; stroke-width=&quot;0.1&quot; data-type=&quot;element node&quot; data-element-id=&quot;2&quot; data-node-id=&quot;2&quot; data-label-id=&quot;24&quot;></circle><circle r=&quot;1.5&quot; stroke=&quot;black&quot; fill=&quot;#b3b3b3&quot; cx=&quot;55.14213943481445&quot; cy=&quot;9.436402320861816&quot; stroke-width=&quot;0.1&quot; data-type=&quot;element node&quot; data-element-id=&quot;3&quot; data-node-id=&quot;3&quot; data-label-id=&quot;25&quot;></circle><circle r=&quot;1.5&quot; stroke=&quot;black&quot; fill=&quot;#b3b3b3&quot; cx=&quot;34.239131927490234&quot; cy=&quot;11.777539253234863&quot; stroke-width=&quot;0.1&quot; data-type=&quot;element node&quot; data-element-id=&quot;4&quot; data-node-id=&quot;4&quot; data-label-id=&quot;26&quot;></circle><circle r=&quot;1.5&quot; stroke=&quot;black&quot; fill=&quot;#b3b3b3&quot; cx=&quot;61.998329162597656&quot; cy=&quot;12.446435928344727&quot; stroke-width=&quot;0.1&quot; data-type=&quot;element node&quot; data-element-id=&quot;5&quot; data-node-id=&quot;5&quot; data-label-id=&quot;27&quot;></circle><circle r=&quot;1.5&quot; stroke=&quot;black&quot; fill=&quot;#b3b3b3&quot; cx=&quot;27.21571922302246&quot; cy=&quot;23.98489761352539&quot; stroke-width=&quot;0.1&quot; data-type=&quot;element node&quot; data-element-id=&quot;6&quot; data-node-id=&quot;6&quot; data-label-id=&quot;28&quot;></circle><circle r=&quot;1.5&quot; stroke=&quot;black&quot; fill=&quot;#b3b3b3&quot; cx=&quot;71.02842712402344&quot; cy=&quot;23.316001892089844&quot; stroke-width=&quot;0.1&quot; data-type=&quot;element node&quot; data-element-id=&quot;7&quot; data-node-id=&quot;7&quot; data-label-id=&quot;29&quot;></circle><circle r=&quot;1.5&quot; stroke=&quot;black&quot; fill=&quot;#b3b3b3&quot; cx=&quot;35.74414825439453&quot; cy=&quot;37.362823486328125&quot; stroke-width=&quot;0.1&quot; data-type=&quot;element node&quot; data-element-id=&quot;8&quot; data-node-id=&quot;8&quot; data-label-id=&quot;30&quot;></circle><circle r=&quot;1.5&quot; stroke=&quot;black&quot; fill=&quot;#b3b3b3&quot; cx=&quot;62.834449768066406&quot; cy=&quot;36.526702880859375&quot; stroke-width=&quot;0.1&quot; data-type=&quot;element node&quot; data-element-id=&quot;9&quot; data-node-id=&quot;9&quot; data-label-id=&quot;31&quot;></circle><circle r=&quot;1.5&quot; stroke=&quot;black&quot; fill=&quot;#b3b3b3&quot; cx=&quot;46.27926254272461&quot; cy=&quot;39.36951446533203&quot; stroke-width=&quot;0.1&quot; data-type=&quot;element node&quot; data-element-id=&quot;10&quot; data-node-id=&quot;10&quot; data-label-id=&quot;32&quot;></circle><circle r=&quot;1.5&quot; stroke=&quot;black&quot; fill=&quot;#b3b3b3&quot; cx=&quot;54.64046859741211&quot; cy=&quot;38.86783981323242&quot; stroke-width=&quot;0.1&quot; data-type=&quot;element node&quot; data-element-id=&quot;11&quot; data-node-id=&quot;11&quot; data-label-id=&quot;33&quot;></circle><circle r=&quot;1.5&quot; stroke=&quot;black&quot; fill=&quot;#b3b3b3&quot; cx=&quot;28.386287689208984&quot; cy=&quot;48.23238754272461&quot; stroke-width=&quot;0.1&quot; data-type=&quot;element node&quot; data-element-id=&quot;12&quot; data-node-id=&quot;12&quot; data-label-id=&quot;34&quot;></circle><circle r=&quot;1.5&quot; stroke=&quot;black&quot; fill=&quot;#b3b3b3&quot; cx=&quot;67.34949493408203&quot; cy=&quot;48.06516647338867&quot; stroke-width=&quot;0.1&quot; data-type=&quot;element node&quot; data-element-id=&quot;13&quot; data-node-id=&quot;13&quot; data-label-id=&quot;35&quot;></circle><circle r=&quot;1.5&quot; stroke=&quot;black&quot; fill=&quot;#b3b3b3&quot; cx=&quot;27.21571922302246&quot; cy=&quot;64.95479583740234&quot; stroke-width=&quot;0.1&quot; data-type=&quot;element node&quot; data-element-id=&quot;14&quot; data-node-id=&quot;14&quot; data-label-id=&quot;36&quot;></circle><circle r=&quot;1.5&quot; stroke=&quot;black&quot; fill=&quot;#b3b3b3&quot; cx=&quot;65.844482421875&quot; cy=&quot;64.453125&quot; stroke-width=&quot;0.1&quot; data-type=&quot;element node&quot; data-element-id=&quot;15&quot; data-node-id=&quot;15&quot; data-label-id=&quot;37&quot;></circle><circle r=&quot;1.5&quot; stroke=&quot;black&quot; fill=&quot;#b3b3b3&quot; cx=&quot;30.72742462158203&quot; cy=&quot;85.02169036865234&quot; stroke-width=&quot;0.1&quot; data-type=&quot;element node&quot; data-element-id=&quot;16&quot; data-node-id=&quot;16&quot; data-label-id=&quot;38&quot;></circle><circle r=&quot;1.5&quot; stroke=&quot;black&quot; fill=&quot;#b3b3b3&quot; cx=&quot;59.82441329956055&quot; cy=&quot;83.85111999511719&quot; stroke-width=&quot;0.1&quot; data-type=&quot;element node&quot; data-element-id=&quot;17&quot; data-node-id=&quot;17&quot; data-label-id=&quot;39&quot;></circle>",
    "attributes": []
  }
]
```



| name | Data-Type | Format |
|--|--|--|
|confidence  |string  |between 0-1|
|type  |string  |Fixed value=rectangle|
|points  |list|[x1, y1, x2, y2]|
|label  |string|labels.get(class_id, "unknown")|

keypoints = ['nose', 'left_eye_inner', 'left_eye', 'left_eye_outer', 'right_eye_inner', 
             'right_eye', 'right_eye_outer', 'left_ear', 'right_ear', 'mouth_left', 
             'mouth_right', 'left_shoulder', 'right_shoulder ', 'left_elbow', 'right_elbow', 
             'left_wrist', 'right_wrist', 'left_pinky', 'right_pinky', 'left_index', 'right_index', 
             'left_thumb', 'right_thumb ', 'left_hip', 'right_hip', 'left_knee', 'right_knee', 
             'left_ankle', 'right_ankle ', 'left_heel', 'right_heel', 'left_foot_index', 'right_foot_index']

src="https://github.com/opencv/cvat/projects/16#:~:text=keypoints%20%3D%20%5B%27nose%27%2C%20%27left_eye_inner,landmark%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%22type%22%3A%20%22point%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D)"
results = []
results.append({
          
          "label": keypoints,
          "points": [[x.x, x.y, x.z, x.visibility] for x in results.pose_landmarks.landmark],
          "type": "point",
      })
--->

**Allowed label method:**

"rectangle","polygon","polyline","points","ellipse","cuboid","skeleton","mask"
