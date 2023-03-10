from datetime import datetime
import os
import pandas as pd
import numpy as np
import cv2
import pytesseract as pyt


class MouseGesture():
    def __init__(self) -> None:
        self.is_dragging = False 
        # 마우스 위치 값 임시 저장을 위한 변수 
        self.x0, self.y0, self.w0, self.h0 = -1,-1,-1,-1

    def on_mouse(self, event, x, y, flags, param):
        global roi_pos
        if event == cv2.EVENT_LBUTTONDOWN:
            self.x0 = x
            self.y0 = y
            self.is_dragging = True
        elif event == cv2.EVENT_LBUTTONUP:
            self.is_dragging = False
            cv2.rectangle(param['image'], (self.x0, self.y0), (x,y),(0,0,255),1)            
            cv2.imshow(param['window_name'], param['image'])
            roi_pos = ((self.x0,self.y0),(x,y))
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.is_dragging:
                temp_img = param['image'].copy()
                cv2.rectangle(temp_img, (self.x0, self.y0), (x,y),(0,0,255),1)
                cv2.imshow(param['window_name'], temp_img)
        return 

roi_pos = ()
def get_roi(img):
    # img = cv2.resize(img, (0,0), fx=, fy=0.5)
    window_name = 'mouse_callback'
    mouse_class = MouseGesture()
    param = {
        "image" : img,
        "window_name" : window_name
    }
    cv2.imshow(window_name, img)
    cv2.setMouseCallback(window_name, mouse_class.on_mouse, param=param)
    cv2.waitKey(0)

def get_word_ls_eng(img):
    import pytesseract as pyt
    pyt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text_en = pyt.image_to_string(img, lang="eng")
    word_ls = []
    for word in text_en.split("\n"):
        word = word.replace("{","(").replace("}",")").replace("[","(").replace("]",")").replace(":",")").replace("  ", "")
        if word:    
            word_ls.append(word)
    return word_ls


def get_eng_words(img_name, scale):
    global eng_roi
    current_path = os.path.dirname(os.path.realpath(__file__))
    image_path = f"{current_path}\\" + img_name
    sample = np.fromfile(image_path, np.uint8)
    img1 = cv2.imdecode(sample, cv2.IMREAD_COLOR)
    get_roi(cv2.resize(img1, (0,0), fx=1/scale, fy=1/scale))
    roi_x = roi_pos[0][0]*scale, roi_pos[1][0]*scale
    roi_y = roi_pos[0][1]*scale, roi_pos[1][1]*scale
    eng_roi = img1[min(roi_y):max(roi_y), min(roi_x):max(roi_x)]


    # cv2.imshow("", cv2.resize(roi, (0,0), fx=1/scale, fy=1/scale))
    # cv2.waitKey(0)

    mark = np.copy(eng_roi)
    blue_threshold = 80
    green_threshold = 80
    red_threshold = 80
    bgr_threshold = [blue_threshold, green_threshold, red_threshold]
    thresholds = (eng_roi[:,:,0] > bgr_threshold[0]) \
                | (eng_roi[:,:,1] > bgr_threshold[1]) \
                | (eng_roi[:,:,2] > bgr_threshold[2])
    mark[thresholds] = [255,255,255]


    return get_word_ls_eng(mark)


def get_word_ls_kor(img):
    pyt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text_en = pyt.image_to_string(img, lang="kor")
    word_ls = []
    for word in text_en.split("\n"):
        word = word.replace("{","(").replace("}",")").replace("[","(").replace("]",")").replace(":",")").replace("  ", "")
        if word:    
            word_ls.append(word)
    return word_ls


