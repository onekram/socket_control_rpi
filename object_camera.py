import cv2
import numpy as np
from movement import *

# минимальный размер контуров пятна
BLOBSIZE = 100
S_MIN = 29
S_MAX = 255
V_MIN = 148
V_MAX = 255
# цвет прямоугольника (B, G, R)
RECTCOLOR = (0, 255, 0)
# толщина линии прямоугольника
RTHICK = 2

def check_size(w, h):
    if w * h > BLOBSIZE:
        return True
    else:
        return False

def follow_object(s: socket.socket):
    cap = cv2.VideoCapture("http://192.168.2.99:8080/?action=stream")  # Открываем видеопоток с камеры
    cap.set(3, 320)  # Устанавливаем ширину изображения в 320 пикселей
    cap.set(4, 320)  # Устанавливаем высоту изображения в 320 пикселей
    i = 0
    while True:  # Бесконечный цикл
        i += 1
        ret, frame = cap.read()  # Считываем кадр с камеры
        cv2.imwrite(f"camera/captured_frame_{i}.jpg", frame)
        if ret == 1:  # Проверяем, работает ли камера
            frame = cv2.GaussianBlur(frame, (5, 5), 0)  # Применяем гауссово размытие к изображению
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Преобразуем изображение в цветовое пространство HSV
            h_min = 0
            h_max = 25

            # определяем границы цвета в HSV
            lower_range = np.array([h_min, S_MIN, V_MIN])
            upper_range = np.array([h_max, S_MAX, V_MAX])

            mask = cv2.inRange(hsv, lower_range, upper_range)  # Создаем маску для выбранного цвета

            mask = cv2.erode(mask, None, iterations=2)  # Применяем операцию эрозии к маске
            mask = cv2.GaussianBlur(mask, (3, 3), 0)  # Применяем гауссово размытие к маске
            res = cv2.bitwise_and(frame, frame, mask=mask)  # Объединяем изображение с маской

            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  # Находим контуры объектов

            if len(cnts) > 0:  # Если найдены контуры
                cnt = max(cnts, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(cnt)
                if check_size(w, h):

                    # центр кубика
                    center_x = (x + w) // 2
                    center_y = (y + h) // 2

                    cv2.putText(frame, f"x={center_x}, y = {center_y}, size={w * h}", (center_x, center_y),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1, (255, 255, 255), 2)
                    d_x = 150
                    time_sleep = 0.1
                    cub_size = 15000
                    if center_x < d_x-30:
                        turn_to_left(s, time_sleep)
                    elif center_x > d_x+30:
                        turn_to_right(s, time_sleep)
                    else:
                        if w * h < cub_size:
                            forward_time(s, time_sleep)
                        else:
                            pass

                    cv2.rectangle(frame, (x, y), (x + w, y + h), RECTCOLOR, RTHICK)

            # Показываем картинку с квадратом выделения
            cv2.imshow("Image", frame)

            # Если была нажата клавиша ESC
            k = cv2.waitKey(1)
            if k == 27:
                # прерываем выполнение цикла
                break
    cap.release()
    cv2.destroyAllWindows()
