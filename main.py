import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os
import cv2
from matplotlib import image
from numpy import result_type
from signature import match, matchCropped


# Mach Threshold
THRESHOLD = 85
ref_point = []


def browsefunc(ent):
    filename = askopenfilename(filetypes=([
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg"),
    ]))
    ent.delete(0, tk.END)
    ent.insert(tk.END, filename)  # add this


def capture_image_from_cam_into_temp(sign=1):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    cv2.namedWindow("test")

    # img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            if not os.path.isdir('temp'):
                os.mkdir('temp', mode=0o777)  # make sure the directory exists
            # img_name = "./temp/opencv_frame_{}.png".format(img_counter)
            if(sign == 1):
                img_name = "./temp/test_img1.png"
            else:
                img_name = "./temp/test_img2.png"
            print('imwrite=', cv2.imwrite(filename=img_name, img=frame))
            print("{} written!".format(img_name))
            # img_counter += 1
    cam.release()
    cv2.destroyAllWindows()
    return True


def captureImage(ent, sign=1):
    if(sign == 1):
        filename = os.getcwd()+'\\temp\\test_img1.png'
    else:
        filename = os.getcwd()+'\\temp\\test_img2.png'
    # messagebox.showinfo(
    #     'SUCCESS!!!', 'Press Space Bar to click picture and ESC to exit')
    res = None
    res = messagebox.askquestion(
        'Click Picture', 'Press Space Bar to click picture and ESC to exit')
    if res == 'yes':
        capture_image_from_cam_into_temp(sign=sign)
        ent.delete(0, tk.END)
        ent.insert(tk.END, filename)
    return True


def checkSimilarity(window, path1, path2):
    result = match(path1=path1, path2=path2)
    if(result <= THRESHOLD):
        messagebox.showerror("Failure: Signatures Do Not Match",
                             "Signatures are "+str(result)+f" % similar!!")
        pass
    else:
        messagebox.showinfo("Success: Signatures Match",
                            "Signatures are "+str(result)+f" % similar!!")
    return True


def shape_selection(event, x, y, flags, param):
    # grab references to the global variables
    global ref_point
    image = param[0]
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being performed
    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        ref_point.append((x, y))

        # draw a rectangle around the region of interest
        cv2.rectangle(image, ref_point[0], ref_point[1], (0, 255, 0), 1)
        cv2.imshow("Image1", image)


