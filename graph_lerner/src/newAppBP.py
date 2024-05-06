from remi import start, App
from remi.gui import VBox, TextInput, Button, Image, Label
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import base64
from io import BytesIO
from intern_learner import graph_learner as gln

class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)
        self.learner = gln()  # สร้าง instance ของ graph_learner
        self.history = []  # เก็บประวัติศาสตร์ข้อมูลภายนอกคลาส graph_learner

    def main(self):
        self.container = VBox(width='100%', style={'align-items': 'center', 'justify-content': 'center'})
        self.input_text = TextInput(width='80%', hint='Enter initial sequence separated by commas')
        self.plot_button = Button('Plot and Predict', width='200px', height='50px')
        self.plot_button.onclick.do(self.on_plot_and_predict)
        self.image = Image('/res:placeholder.png', width=500, height=300)
        self.container.append(self.input_text)
        self.container.append(self.plot_button)
        self.container.append(self.image)
        return self.container

    def on_plot_and_predict(self, widget):
        input_string = self.input_text.get_value()
        try:
            new_data = [float(i) for i in input_string.split(',') if i.strip()]
            self.history.extend(new_data)  # เพิ่มข้อมูลใหม่เข้าประวัติศาสตร์
            self.learner.add_data(new_data)  # อัพเดทประวัติศาสตร์ใน learner
            if len(self.history) > 1:  # ต้องการอย่างน้อย 2 ข้อมูลขึ้นไปเพื่อทำนาย
                prediction = self.learner.gen_next_n(self.history[:-1], 1)[-1]  # ใช้ข้อมูลทั้งหมดยกเว้นตัวสุดท้ายเพื่อทำนายตัวสุดท้าย
                self.update_graph(self.history + [prediction])
            else:
                self.update_graph(self.history)  # แสดงกราฟโดยไม่มีการทำนาย
        except Exception as e:
            self.image.set_image('/res:placeholder.png')
            self.container.append(Label(f'Error: {str(e)} Please enter valid numbers.'))

    def update_graph(self, data):
        fig = Figure()
        ax = fig.add_subplot(111)
        ax.plot(data[:-1], 'ro-', label='Original Data')
        ax.plot(len(data) - 1, data[-1], 'bo', label='Prediction')
        ax.legend()
        buffer = BytesIO()
        fig.savefig(buffer, format='png')
        plt.close(fig)
        buffer.seek(0)
        img_str = base64.b64encode(buffer.read()).decode('utf-8')
        self.image.set_image(f'data:image/png;base64,{img_str}')

if __name__ == "__main__":
    start(MyApp, address='0.0.0.0', port=8081, start_browser=True, multiple_instance=True)
