# ugly-ahh-hampters

Real-time facial expression recognition that shows a matching hamster picture. Make a face at your webcam, and the hamster copies it.

Built with [MediaPipe](https://developers.google.com/mediapipe) Face Landmarker + OpenCV.

## How it works

1. OpenCV grabs a webcam frame and mirrors it.
2. MediaPipe's Face Landmarker returns blendshape scores (0 to 1) for facial movements, e.g. `mouthSmileLeft`, `jawOpen`, `eyeSquintLeft`.
3. Simple threshold rules turn those scores into an expression.
4. The matching hamster image is shown in a second window.

## Expressions

| Expression | Trigger | Image |
|---|---|---|
| Neutral | none of the below | `neutral.png` |
| Smiling | smile > 0.5 | `smile.png` |
| Huge smile | smile > 0.5 and jaw open > 0.5 | `big_smile.png` |
| Squint | avg eye squint > 0.5 | `squint.png` |
| The Rock (right) | right brow down > 0.5 | `the_rock_right_down.png` |
| The Rock (left) | left brow down > 0.5 | `the_rock_left_down.png` |

Thresholds are constants at the top of `main.py`.

## Project structure

```
ugly-ahh-hampters/
├── main.py
├── requirements.txt
├── face_landmarker.task      # downloaded model (see Setup)
├── neutral.png
├── smile.png
├── big_smile.png
├── squint.png
├── the_rock_right_down.png
└── the_rock_left_down.png
```

## Setup

Requires Python 3.9+ and a webcam.

```bash
git clone https://github.com/luxyab/ugly-ahh-hampters
cd ugly-ahh-hampters
pip install -r requirements.txt
```

Download the model file into the project folder:

```bash
curl -O https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task
```

## Run

```bash
python main.py
```

Two windows open: your webcam and the hamster. Press **q** to quit.

## Troubleshooting

- **No webcam window:** change `cv2.VideoCapture(0)` to `1` for an external camera.
- **Hamster not showing:** check the image filename matches exactly. Missing images print a warning on startup.
- **Model not found error:** make sure `face_landmarker.task` is in the same folder as `main.py`.
- **Too sensitive or too dull:** tune the thresholds at the top of `main.py`.