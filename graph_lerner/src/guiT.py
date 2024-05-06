import remi.gui as gui
from remi import start, App

class SequencePredictorApp(App):
    def __init__(self, *args):
        super(SequencePredictorApp, self).__init__(*args)

    def main(self):
        container = gui.VBox(width=600, height=400)
        
        # Input fields for sequences
        self.input_sequence = gui.TextInput(width=200, height=30, placeholder='Enter sequence here')
        
        # Buttons for actions
        predict_btn = gui.Button('Predict', width=200, height=30)
        predict_btn.onclick.do(self.on_predict_clicked)
        
        new_predict_btn = gui.Button('New Prediction', width=200, height=30)
        clear_data_btn = gui.Button('Clear Data', width=200, height=30)
        clear_data_btn.onclick.do(self.on_clear_data_clicked)
        
        # Label for sequence display
        self.label_sequence = gui.Label('', width=200, height=30)
        
        # Assemble the widgets
        container.append(self.input_sequence)
        container.append(predict_btn)
        container.append(new_predict_btn)
        container.append(clear_data_btn)
        container.append(self.label_sequence)
        
        # Placeholder for the graph
        # In a real application, you would integrate with a plotting library
        self.graph_placeholder = gui.Label('Graph will be here')
        container.append(self.graph_placeholder)
        
        return container

    def on_predict_clicked(self, widget):
        # Here we get the text from the input field
        input_sequence = self.input_sequence.get_text()
        # You can now use this input sequence to do whatever processing you need
        # For example:
        # predicted_sequence = your_predict_function(input_sequence)
        # self.label_sequence.set_text(str(predicted_sequence))
        self.label_sequence.set_text('Received input: ' + input_sequence)

    def on_clear_data_clicked(self, widget):
        self.input_sequence.set_text('')
        self.label_sequence.set_text('')
    def update_graph(self, data):
        fig = Figure()
        ax = fig.add_subplot(111)
        ax.plot(data[:-1], 'ro-', label='Original Data')
        ax.plot(len(data) - 1, data[-1], 'bo', label='Prediction')
        ax.legend()
        
        for i, txt in enumerate(data[:-1]):
            ax.annotate(txt, (i, data[i]))
        ax.annotate(f'Prediction: {data[-1]}', (len(data) - 1, data[-1]), textcoords="offset points", xytext=(0,10), ha='center') 
        
        # Include a legend within the plot
        ax.legend()

        # Place a text label outside the graph area for the prediction
        prediction_text = f'Prediction: {data[-1]:.2f}'
        fig.text(0.5, 0.01, prediction_text, ha='center', va='bottom', fontsize='large')

        buffer = BytesIO()
        fig.savefig(buffer, format='png')
        plt.close(fig)
        buffer.seek(0)
        img_str = base64.b64encode(buffer.read()).decode('utf-8')
        self.graph_image.set_image(f'data:image/png;base64,{img_str}')  # Make sure this widget name matches your REMI image widget

    
    
# Starts the web server
start(SequencePredictorApp, address='0.0.0.0', port=8080, start_browser=True)
