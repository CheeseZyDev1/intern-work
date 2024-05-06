import remi.gui as gui
from remi import start, App
import matplotlib.pyplot as plt
import io
import base64
import random
from intern_learner import graph_learner

class GraphLearnerGUI(App):
    def __init__(self, *args):
        super(GraphLearnerGUI, self).__init__(*args)
        self.learner = graph_learner()
        self.graph_containers = {}

    def main(self):
        container = gui.VBox(width=600, height=1000, style={'margin': '0px auto'})
        self.lbl_instruction = gui.Label('Please enter a sequence of numbers, each sequence separated by a new line:')
        self.text_area = gui.TextInput(width=580, height=100, single_line=False, hint='1,2,3,4,5\n7,8,9,10,11')
        self.lbl_exclude = gui.Label('Enter the numbers to exclude, separated by commas (e.g. "3,5"):')
        self.text_exclude = gui.TextInput(width=580, height=30, single_line=True)
        self.lbl_focus = gui.Label('Enter the numbers to focus on, separated by commas (e.g. "2,4"):')
        self.text_focus = gui.TextInput(width=580, height=30, single_line=True)
        self.btn_process = gui.Button('Create a prediction', width=250, height=30)
        self.btn_clear = gui.Button('Clear Screen', width=250, height=30)
        self.output_area = gui.VBox(width=580, height=600)

        self.btn_process.onclick.do(self.on_button_pressed)
        self.btn_clear.onclick.do(self.clear_screen)

        container.append(self.lbl_instruction)
        container.append(self.text_area)
        container.append(self.lbl_exclude)
        container.append(self.text_exclude)
        container.append(self.lbl_focus)
        container.append(self.text_focus)
        container.append(self.btn_process)
        container.append(self.btn_clear)
        container.append(self.output_area)

        return container

    def clear_screen(self, widget):
        self.output_area.empty()
        self.text_area.set_value('')
        self.learner.clear_data()

    def on_button_pressed(self, widget):
        sequences = self.text_area.get_value().split('\n')
        exclude_numbers = list(map(int, self.text_exclude.get_value().split(','))) if self.text_exclude.get_value() else []
        focus_numbers = list(map(int, self.text_focus.get_value().split(','))) if self.text_focus.get_value() else []

        for i, seq in enumerate(sequences):
            numbers = list(map(int, seq.split(',')))
            if exclude_numbers:
                numbers = [n for n in numbers if n not in exclude_numbers]
            if focus_numbers:
                numbers = [n for n in numbers if n in focus_numbers]
            
            self.learner.add_data(numbers)
            predicted_next = self.learner.gen_next_n(numbers, 1)[-1]
            graph_container = gui.VBox(width=580, height=300)
            self.graph_containers[i] = graph_container
            self.output_area.append(graph_container)
            # ส่งข้อมูลเข้าไปในฟังก์ชัน update_graph เพื่อทำการแสดงผลล่าสุดบนกราฟ
            self.update_graph(graph_container, numbers, predicted_next)
            
    #def update_graph(self, graph_container, numbers, predicted_next):
        #graph_container.empty()

        #plot_url = self.plot_sequence(numbers, predicted_next)
        #img = gui.Image(plot_url, width=580, height=200)
        #label = gui.Label(f'Current sequence: {numbers}')

        #btn_add_prediction = gui.Button('Add Prediction to Sequence', width=200, height=30)
        #btn_randomize = gui.Button('Randomize New Prediction', width=200, height=30)
        
        #prediction_buttons = []
        #predictions = [predicted_next, predicted_next - 1, predicted_next + 10]
        #self.selected_predictions = []

        #for idx, pred in enumerate(predictions):
            #btn = gui.Button(f'Choose Prediction {idx + 1}: {pred}', width=200, height=30)
            #btn.onclick.do(self.choose_prediction, numbers, pred, graph_container)
            #prediction_buttons.append(btn)

        #graph_container.append(label)
        #graph_container.append(img)
        #for btn in prediction_buttons:
            #graph_container.append(btn)
        #graph_container.append(btn_add_prediction)
        #graph_container.append(btn_randomize)

        #btn_add_prediction.onclick.do(self.add_predictions, numbers, graph_container)
        #btn_randomize.onclick.do(self.randomize_prediction, numbers, graph_container)

    #def choose_prediction(self, widget, numbers, chosen_prediction, graph_container):
        #if chosen_prediction in self.selected_predictions:
        #    self.selected_predictions.remove(chosen_prediction)
        #    widget.set_text(f'Choose Prediction {numbers.index(chosen_prediction) + 1}: {chosen_prediction}')
         #   widget.set_enabled(True)
         #   widget.style['background-color'] = 'Blue'
        #else:
           # self.selected_predictions.append(chosen_prediction)
            #widget.set_text(f'Selected: {chosen_prediction}')
           # widget.set_enabled(True)
            #widget.style['background-color'] = 'Green'
    
    def update_graph(self, graph_container, numbers, predicted_next):
        graph_container.empty()

        plot_url = self.plot_sequence(numbers, predicted_next)
        img = gui.Image(plot_url, width=580, height=200)
        label = gui.Label(f'Current sequence: {numbers}')

        btn_add_prediction = gui.Button('Add Prediction to Sequence', width=200, height=30)
        btn_randomize = gui.Button('Randomize New Prediction', width=200, height=30)
        
        self.update_predictions(numbers[-1])  # อัปเดตคำทำนายที่สามตามเลขล่าสุด

        prediction_buttons = []
        predictions = [predicted_next, predicted_next - 1, predicted_next + 10]
        self.selected_predictions = []

        for idx, pred in enumerate(predictions):
            selected_text = 'Selected: ' if pred in self.selected_predictions else f'Choose Prediction {idx + 1}: '
            selected_color = 'lightgreen' if pred in self.selected_predictions else ''
            btn = gui.Button(f'{selected_text}{pred}', width=200, height=30)
            btn.style['background-color'] = selected_color
            btn.onclick.do(self.choose_prediction, numbers, pred, graph_container)
            prediction_buttons.append(btn)

        graph_container.append(label)
        graph_container.append(img)
        for btn in prediction_buttons:
            graph_container.append(btn)
        graph_container.append(btn_add_prediction)
        graph_container.append(btn_randomize)

        btn_add_prediction.onclick.do(self.add_predictions, numbers, graph_container)
        btn_randomize.onclick.do(self.randomize_prediction, numbers, graph_container)

    def update_predictions(self, last_number):
        self.predictions = [last_number + 1, last_number - 1, last_number + 10]

    
    def choose_prediction(self, widget, numbers, chosen_prediction, graph_container):
        # Toggle the selection state of the prediction
        if chosen_prediction in self.selected_predictions:
            self.selected_predictions.remove(chosen_prediction)
            widget.set_text(f'Choose Prediction: {chosen_prediction}')  # Update the button text to show it's deselected
            widget.style['background-color'] = ''  # Reset button color to default
        else:
            self.selected_predictions.append(chosen_prediction)
            widget.set_text(f'Selected: {chosen_prediction}')  # Update the button text to show it's selected
            widget.style['background-color'] = 'lightgreen'  # Highlight button


    def add_predictions(self, widget, numbers, graph_container):
        for pred in self.selected_predictions:
            numbers.append(pred)
        self.update_graph(graph_container, numbers, numbers[-1])
        self.selected_predictions = []
    
    def update_selected_predictions(self, chosen_prediction):
        if chosen_prediction in self.selected_predictions:
            self.selected_predictions.remove(chosen_prediction)
        else:
            self.selected_predictions.append(chosen_prediction)
        
        
    def randomize_prediction(self, widget, numbers, graph_container):
        # Example of more contextual randomization
        range_start = numbers[-1] + 1
        range_end = numbers[-1] + 10
        new_prediction = random.randint(range_start, range_end)
        # Update graph and possibly refresh the available choices
        self.update_graph(graph_container, numbers, new_prediction)

    def add_prediction(self, widget, numbers, prediction, graph_container):
        numbers.append(prediction)
        self.update_graph(graph_container, numbers, prediction)  # อัปเดตกราฟด้วยข้อมูลใหม่

    def plot_sequence(self, sequence, predicted_next):
        plt.figure(figsize=(10, 5))
        plt.plot(range(len(sequence)), sequence, marker='o', linestyle='-', color='blue')
        predictions = [predicted_next, predicted_next * 2, predicted_next + 10]  # ตัวอย่างของการทำนายสามารถปรับเปลี่ยนตามความต้องการ
        for i, pred in enumerate(predictions):
            plt.plot(len(sequence), pred, marker='o', color=['red', 'green', 'orange'][i], linestyle='--')
            plt.text(len(sequence), pred, str(pred), ha='center', va='bottom')
        plt.title("Graph Showing Historical Data and Multiple Predictions")
        plt.xlabel("Index of sequence")
        plt.ylabel("Data Value")
        plt.grid(True)
        plt.legend(['Historical Data'] + [f'Prediction {i+1}' for i in range(len(predictions))])
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)
        data_uri = base64.b64encode(buffer.read()).decode('utf-8')
        img_url = f"data:image/png;base64,{data_uri}"
        return img_url


if __name__ == "__main__":
    start(GraphLearnerGUI, address='0.0.0.0', port=8081, start_browser=True)
