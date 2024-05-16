import remi.gui as gui
from remi import start, App
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
import base64

class PredictionTreeApp(App):
    def __init__(self, *args):
        super(PredictionTreeApp, self).__init__(*args)

    def main(self):
        container = gui.VBox(width=600, height=600, style={'margin': '0px auto'})

        self.input_text = gui.TextInput(width=200, height=30, hint='Enter initial value')
        self.submit_btn = gui.Button('Generate Prediction Tree', width=200, height=30)
        self.submit_btn.onclick.do(self.generate_tree)

        self.image = gui.Image('/res:placeholder.png', width=580, height=450)

        container.append(self.input_text)
        container.append(self.submit_btn)
        container.append(self.image)

        return container

    def generate_tree(self, widget):
        try:
            initial_value = int(self.input_text.get_value())
            img_url = self.plot_prediction_tree(initial_value)
            self.image.set_image(img_url)
        except Exception as e:
            self.image.set_image('/res:error.png')

    def plot_prediction_tree(self, initial_value):
        G = nx.DiGraph()
        root = initial_value
        predictions = [root + 1, root - 1, root * 2]
        for pred in predictions:
            G.add_edge(root, pred)
        
        pos = nx.spring_layout(G)
        plt.figure(figsize=(10, 8))
        nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=2000, font_size=12)
        
        img = BytesIO()
        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)
        return 'data:image/png;base64,' + base64.b64encode(img.read()).decode('utf-8')

if __name__ == "__main__":
    start(PredictionTreeApp, address='0.0.0.0', port=8080, multiple_instance=True, enable_file_cache=True, update_interval=0.1, start_browser=True)
