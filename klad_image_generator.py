# coding: UTF-8
import glob
import random
import cv2
import numpy as np
import pathlib
from PIL import ImageFont, ImageDraw, Image
from typing import Tuple, Optional, List


class KladImageGenerator:

    levm_lower_green = np.array([25, 20, 35], dtype="uint8")
    levm_upper_green = np.array([90, 225, 255], dtype="uint8")
    levm_min_counter_area = 350
    levm_fill_colour = (255, 255, 0)
    KEY_S = 115
    KEY_R = 114
    google_panorama_height = 8192
    google_panorama_width = 16384

    def __draw_utf8_text(self, image: np.ndarray, text: str) -> np.ndarray:
        height, width, _ = image.shape
        pil_image = Image.fromarray(image)
        font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 32)
        draw = ImageDraw.Draw(pil_image)
        draw.text((30, height - 80), text, font=font, fill=(0, 0, 255), spacing=6)
        return np.asarray(pil_image)

    def __gen_utf8_text(self, coords: str) -> str:
        return f"{coords}\n{random.choice("Меф,Мет".split(","))} {random.randint(1, 5)}г Прикоп {random.randint(2, 7)}см {random.choice("Синяя,Красная,Белая,Чёрная".split(","))} иза"

    def __resize_img_by_scale(self, image: np.ndarray, scale: float = 1.5) -> np.ndarray:
        height, width, _ = image.shape
        return cv2.resize(image, (int(width / scale), int(height / scale)))

    def __draw_arrow(self, image: np.ndarray, x, y, length=200) -> np.ndarray:
        return cv2.arrowedLine(image, (x + length, y + length), (x, y), (0, 0, 255), 3)

    def __process_image(self, raw_img: np.ndarray, path: str) -> Tuple[np.ndarray, ...]:
        # Cоздаём копию в hsv цветах
        hsv_image = cv2.cvtColor(raw_img, cv2.COLOR_BGR2HSV)
        height, width, _ = hsv_image.shape
        # Игнорируем верхнюю треть изображения
        hsv_image[0:int(height / 3), 0:width] = (0, 0, 0)

        # Находим контуры с площадью больше порога
        mask = cv2.inRange(hsv_image, self.levm_lower_green, self.levm_upper_green)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        size_filtered_counters = list(filter(lambda c: cv2.contourArea(c) > self.levm_min_counter_area, contours))

        # Заполнить на копии оригинального изображения отфильтрованные контуры
        img_filled_areas = raw_img.copy()
        cv2.drawContours(img_filled_areas, size_filtered_counters, -1, self.levm_fill_colour, thickness=cv2.FILLED)

        # Игнорируем верхнюю половину изображения
        img_for_choosing_point = img_filled_areas.copy()
        img_for_choosing_point[0:int(height / 2), 0:width] = (0, 0, 0)

        # Закрасить чёрным всё, кроме контуров
        hsv_bitwise_and = cv2.bitwise_and(raw_img, raw_img, mask=mask)

        # Итог
        result = raw_img.copy()
        # Выбираем случайный контур
        y_coords_array, x_coords_array = np.where(np.all(img_for_choosing_point == self.levm_fill_colour, axis=2))
        # Выбираем случайную точку в выбранном контуре
        i = random.randint(0, len(x_coords_array))
        cx, cy = x_coords_array[i], y_coords_array[i]
        # Рисуем стрелку
        result = self.__draw_arrow(result, cx, cy, 200)
        # Рисуем текст
        plib_path = pathlib.Path(path)
        result = self.__draw_utf8_text(result, self.__gen_utf8_text(plib_path.name if plib_path else ""))

        return raw_img, result, hsv_bitwise_and, img_filled_areas

    def __display_4_imgs_window(self, images: Tuple[np.ndarray, ...], description="") -> Optional[int]:
        MINIMUM_IMAGES_COUNT = 4
        converted_imgs = list(map(lambda img: self.__resize_img_by_scale(img), images))
        if not converted_imgs:
            return None
        if len(converted_imgs) < MINIMUM_IMAGES_COUNT:
            converted_imgs = [converted_imgs[0] for i in range(MINIMUM_IMAGES_COUNT)]
        cv2.imshow(description, np.concatenate(
            (np.concatenate((converted_imgs[0], converted_imgs[2]), axis=1),
             np.concatenate((converted_imgs[1], converted_imgs[3]), axis=1)), axis=0))
        key = cv2.waitKey(0)
        cv2.destroyAllWindows()
        return key

    def __split_google_panorama(self, path: str) -> List[np.ndarray]:
        raw_img = cv2.imread(path)
        raw_height, raw_width, _ = raw_img.shape
        splitted_imgs = []
        if raw_height == self.google_panorama_height and raw_width == self.google_panorama_width:
            splitted_imgs.append(raw_img[0:int(raw_height / 2), 0:int(raw_width / 2)])
            splitted_imgs.append(raw_img[int(raw_height / 2):raw_height, int(raw_width / 2):raw_width])
        else:
            splitted_imgs.append(raw_img)
        return splitted_imgs

    def __mianloop(self, path: str):
        for img in self.__split_google_panorama(path):
            while True:
                imgs = self.__process_image(img, path)
                ret_key = self.__display_4_imgs_window(imgs,
                                                       description=f"{path} r - recreate, s - save, other key - skip")
                if ret_key == self.KEY_R:
                    continue
                elif ret_key == self.KEY_S:
                    if parsed_path := pathlib.Path(path):
                        img_name = parsed_path.name
                        parsed_path = parsed_path.parent / "ai_results"
                        parsed_path.mkdir(parents=True, exist_ok=True)
                        cv2.imwrite(str(parsed_path / img_name), imgs[1] if len(imgs) > 1 else imgs[0])
                break

    def process_folder(self, path: str):
        for p in glob.glob(path):
            self.__mianloop(p)


