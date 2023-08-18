from multiprocessing import Process, Queue, freeze_support
import time
import cv2
import onnxruntime
import numpy as np

def convert(cards):
    labels = ['10c', '10d', '10h', '10s', '2c', '2d', '2h', '2s', '3c', '3d',
              '3h', '3s', '4c', '4d', '4h', '4s', '5c', '5d', '5h', '5s', '6c',
              '6d', '6h', '6s', '7c', '7d', '7h', '7s', '8c', '8d', '8h', '8s',
              '9c', '9d', '9h', '9s', 'Ac', 'Ad', 'Ah', 'As', 'Jc', 'Jd', 'Jh',
              'Js', 'Kc', 'Kd', 'Kh', 'Ks', 'Qc', 'Qd', 'Qh', 'Qs']
    dict_card = {}
    for card in cards:
        if(labels[int(card[5])] in dict_card):
            if(card[2] < dict_card[labels[int(card[5])]][2]):
                dict_card[labels[int(card[5])]] = card
        else:
            dict_card[labels[int(card[5])]] = card
    points = []
    for i in dict_card:
        x = dict_card[i][1] + dict_card[i][3]
        y = dict_card[i][2] + dict_card[i][4]
        points.append([i, int(x/2), int(y/2)])
    order_dict = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}
    sorted_cards = sorted(points, key=lambda x: order_dict[x[0][:-1]])
    text = ''
    for point in sorted_cards:
        text += point[0] + ' '
    return text

# Đoạn mã thứ nhất
def code1(queue_in1, queue_in2):
    session = onnxruntime.InferenceSession(r'C:\Users\LAMHN\OneDrive - Hanoi University of Science and Technology\Hust\20222\CV\Project\weight_50.onnx')
    while(True):
        if not queue_in1.empty():
            frame = queue_in1.get()  # Lay frame anh tu code 2

            resized = cv2.resize(frame, (1280, 960), interpolation=cv2.INTER_LINEAR)
            img_in = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            img_in = np.transpose(img_in, (2, 0, 1)).astype(np.float32)
            img_in = np.expand_dims(img_in, axis=0)
            img_in /= 255.0
            input_name = session.get_inputs()[0].name
            outputs = session.run(None, {input_name: img_in})
            text = convert(outputs[0].tolist())
            print("Kết quả từ code 1:", text)
            queue_in2.put(text)  # Đưa kết quả vào queue


# Đoạn mã thứ hai
def code2(queue_in1, queue_in2, tmp):
    # Kiểm tra xem queue có kết quả từ code 1 hay không
    ip_address = '10.145.61.75'  # Thay đổi thành địa chỉ IP của điện thoại của bạn

    # Kết nối đến camera IP
    cap = cv2.VideoCapture(f'http://{ip_address}:4747/video')

    while(True):
        # Đọc khung hình từ camera
        ret, frame = cap.read()

        if not queue_in2.empty():
            result = queue_in2.get()  # Lấy text du doan
            text = result
            print("Kết quả lấy từ code 1:", result)
            queue_in1.put(frame)
        # Lay input
        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)
        cv2.rectangle(frame, (10, 475), (10+text_size[0], 465-text_size[1]), (255, 255, 255), -1)
        cv2.putText(frame, f'{text}', (10,470), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Hiển thị khung hình
        cv2.imshow('Camera', frame)

        # Đợi phím 'q' được nhấn để thoát khỏi vòng lặp
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# Tạo queue để chia sẻ kết quả giữa hai đoạn mã
queue = Queue()

# Khởi tạo và chạy hai tiến trình cho hai đoạn mã
if __name__ == '__main__':
    freeze_support()

    queue_in1 = Queue()
    queue_in2 = Queue()
    tmp = ''
    queue_in2.put('')
    process1 = Process(target=code1, args=(queue_in1, queue_in2,))
    process2 = Process(target=code2, args=(queue_in1, queue_in2, tmp,))
    process1.start()
    process2.start()
    process1.join()
    process2.join()