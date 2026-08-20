import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision


#grabbing the base model file for facial landmarks
base_options = mp_python.BaseOptions(model_asset_path='face_landmarker.task')

options = vision.FaceLandmarkerOptions(
    base_options = base_options, #using the model file
    output_face_blendshapes = True,
    num_faces = 1  # no. of faces to look at
)

#basically just computes throught different paramenters using pixel distances( things like mouth openness, right sideness etc.)
landmarker= vision.FaceLandmarker.create_from_options(options)

images = {
    "smiling": cv2.imread("smile.png"),
    "neutral": cv2.imread("neutral.png"),
    "huge_smile": cv2.imread("big_smile.png"),
    "squint": cv2.imread("squint.png"),
    "the_rock_right": cv2.imread("the_rock_right_down.png"),
    "the_rock_left": cv2.imread("the_rock_left_down.png")
    }





#opens the webcam

cap= cv2.VideoCapture(0)  #0-default webcam, if external, put (1)


while True:
    
    ret, frame = cap.read()   #reads the current camera frame
    if not ret:
        break

    mirror_frame = cv2.flip(frame,1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # mediapipe uses rgb, opencv gives us bgr so converting to rgb

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)  #basically opencv image format to mp format

    result= landmarker.detect(mp_image) #the ai gives back all the data it found, face posn, landmark pts, and blendshape scores

    current_state= "neutral"

    if result.face_blendshapes:

        blendshapes = {b.category_name : b.score for b in result.face_blendshapes[0] } #dictionary checking all the elements in mediapipe library one by one and assigning a score to them


    smile_score = blendshapes.get("mouthSmileLeft",0)
    jaw_open_score = blendshapes.get("jawOpen",0)  #get this particular blendshape from the library
    left_eye_squint = blendshapes.get("eyeSquintLeft",0) 
    right_eye_squint = blendshapes.get("eyeSquintRight",0)
    squint_score= (left_eye_squint + right_eye_squint)/2
    brow_down_right= blendshapes.get("browDownRight",0)
    brow_down_left = blendshapes.get("browDownLeft",0)



    if smile_score > 0.5:
        current_state = "smiling"
    elif jaw_open_score >0.5:
         current_state = "huge_smile"   
    elif squint_score >0.5    :
        current_state = "squint"
    elif brow_down_right > 0.5:
        current_state = "the_rock_right"   
    elif brow_down_left > 0.5 :
        current_state = "the_rock_left"
    else:
        current_state="neutral"

    cv2.imshow("Webcam", mirror_frame)    


    if images[current_state] is not None:
        cv2.imshow("Hampter", images[current_state])


    if cv2.waitKey(1) & 0xFF == ord('q')  :
        break


cap.release
cv2.destroyAllWindows