kig = KladImageGenerator()
kig.process_folder("./ai_results/*.jpg")

#
# # -----------------
#
#
# def _first(filepath: str) -> cv2.typing.MatLike:
#     image = cv2.imread(filepath, cv2.IMREAD_COLOR)
#     imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     ret, im_th = cv2.threshold(imgray, 120, 255, cv2.THRESH_TRIANGLE)
#     contours, hierarchy = cv2.findContours(im_th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     cv2.drawContours(image, contours, -3, (255, 0, 0), 6)
#     cv2.imshow('Full Mask', image)
#     cv2.waitKey(0)
#     #return image
#
#
# def _second():
#     image = cv2.imread("a2c6eeccdbf404ea42c0421f52293435f203ec479f_hq.jpg", cv2.IMREAD_COLOR)
#     hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     lower_green = np.array([25, 20, 35], dtype="uint8")
#     upper_green = np.array([90, 225, 255], dtype="uint8")
#     mask = cv2.inRange(image, lower_green, upper_green)
#     w_3c = np.full_like(image, fill_value=(255, 255, 255))
#     contours, _ = cv2.findContours(hsv_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     #img_m = cv2.bitwise_and(hsv_image, w_3c, mask=mask)
#     cv2.drawContours(image, contours, -1, (255,), 10)
#
#     cv2.imshow('Full Mask', image)
#     cv2.waitKey(0)
#     #return image
#     #new_image = np.where(mask, np.uint8(0), np.uint8(255))
#
#     #print(contours)
#     cv2.drawContours(image, contours, -1, (255,), 10)
#     new_image = np.where(mask, np.uint8(0), np.uint8(255))
#     new_image = cv2.erode(new_image, kernel=np.ones((7, 7)))
#     ret, im_th = cv2.threshold(hsv_image, 200, 255, cv2.THRESH_BINARY_INV)
#     contours, hierarchy = cv2.findContours(im_th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#
#     cv2.drawContours(hsv_image, contours, -1, (56, 110, 0), 3)
#     cv2.imshow('Full Mask', new_image)
#     #labels, stats = cv2.connectedComponentsWithStats(new_image)[1:3]
#     #cv2.imshow('Full Mask', hsv_image)
#     cv2.waitKey(0)
#     #cv2.imshow('Full Mask', new_image)
#     #cv2.waitKey(0)
#     #new_image = np.where(mask, np.uint8(0), np.uint8(255))

# # -----------------
