import remi.gui as gui
from remi import start, App
import matplotlib.pyplot as plt
import io
import base64
import math
import random
from intern_learner import graph_learner
#เเก้ให้ predict เกิน data เดิม + กดเเล้วกราฟไม่เด้ง
class GraphLearnerGUI(App):
    def __init__(self, *args):
        super(GraphLearnerGUI, self).__init__(*args)
        self.learner = graph_learner()
        self.data_history = []
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
        self.btn_clear = gui.Button('Clear Screen', width=250, height=30)  # Create the clear button
        self.output_area = gui.VBox(width=580, height=600)

        self.btn_process.onclick.do(self.on_button_pressed)
        self.btn_clear.onclick.do(self.clear_screen)  # Set onclick event for the clear button

        container.append(self.lbl_instruction)
        container.append(self.text_area)
        container.append(self.lbl_exclude)
        container.append(self.text_exclude)
        container.append(self.lbl_focus)
        container.append(self.text_focus)
        container.append(self.btn_process)
        container.append(self.btn_clear)  # Add the clear button to the GUI
        container.append(self.output_area)

        return container

    def clear_screen(self, widget):
        """Clears all inputs and outputs on the screen."""
        self.output_area.empty()  # Clear the output area
        self.text_area.set_value('')  # Reset the text area
        self.data_history.clear()  # Optional: Clear any stored data history if applicable

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
            self.update_graph(graph_container, numbers, predicted_next)

    def update_graph(self, graph_container, numbers, predicted_next):
        graph_container.empty()

        plot_url = self.plot_sequence(numbers, predicted_next)
        img = gui.Image(plot_url, width=580, height=200)
        label = gui.Label(f'Predicted next for {numbers}: {predicted_next}')
        
        btn_add_prediction = gui.Button('Add Prediction to Sequence', width=200, height=30)
        btn_randomize = gui.Button('Randomize New Prediction', width=200, height=30)

        graph_container.append(img)
        graph_container.append(label)
        graph_container.append(btn_add_prediction)
        graph_container.append(btn_randomize)

        # Bind events
        btn_add_prediction.onclick.do(self.add_prediction, numbers, predicted_next, graph_container)
        btn_randomize.onclick.do(self.randomize_prediction, numbers, graph_container)
    
    
    
    def randomize_prediction(self, widget, seq, seq_index):
        # สุ่มคำทำนายใหม่ที่มีค่ามากกว่าค่าล่าสุดในลำดับ
        new_prediction = seq[-1] + random.randint(1, 10)  # สุ่มค่าระหว่าง 1 ถึง 10
        # อัปเดตลำดับกับคำทำนายใหม่และแสดงกราฟ
        self.update_graph(seq_index, seq, new_prediction)

    def add_prediction(self, widget, numbers, prediction, graph_container):
        numbers.append(prediction)
        self.update_graph(graph_container, numbers, prediction)

    def plot_sequence(self, sequence, predicted_next):
        plt.figure(figsize=(10, 5))
        plt.plot(sequence + [predicted_next], marker='o', linestyle='-', color='blue')
        plt.plot(len(sequence), predicted_next, marker='o', color='red', linestyle='--')
        for i, value in enumerate(sequence + [predicted_next]):
            plt.text(i, value, str(value), ha='center', va='bottom')
        plt.title("Graph Showing Historical Data and Prediction")
        plt.xlabel("Index of sequence")
        plt.ylabel("Data Value")
        plt.grid(True)
        plt.legend(['Historical Data', 'Predicted Next'])
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)
        data_uri = base64.b64encode(buffer.read()).decode('utf-8')
        img_url = f"data:image/png;base64,{data_uri}"
        return img_url

if __name__ == "__main__":
    start(GraphLearnerGUI, address='0.0.0.0', port=8081, start_browser=True)
