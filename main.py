import argparse

import cv2


class ImageUtility:
    def __init__(self, image, path):
        self.drawing = False
        self.finish = False
        self.image = image
        self.copy_image = self.image.copy()
        self.rectangles = []
        self.first_point = None
        self.second_point = None
        self.x_start, self.y_start, self.x_end, self.y_end = -1, -1, -1, -1
        height, width, __ = self.image.shape
        self.path = path
        self.thickness = 1 + height//1000

    def select_image(self):
        cv2.namedWindow('image', flags=cv2.WINDOW_FREERATIO)
        cv2.resizeWindow('image', 1400, 2000)
        cv2.setMouseCallback('image', self.draw_rectangle)

        while True:
            cv2.imshow('image', self.copy_image)
            if self.drawing:
                self.copy_image = self.image.copy()
            if self.finish:
                cv2.imshow('image', self.image)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break
            elif k == ord('r'):
                self.image = cv2.imread(self.path)
                self.copy_image = self.image.copy()
                self.reset()
            elif k == ord('z'):
                self.first_point = None
                print('undo')
                self.undo()
                self.copy_image = self.image.copy()

        cv2.destroyAllWindows()

    def reset(self):
        self.finish = False
        self.rectangles = []

    def undo(self):
        self.finish = False
        self.image = cv2.imread(self.path)
        if len(self.rectangles) > 0:
            self.rectangles.pop()
            for rectangle in self.rectangles:
                cv2.rectangle(
                    self.image,
                    (rectangle[0], rectangle[1]), (rectangle[2], rectangle[3]),
                    (0, 255, 0),
                    self.thickness
                )
        else:
            self.reset()

    def draw_rectangle(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.finish = False
            self.x_start, self.y_start = x, y

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                cv2.rectangle(
                    self.copy_image,
                    (self.x_start, self.y_start),
                    (x, y),
                    (0, 255, 0),
                    self.thickness
                )

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.finish = True
            self.x_end = x
            self.y_end = y
            cv2.rectangle(
                self.image,
                (self.x_start, self.y_start),
                (x, y),
                (0, 255, 0),
                self.thickness
            )
            if self.x_start == self.x_end and self.y_start == self.y_end:
                if self.first_point:
                    self.second_point = (x, y)
                    cv2.rectangle(
                        self.image,
                        self.first_point,
                        self.second_point,
                        (0, 255, 0),
                        self.thickness
                    )
                    self.rectangles.append(
                        (self.first_point[0],
                         self.first_point[1],
                         self.second_point[0],
                         self.second_point[1])
                    )
                    print(
                        f'Location({self.first_point[0]},'
                        f' {self.first_point[1]},'
                        f' {abs(self.second_point[0]-self.first_point[0])},'
                        f' {abs(self.second_point[1]-self.first_point[1])})'
                    )
                    self.first_point = None
                    self.second_point = None
                else:
                    self.first_point = (x, y)
            else:
                cv2.rectangle(
                    self.image,
                    (self.x_start, self.y_start),
                    (x, y),
                    (0, 255, 0),
                    self.thickness
                )
                self.rectangles.append(
                    (self.x_start,
                     self.y_start,
                     self.x_end,
                     self.y_end)
                )
                print(
                    f'Location({self.x_start},'
                    f' {self.y_start},'
                    f' {abs(self.x_end-self.x_start)},'
                    f' {abs(self.y_end-self.y_start)})'
                )
                print(f'{{x: {self.x_start }, y: {self.y_start}, w: {abs(self.x_end-self.x_start)}, z: {abs(self.y_end-self.y_start)}}}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path',
        help='path to image'
    )
    parser.parse_args()
    args = vars(parser.parse_args())

    image = cv2.imread(args['path'])
    ImageUtility(image, args['path']).select_image()


if __name__ == '__main__':
    main()
