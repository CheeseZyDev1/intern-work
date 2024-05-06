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
        self.learner = gln()
        self.data = []

    def main(self):
        self.container = VBox(width='100%', style={'align-items': 'center', 'justify-content': 'center', 'margin': 'auto', 'max-width': '800px', 'padding': '20px'})
        self.input_text = TextInput(width='80%', style={'padding': '10px', 'font-size': '16px', 'margin-bottom': '15px'})
        self.plot_button = Button('Plot and Predict', width='200px', height='50px', style={'font-size': '16px', 'margin': '10px'})
        self.plot_button.onclick.do(self.on_plot_and_predict)
        self.graph_container = VBox(width='100%', style={'text-align': 'center', 'margin-top': '20px'})
        self.image = Image('/res:placeholder.png', width=500, height=300)
        self.graph_container.append(self.image)

        # Add a clear button
        self.clear_button = Button('Clear', width='200px', height='50px', style={'font-size': '16px', 'margin': '10px'})
        self.clear_button.onclick.do(self.on_clear)

        # Add a new prediction button
        self.new_prediction_button = Button('New Prediction', width='200px', height='50px', style={'font-size': '16px', 'margin': '10px'})
        self.new_prediction_button.onclick.do(self.on_new_prediction)

        # Assemble the GUI
        self.container.append(self.input_text)
        self.container.append(self.plot_button)
        self.container.append(self.graph_container)
        self.container.append(self.clear_button)
        self.container.append(self.new_prediction_button)
        
        return self.container

    def on_clear(self, widget):
        # Clear the input text
        self.input_text.set_value('')

        # Clear the graph container image or replace with a placeholder
        self.image.set_image('/res:placeholder.png')

        # Optionally, reset the data and learner's state if needed
        self.data = []
        # You need to implement the reset method in your graph_learner class
        # self.learner.reset() # Assuming there's a reset method in your graph_learner class
    def on_new_prediction(self, widget):
        # Clear the graph container image or replace with a placeholder
        self.image.set_image('/res:placeholder.png')

        # Optionally, reset the data and learner's state if needed
        self.data = []
        # self.learner.reset() # Assuming there's a reset method in your graph_learner class
    def on_plot_and_predict(self, widget):
        input_string = self.input_text.get_value()
        try:
            # Parse input data and update the learner's history
            new_data = [float(i) for i in input_string.split(',') if i.strip().replace('.', '', 1).isdigit()]
            self.learner.add_data(new_data)

            # Predict the next value using the graph_learner
            prediction = self.learner.gen_next_n(new_data, 1)[-1]

            # Plot both the original data and the prediction
            self.update_graph(new_data + [prediction])
        except ValueError:
            self.graph_container.empty()
            self.graph_container.append(Label('Please enter valid numbers separated by commas.'))

    def update_graph(self, data):
        fig = Figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(data[:-1], 'ro-', label='Original Data')

        # Plot the prediction as a blue dot
        ax.plot(len(data) - 1, data[-1], 'bo', label='Prediction')

        # Annotate each point with its value
        for i, txt in enumerate(data[:-1]):
            ax.annotate(txt, (i, data[i]))
        ax.annotate(f'Prediction: {data[-1]}', (len(data) - 1, data[-1]), textcoords="offset points", xytext=(0,10), ha='center') 
        # Include a legend within the plot
        ax.legend()

        # Place a text label outside the graph area for the prediction
        prediction_text = f'Prediction: {data[-1]:.2f}'
        fig.text(0.5, 0.01, prediction_text, ha='center', va='bottom', fontsize='large')

        # Convert plot to PNG image
        buffer = BytesIO()
        fig.savefig(buffer, format='png')
        plt.close(fig)
        buffer.seek(0)
        img_str = base64.b64encode(buffer.read()).decode('utf-8')
        self.image.set_image(f'data:image/png;base64,{img_str}')

# Start the application
if __name__ == "__main__":
    start(MyApp, address='0.0.0.0', port=8081, start_browser=True, multiple_instance=True)
