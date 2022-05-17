# SERVO för höjdled
#Set function to calculate percent from angle
def angle_to_percent (angle) :
    if angle > 180 or angle < 0 :
        return False

    start = 4
    end = 12.5
    ratio = (end - start)/180 #Calcul ratio from angle to percent
    angle_as_percent = angle * ratio
    return start + angle_as_percent

GPIO.setmode(GPIO.BOARD) #Use Board numerotation mode
GPIO.setwarnings(False) #Disable warnings

#Use pin 12 for PWM signal
pwm_gpio = 12
frequence = 50
GPIO.setup(pwm_gpio, GPIO.OUT)
pwm = GPIO.PWM(pwm_gpio, frequence)

#Init at 90°
present_angle = 90
pwm.start(angle_to_percent(present_angle))
time.sleep(1)

lower_limit = 60
upper_limit = 120
####

### Ventil ###


### Vippa ###

###
import cv2

# Opencv DNN
net = cv2.dnn.readNet("dnn_model/yolov4-tiny.weights", "dnn_model/yolov4-tiny.cfg")
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(320, 320), scale=1/255)

# Load class lists
classes = []
with open("dnn_model/classes.txt", "r") as file_object:
    for class_name in file_object.readlines():
        class_name = class_name.strip()
        classes.append(class_name)

# print("Objects list")
# print(classes)


# Initalize camera
frame_width = 1280
frame_height = 720
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
# FULL HD 1920 x 1080


while True:
    # Get frames
    ret, frame = cap.read()

    # Object detection
    (x, y, w, h) = []
    (class_ids, scores, bboxes) = model.detect(frame)
    for class_id, score, bbox in zip(class_ids, scores, bboxes):
        (x, y, w, h) = bbox
        class_name = classes[class_id]

        cv2.putText(frame, class_name, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 2, (200, 0, 50), 2)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (200, 0, 50), 3)

    # print("class ids", class_ids)
    # print("scores", scores)
    # print("bboxes", bboxes)

    # Styra servo upp/ner
    u = frame_height*0.5 - 50
    l = frame_height*0.5 + 50

    if not ((y > u and y < l) or (h > u and h < l)):
        if (y > l and present_angle >= (lower_limit+2)):
            present_angle = angle_to_percent((present_angle-2))
            pwm.ChangeDutyCycle(present_angle)
            time.sleep(1)
        elif (y+h < u and present_angle <= upper_limit-2):
            present_angle = angle_to_percent((present_angle + 2))
            pwm.ChangeDutyCycle(present_angle)
            time.sleep(1)

    # Avståndsbedömning, ja eller nej

    if not bbox :   #Vad händer om den är odefinierad?
        skjutvillkor = 0
    else :
        sida = max(w, h)
        if sida < 10:
            skjutvillkor = 0
        else:
            skjutvillkor = 1

    # Vippor på eller av
    vippvillkor = 0
    vippvillkor_M = 0

    # Utskjutning
    if ((skjutvillkor == 1 or vippvillkor_M == 1) and vippvillkor == 1)
        # Öppna ventilen


    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

# Close all windows and the camera
cap.release()
cv2.destroyAllWindows()

#Close GPIO & cleanup
pwm.stop()
GPIO.cleanup()