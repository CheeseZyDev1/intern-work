import remi.gui as gui
from remi import start, App

class MyApplication(App):
    def __init__(self, *args):
        super(MyApplication, self).__init__(*args)

    def main(self):
        container = gui.VBox(width=600, height=450)

        # Input Sequence
        input_sequence_label = gui.Label('Input Sequence:', width='80%', height='30px')
        self.input_sequence = gui.TextInput(width='80%', height='30px')
        self.input_sequence.set_value('1,8,9,6,82')
        
        prediction_button = gui.Button('Prediction', width='80%', height='30px')
        clear_data_button = gui.Button('Clear Data', width='80%', height='30px')

        prediction_button.onclick.do(self.on_prediction_button_pressed)
        clear_data_button.onclick.do(self.on_clear_data_button_pressed)
        
        # Label Sequence
        label_sequence_label = gui.Label('Label Sequence:', width='80%', height='30px')
        self.label_sequence = gui.TextInput(width='80%', height='30px')
        self.label_sequence.set_value('1,8,6,865,7')
        
        # Graph Placeholder - In REMI you would integrate with a library that supports graphing, or use custom HTML
        self.graph = gui.Label('Graph will be displayed here.', width='100%', height='200px')
        self.graph.style['border'] = '1px solid black'
        
        # Arrange widgets in the container
        container.append(input_sequence_label)
        container.append(self.input_sequence)
        container.append(prediction_button)
        container.append(clear_data_button)
        container.append(label_sequence_label)
        container.append(self.label_sequence)
        container.append(self.graph)
        
        return container
    
    def on_prediction_button_pressed(self, widget):
        self.graph.set_text('Predicted data will be displayed here.')

    def on_clear_data_button_pressed(self, widget):
        self.input_sequence.set_value('')
        self.label_sequence.set_value('')
        self.graph.set_text('Graph cleared.')

# starts the webserver
start(MyApplication, address='0.0.0.0', port=8080, start_browser=True)