def get_kor_words(img_name, scale):
    global kor_roi
    current_path = os.path.dirname(os.path.realpath(__file__))
    image_path = f"{current_path}\\" + img_name
    sample = np.fromfile(image_path, np.uint8)
    img1 = cv2.imdecode(sample, cv2.IMREAD_COLOR)    
    get_roi(cv2.resize(img1, (0,0), fx=1/scale, fy=1/scale))
    roi_x = roi_pos[0][0]*scale, roi_pos[1][0]*scale
    roi_y = roi_pos[0][1]*scale, roi_pos[1][1]*scale
    kor_roi = img1[min(roi_y):max(roi_y), min(roi_x):max(roi_x)]

    mark = np.copy(kor_roi)
    blue_threshold = 80
    green_threshold = 80
    red_threshold = 80
    bgr_threshold = [blue_threshold, green_threshold, red_threshold]
    thresholds = (kor_roi[:,:,0] > bgr_threshold[0]) \
                | (kor_roi[:,:,1] > bgr_threshold[1]) \
                | (kor_roi[:,:,2] > bgr_threshold[2])
    mark[thresholds] = [255,255,255]

    return get_word_ls_kor(mark)


def change_thr_word():
    global eng_roi
    mark = np.copy(eng_roi)
    threshold = int(thr_entry.get())
    blue_threshold = threshold
    green_threshold = threshold
    red_threshold = threshold
    bgr_threshold = [blue_threshold, green_threshold, red_threshold]
    thresholds = (eng_roi[:,:,0] > bgr_threshold[0]) \
                | (eng_roi[:,:,1] > bgr_threshold[1]) \
                | (eng_roi[:,:,2] > bgr_threshold[2])
    mark[thresholds] = [255,255,255]

    return get_word_ls_eng(mark)


def change_thr_mean():
    global kor_roi
    mark = np.copy(kor_roi)
    threshold = int(thr_entry.get())
    blue_threshold = threshold
    green_threshold = threshold
    red_threshold = threshold
    bgr_threshold = [blue_threshold, green_threshold, red_threshold]
    thresholds = (kor_roi[:,:,0] > bgr_threshold[0]) \
                | (kor_roi[:,:,1] > bgr_threshold[1]) \
                | (kor_roi[:,:,2] > bgr_threshold[2])
    mark[thresholds] = [255,255,255]

    return get_word_ls_kor(mark)


def change_thr(event):
    global word_ls, mean_ls
    word_ls = change_thr_word()
    mean_ls = change_thr_mean()
    update()


word_ls = get_eng_words("sample1.jpg",2)
mean_ls = get_kor_words("sample1.jpg",2)


import tkinter
import tkinter.ttk

window = tkinter.Tk()
window.title("image to voca")
window.geometry("600x400+200+200")

treeview = tkinter.ttk.Treeview(window, 
    column=["idx", "word", "mean"],
    displaycolumns=["idx", "word", "mean"])
treeview.pack(fill=tkinter.BOTH,expand=1)

treeview.column("idx", width=50, anchor="center")
treeview.heading("idx", text="번호", anchor="center")

treeview.column("word", width=200, anchor="center")
treeview.heading("word", text="단어", anchor="center")

treeview.column("mean", width=200, anchor="center")
treeview.heading("mean", text="뜻", anchor="center")

# 컬럼제목만 보이게함
treeview["show"] = "headings"
 

for i in range(max(len(word_ls), len(mean_ls)) - 1):
    try:
        treeview.insert("", "end", text="", values=[i+1, word_ls[i], mean_ls[i]], iid=i)
    except IndexError:
        try:
            treeview.insert("", "end", text="", values=[i+1, "", mean_ls[i]], iid=i)
        except IndexError:
            try:
                treeview.insert("", "end", text="", values=[i+1, word_ls[i], ""], iid=i)
            except IndexError:
                pass







def modify_tree(event):
    value = treeview.item(treeview.selection())["values"]
    treeview.item(treeview.selection(), values=[value[0], modify_word.get(), modify_mean.get()])
    word_ls[int(treeview.focus())] = modify_word.get()
    mean_ls[int(treeview.focus())] = modify_mean.get()
    print(value)



modify_frame = tkinter.Frame(window)
modify_frame.pack()

modify_word = tkinter.Entry(modify_frame, width=20)
modify_word.grid(row=1, column=1, padx=2)
modify_word.bind("<Return>", modify_tree)

modify_mean = tkinter.Entry(modify_frame, width=20)
modify_mean.grid(row=1, column=2)
modify_mean.bind("<Return>", modify_tree)
  


