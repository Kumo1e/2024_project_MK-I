import cv2
import time

def put_cv2_text(image, text, org):
    cv2.putText( 
        img=image,
        text=text,
        org=org,  # 圖片的像素坐標系，Y軸是反過來的(向下變大)
        fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
        fontScale=0.8,
        color=(0, 255, 255), 
        thickness=2, 
        lineType=cv2.LINE_AA
    )            
def collator_image(file_path,category_name,camera_id=0):
    camera = cv2.VideoCapture(camera_id)
    is_collation_start = False
    while True:
        is_success, frame = camera.read()
        if is_success:
            show_frame = frame.copy()
            text = f"Category: {category_name}, Collecting: {is_collation_start}"
            put_cv2_text(show_frame, text, (25, 50))
            cv2.imshow("Collector", show_frame)
            if is_collation_start:
                # use camera to save images
                image_name = f"{time.time()}.jpg"
                filename = f"{file_path}/{category_name}/{image_name}"
                cv2.imwrite(filename, frame)
                key = cv2.waitKey(100)
            else:
                key = cv2.waitKey(1)
        else:
            print("Wait for camera ready......")
            key = cv2.waitKey(1000)

        if key == ord("q") or key == ord("Q"):
            break
        elif key == ord("a") or key == ord("A"):
            is_collation_start = True
        elif key == ord("z") or key == ord("Z"):
            is_collation_start = False

    cv2.destroyAllWindows()

if __name__ == "__main__":
    categories_name = ["tissue"]
    for category_name in categories_name:
        file_path = "images/object"
        camera_id = 1
        collator_image(file_path,category_name,camera_id)


        