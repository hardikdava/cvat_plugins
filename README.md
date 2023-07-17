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