def add_word(event):
    idx = int(treeview.focus())
    word_ls.insert(idx, "")
    update()
    treeview.focus(idx+1)
    treeview.selection_set(idx+1)

def add_mean(event):
    idx = int(treeview.focus())
    mean_ls.insert(idx, "")
    update()
    treeview.focus(idx+1)
    treeview.selection_set(idx+1)



def remove_word(event):
    idx = int(treeview.focus())
    word_ls.pop(idx)
    update()
    treeview.focus(idx)
    treeview.selection_set(idx)

def remove_mean(event):
    idx = int(treeview.focus())
    mean_ls.pop(idx)
    update()
    treeview.focus(idx)
    treeview.selection_set(idx)


def click_item(event):
    selectedItem = treeview.focus()
    getValue = treeview.item(selectedItem).get('values')  # 딕셔너리의 값만 가져오기
    modify_word.delete
    modify_word.delete(0, "end")
    modify_word.insert("end", str(getValue[1]))
    modify_mean.delete(0, "end")
    modify_mean.insert("end", str(getValue[2]))
    # modify_word.configure(text=getValue)  # 라벨 내용 바꾸기


def up_item(event):
    selectedItem = str(int(treeview.focus())-1)
    getValue = treeview.item(selectedItem).get('values')  # 딕셔너리의 값만 가져오기
    modify_word.delete
    modify_word.delete(0, "end")
    modify_word.insert("end", str(getValue[1]))
    modify_mean.delete(0, "end")
    modify_mean.insert("end", str(getValue[2]))



def down_item(event):
    selectedItem = str(int(treeview.focus())+1)
    getValue = treeview.item(selectedItem).get('values')  # 딕셔너리의 값만 가져오기
    modify_word.delete
    modify_word.delete(0, "end")
    modify_word.insert("end", str(getValue[1]))
    modify_mean.delete(0, "end")
    modify_mean.insert("end", str(getValue[2]))



def update():
    for i in treeview.get_children():
        treeview.delete(i)
    for i in range(max(len(word_ls), len(mean_ls))):
        try:
            treeview.insert("", "end", text="", values=[i+1, word_ls[i], mean_ls[i]], iid=i)
        except IndexError:
            try:
                treeview.insert("", "end", text="", values=[i+1, "", mean_ls[i]], iid=i)
            except IndexError:
                try:
                    treeview.insert("", "end", text="", values=[i+1, word_ls[i], ""], iid=i)
                except IndexError:
                    pass



def delete():
    idx = int(treeview.focus())
    word_ls.pop(idx)
    mean_ls.pop(idx)
    update()


treeview.bind("<ButtonRelease-1>", click_item)
treeview.bind("<Return>", click_item)
treeview.bind("<Left>", add_word)
treeview.bind("<Right>", add_mean)

treeview.bind("<Shift-Left>", remove_word)
treeview.bind("<Shift-Right>", remove_mean)


treeview.bind("<Up>", up_item)
treeview.bind("<Down>", down_item)





thr_entry = tkinter.Entry(width = 10)
thr_entry.pack()
thr_entry.bind("<Return>", change_thr)


menu = tkinter.Menu(window)
window.config(menu=menu)


menu_file = tkinter.Menu(menu, tearoff=0)




def save():
    need = len(word_ls) - len(mean_ls)
    word_copy = word_ls.copy()
    mean_copy = mean_ls.copy()
    if need >= 0:
        for k in range(need):
            mean_copy.append("")
    else:
        for k in range(abs(need)):
            word_copy.append("")
    df = pd.DataFrame(word_copy, columns = ['word'])
    df["mean"] = mean_copy
    current_path = os.path.dirname(os.path.realpath(__file__))
    filename = str(datetime.now()).replace(":", "_")
    df.to_csv(f"{current_path}\\words\\{filename}.csv", index=False, header=False,encoding="cp949")
    
    
menu_file.add_command(label="Save", command=save)
menu_file.add_separator()
menu_file.add_command(label="Exit", command=window.quit)
menu.add_cascade(label="file",menu=menu_file)


window.mainloop()