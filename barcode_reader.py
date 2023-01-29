import cv2
from pyzbar.pyzbar import decode
import PySimpleGUI as sg


layout = [[sg.Text("Insert a bottle to the feeder", text_color="snow",font=("Helvetica", 20), key="-TEXT-")],
          [sg.Image(filename="", key="-IMAGE-")]]
# layout2 = [[sg.Text("Do you want money?", text_color="snow",font=("Helvetica", 20), key="-TEXT2-")],
#               [sg.Image(filename="images.png", key="-IMAGE2-")],
#               [sg.Button("Yes"), sg.Button("No")]]
# Create the window
window = sg.Window("Demo", layout, margins=(100, 50))


def update(window):
    event, values = window.read(timeout=20)
    if event == sg.WIN_CLOSED or event == "Exit" or event == "Yes" or event == "No":
        window.close()

# Make one method to decode the barcode
def BarcodeReader(frame):
    # Decode the barcode image
    detectedBarcodes = decode(frame)

    # If not detected then print the message
    if detectedBarcodes:
        for barcode in detectedBarcodes:
            if barcode.data != "":
                # Print the barcode data
                return barcode

def main():
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            return 1

        update(window)
        try:
            imgbytes = cv2.imencode(".png", frame)[1].tobytes()
            window["-IMAGE-"].update(data=imgbytes)
        except:
            pass

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        barcode = BarcodeReader(gray)
        if barcode:
            rect = cv2.line(frame, (barcode.rect.left, barcode.rect.top),
                            (barcode.rect.left + barcode.rect.width, barcode.rect.top + barcode.rect.height),
                            (0, 255, 0), 5)
            # cv2.imshow('code', rect)
            # cv2.waitKey(1000)
            # cv2.destroyAllWindows()
            code = barcode.data.decode()
            if code in bottles:
                print("Barcode: " + code + " is " + bottles[code])
                window["-TEXT-"].update("This is " + bottles[code], text_color="lime green")
                update(window)
                # window2 = sg.Window("Money", layout2)
                # update(window2)
                # return bottles[code]
            else:
                print("Barcode: " + code + " is not in the database")
                window["-TEXT-"].update("This is unknown bottle", text_color="red")
                # return "reverse"
        else:
            window["-TEXT-"].update("Insert a bottle to the feeder", text_color="snow")

bottles = {"0611269101713": "redbull", "0012993101619": "laCroix",  "0049000009774": "dasani", "0049000040869": "coke", "0049000007909":"powerade"}
if __name__ == "__main__":
    main()