def crop_compare(window, path1, path2):
    global ref_point
    # read the images
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)
    # turn images to grayscale
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # cropping first image
    image = img1.copy()
    clone = image.copy()
    ref_point = []
    cv2.namedWindow("Image1")
    param = [image]
    cv2.setMouseCallback("Image1", shape_selection, param)
    while True:
        # display the image and wait for a keypress
        cv2.imshow("Image1", image)
        key = cv2.waitKey(1) & 0xFF
        # press 'r' to reset the window
        if key == ord("r"):
            image = clone.copy()

        # if the 'esc' key is pressed, break from the loop
        elif key % 256 == 27 or cv2.waitKey(0):
            break
    # close all open windows
    cv2.destroyAllWindows()
    # print("reference points", ref_point)
    # print("reference points",
    #       ref_point[0][0], ref_point[0][1], ref_point[1][0], ref_point[1][1],)
    top_left_x = min([ref_point[1][0], ref_point[0][0]])
    top_left_y = min([ref_point[0][1], ref_point[1][1]])
    bot_right_x = max([ref_point[1][0], ref_point[0][0]])
    bot_right_y = max([ref_point[0][1], ref_point[1][1]])
    newImg1 = clone[top_left_y:bot_right_y+1, top_left_x:bot_right_x+1]
    # print("New Image -=====-", newImg1)
    cv2.imshow("Final image 1 used for comparison", newImg1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # cropping second image
    image = img2.copy()
    clone = image.copy()
    ref_point = []
    cv2.namedWindow("Image1")
    param = [image]
    cv2.setMouseCallback("Image1", shape_selection, param)
    while True:
        # display the image and wait for a keypress
        cv2.imshow("Image1", image)
        key = cv2.waitKey(1) & 0xFF
        # press 'r' to reset the window
        if key == ord("r"):
            image = clone.copy()

        # if the 'esc' key is pressed, break from the loop
        elif key % 256 == 27 or cv2.waitKey(0):
            break
    # close all open windows
    cv2.destroyAllWindows()
    # print("reference points", ref_point)
    # print("reference points",
    #       ref_point[0][0], ref_point[0][1], ref_point[1][0], ref_point[1][1],)
    top_left_x = min([ref_point[1][0], ref_point[0][0]])
    top_left_y = min([ref_point[0][1], ref_point[1][1]])
    bot_right_x = max([ref_point[1][0], ref_point[0][0]])
    bot_right_y = max([ref_point[0][1], ref_point[1][1]])
    newImg2 = clone[top_left_y:bot_right_y+1, top_left_x:bot_right_x+1]
    # print("New Image -=====-", newImg1)
    cv2.imshow("Final image 2 used for comparison", newImg2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    result = matchCropped(newImg1, newImg2)
    if(result <= THRESHOLD):
        messagebox.showerror("Failure: Signatures Do Not Match",
                             "Signatures are "+str(result)+f" % similar!!")
        pass
    else:
        messagebox.showinfo("Success: Signatures Match",
                            "Signatures are "+str(result)+f" % similar!!")
    return True


def verify_images(window, path1, path2):
    result = match(path1=path1, path2=path2)
    if(result <= THRESHOLD):
        messagebox.showerror(
            message="Failure: Signatures Do Not Match",)
        pass
    else:
        messagebox.showinfo(
            message="Success: Signatures Match",)
    return True


root = tk.Tk()
root.title("Signature Matching")
root.geometry("500x700")  # 300x200
uname_label = tk.Label(root, text="Compare Two Signatures:", font=10)
uname_label.place(x=90, y=50)

img1_message = tk.Label(root, text="Signature 1", font=10)
img1_message.place(x=10, y=120)

image1_path_entry = tk.Entry(root, font=10)
image1_path_entry.place(x=150, y=120)

img1_capture_button = tk.Button(
    root, text="Capture", font=10, command=lambda: captureImage(ent=image1_path_entry, sign=1))
img1_capture_button.place(x=400, y=90)

img1_browse_button = tk.Button(
    root, text="Browse", font=10, command=lambda: browsefunc(ent=image1_path_entry))
img1_browse_button.place(x=400, y=140)

image2_path_entry = tk.Entry(root, font=10)
image2_path_entry.place(x=150, y=240)

img2_message = tk.Label(root, text="Signature 2", font=10)
img2_message.place(x=10, y=250)

img2_capture_button = tk.Button(
    root, text="Capture", font=10, command=lambda: captureImage(ent=image2_path_entry, sign=2))
img2_capture_button.place(x=400, y=210)

img2_browse_button = tk.Button(
    root, text="Browse", font=10, command=lambda: browsefunc(ent=image2_path_entry))
img2_browse_button.place(x=400, y=260)

verify_button = tk.Button(
    root, text="Verify", font=10, command=lambda: verify_images(window=root,
                                                                path1=image1_path_entry.get(),
                                                                path2=image2_path_entry.get(),))

verify_button.place(x=200, y=320)

compare_button = tk.Button(
    root, text="Compare", font=10, command=lambda: checkSimilarity(window=root,
                                                                   path1=image1_path_entry.get(),
                                                                   path2=image2_path_entry.get(),))

compare_button.place(x=200, y=380)

crop_compare_button = tk.Button(
    root, text="Crop and Compare", font=10, command=lambda: crop_compare(window=root,
                                                                         path1=image1_path_entry.get(),
                                                                         path2=image2_path_entry.get(),))

crop_compare_button.place(x=200, y=440)

root.mainloop()
