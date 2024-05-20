import remi.gui as gui
from remi import start, App
import matplotlib.pyplot as plt
import io
import base64
from intern_learner import graph_learner

class GraphLearnerGUI(App):
    def __init__(self, *args):
        super(GraphLearnerGUI, self).__init__(*args)
        self.learner = graph_learner()
        self.graph_containers = {}
        self.selected_predictions = []
        self.level = 0
        self.current_numbers = []
        self.predictions = []
        self.add_to_history_button = None
        self.graph_container = None

    def main(self):
        container = gui.VBox(width=800, height=1200, style={'margin': '0px auto', 'padding': '20px', 'font-family': 'Arial, sans-serif', 'background-color': '#f5f5f5', 'border-radius': '10px'})
        self.lbl_instruction = gui.Label('Please enter a sequence of numbers, each sequence separated by a new line:', style={'font-size': '16px', 'margin-bottom': '10px'})
        self.text_area = gui.TextInput(width=760, height=100, single_line=False, hint='1,2,3,4,5\n7,8,9,10,11', style={'margin-bottom': '10px', 'padding': '10px', 'font-size': '14px'})
        self.lbl_exclude = gui.Label('Enter the numbers to exclude, separated by commas (e.g. "3,5"):', style={'font-size': '16px', 'margin-bottom': '10px'})
        self.text_exclude = gui.TextInput(width=760, height=30, single_line=True, style={'margin-bottom': '10px', 'padding': '10px', 'font-size': '14px'})
        self.lbl_focus = gui.Label('Enter the numbers to focus on, separated by commas (e.g. "2,4"):', style={'font-size': '16px', 'margin-bottom': '10px'})
        self.text_focus = gui.TextInput(width=760, height=30, single_line=True, style={'margin-bottom': '10px', 'padding': '10px', 'font-size': '14px'})
        self.btn_process = gui.Button('Create a prediction', width=250, height=40, style={'margin': '10px', 'background-color': '#4CAF50', 'color': 'white', 'font-size': '16px', 'border': 'none', 'border-radius': '5px', 'cursor': 'pointer'})
        self.btn_clear = gui.Button('Clear Screen', width=250, height=40, style={'margin': '10px', 'background-color': '#f44336', 'color': 'white', 'font-size': '16px', 'border': 'none', 'border-radius': '5px', 'cursor': 'pointer'})
        self.output_area = gui.VBox(width=760, height=600, style={'margin-top': '20px', 'padding': '10px', 'background-color': 'white', 'border-radius': '10px', 'box-shadow': '0 0 10px rgba(0,0,0,0.1)'})
        self.history_area = gui.VBox(width=760, height=200, style={'margin-top': '20px', 'padding': '10px', 'background-color': 'white', 'border-radius': '10px', 'box-shadow': '0 0 10px rgba(0,0,0,0.1)'})

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
        container.append(gui.Label('History', style={'font-size': '18px', 'margin-top': '20px'}))
        container.append(self.history_area)

        return container

    def clear_screen(self, widget):
        self.output_area.empty()
        self.text_area.set_value('')
        self.learner.clear_data()
        self.selected_predictions = []
        self.level = 0
        self.current_numbers = []
        self.predictions = []
        self.add_to_history_button = None
        self.graph_container = None

    def on_button_pressed(self, widget):
        self.output_area.empty()
        sequences = self.text_area.get_value().split('\n')
        exclude_numbers = [int(num) for num in self.text_exclude.get_value().split(',') if num] if self.text_exclude.get_value() else []
        focus_numbers = [int(num) for num in self.text_focus.get_value().split(',') if num] if self.text_focus.get_value() else []

        for seq in sequences:
            numbers = [int(num) for num in seq.split(',') if num.strip()]
            numbers = [n for n in numbers if not exclude_numbers or n not in exclude_numbers]
            numbers = [n for n in numbers if not focus_numbers or n in focus_numbers]

            self.learner.add_data(numbers)
            self.current_numbers = numbers
            self.predictions = self.learner.gen_next_n(numbers, 3)  # Generate 3 predictions initially
            if not self.graph_container:
                self.graph_container = gui.VBox(width=760, height=400, style={'margin-top': '20px'})
                self.output_area.append(self.graph_container)
            self.update_graph(self.graph_container, numbers, self.predictions, 0)

    def update_graph(self, graph_container, numbers, predictions, level=0):
        if 'img' not in graph_container.children or 'label' not in graph_container.children:
            img = gui.Image('', width=740, height=300, style={'margin-bottom': '10px'})
            label = gui.Label('', style={'font-size': '16px', 'margin-bottom': '10px'})
            graph_container.append(label, key='label')
            graph_container.append(img, key='img')

        new_predictions = {i: p for i, p in enumerate(predictions[:3], start=1)}  # Limit to 3 predictions
        self.plot_sequence(numbers, new_predictions, level, graph_container)
        graph_container.children['label'].set_text(f'Current sequence: {numbers}')

        prediction_buttons = gui.HBox(style={'justify-content': 'center', 'margin-top': '10px'})
        for i, pred in new_predictions.items():
            btn = gui.Button(f'Choose Prediction {i}: {pred}', width=200, height=40, style={'margin': '5px', 'background-color': '#2196F3', 'color': 'white', 'font-size': '14px', 'border': 'none', 'border-radius': '5px', 'cursor': 'pointer'})
            btn.onclick.do(self.choose_prediction, graph_container, numbers, new_predictions, pred, i, level + 1, btn)
            prediction_buttons.append(btn, key=f'button_{i}')

        graph_container.append(prediction_buttons, key='prediction_buttons')

        if self.add_to_history_button is None:
            self.add_to_history_button = gui.Button('Add to Sequence', width=250, height=40, style={'margin-top': '10px', 'background-color': '#2196F3', 'color': 'white', 'font-size': '16px', 'border': 'none', 'border-radius': '5px', 'cursor': 'pointer'})
            self.add_to_history_button.onclick.do(self.add_to_sequence)
            self.output_area.append(self.add_to_history_button)

    def choose_prediction(self, widget, graph_container, numbers, predictions, chosen_prediction, prediction_idx, level, button):
        if chosen_prediction in self.selected_predictions:
            self.selected_predictions.remove(chosen_prediction)
            button.set_text(f'Choose Prediction {prediction_idx}: {chosen_prediction}')
            button.set_style({'background-color': '#2196F3', 'color': 'white'})
        else:
            self.selected_predictions.append(chosen_prediction)
            button.set_text(f'Selected Prediction {prediction_idx}: {chosen_prediction}')
            button.set_style({'background-color': 'lightgreen', 'color': 'black'})

        self.update_branch_graph(graph_container, numbers, predictions, self.selected_predictions, level)

    def update_branch_graph(self, graph_container, numbers, predictions, selected_predictions, level):
        plt.figure(figsize=(10, 5))
        x_values = list(range(1, len(numbers) + 2))  # Add one extra for the space between

        # Plot historical data
        plt.plot(x_values[:-1], numbers, marker='o', linestyle='-', color='blue', label='Historical Data')

        # Plot zero line
        plt.axvline(x=len(numbers), color='black', linestyle='-')
        plt.xticks(list(range(1, len(numbers) + 2)), list(range(1, len(numbers) + 1)) + [0])

        # Plot predictions
        colors = ['red', 'green', 'orange']
        for i, (pred_idx, pred) in enumerate(predictions.items()):
            if pred in selected_predictions:
                plt.plot([len(numbers), len(numbers) + 1], [numbers[-1], pred], marker='o', color=colors[pred_idx % len(colors)], linestyle='--', label=f'Prediction {pred_idx+1}')
            else:
                plt.plot([len(numbers) + 1], [pred], marker='o', color=colors[pred_idx % len(colors)], linestyle='--', label=f'Prediction {pred_idx+1}')
            plt.text(len(numbers) + 1, pred, f'{pred}', ha='center', va='bottom', color=colors[pred_idx % len(colors)])

        for i, num in enumerate(numbers):
            plt.text(x_values[i], num, f'{num}', ha='center', va='bottom', color='blue')

        plt.title("Graph Showing Historical Data and Predictions")
        plt.xlabel("Index of sequence")
        plt.ylabel("Value")
        plt.grid(True)
        plt.legend()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)
        data_uri = base64.b64encode(buffer.read()).decode('utf-8')
        img_url = f"data:image/png;base64,{data_uri}"
        graph_container.children['img'].attributes['src'] = img_url

    def plot_sequence(self, sequence, predictions, level, graph_container):
        plt.figure(figsize=(10, 5))
        x_values = list(range(1, len(sequence) + 2))  # Add one extra for the space between

        plt.plot(x_values[:-1], sequence, marker='o', linestyle='-', color='blue', label='Historical Data')

        # Plot zero line
        plt.axvline(x=len(sequence), color='black', linestyle='-')
        plt.xticks(list(range(1, len(sequence) + 2)), list(range(1, len(sequence) + 1)) + [0])

        colors = ['red', 'green', 'orange']
        for i, (idx, pred) in enumerate(predictions.items(), start=1):
            plt.plot([len(sequence) + 1], [pred], marker='o', color=colors[i % len(colors)], linestyle='--', label=f'Prediction {idx}')
            plt.text(len(sequence) + 1, pred, f'{pred}', ha='center', va='bottom', color=colors[i % len(colors)])

        for i, num in enumerate(sequence):
            plt.text(x_values[i], num, f'{num}', ha='center', va='bottom', color='blue')

        plt.title("Graph Showing Historical Data and Predictions")
        plt.xlabel("Index of sequence")
        plt.ylabel("Value")
        plt.grid(True)
        plt.legend()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)
        data_uri = base64.b64encode(buffer.read()).decode('utf-8')
        img_url = f"data:image/png;base64,{data_uri}"
        graph_container.children['img'].attributes['src'] = img_url

    def add_to_sequence(self, widget):
        if self.selected_predictions:
            history_entry = f"Round {self.level + 1}: Added {self.selected_predictions}"
            self.history_area.append(gui.Label(history_entry, style={'font-size': '14px', 'margin-bottom': '5px', 'color': '#333'}))
            
            self.current_numbers.extend(self.selected_predictions)
            self.selected_predictions = []
            self.level += 1

            new_predictions = self.learner.gen_next_n(self.current_numbers, 3)  # Generate new predictions
            self.update_graph(self.graph_container, self.current_numbers, new_predictions, self.level)  # Update graph with new data

if __name__ == "__main__":
    start(GraphLearnerGUI, address='0.0.0.0', port=8081, start_browser=True)
