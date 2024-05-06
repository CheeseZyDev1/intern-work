import matplotlib.pyplot as plt
import networkx as nx

# สร้างกราฟ
G = nx.DiGraph()  # ใช้ DiGraph เพื่อแสดงทิศทาง

# เพิ่มโหนดสำหรับข้อมูลที่ผู้ใช้ป้อน
user_data = [1, 2, 3]
user_pos = {1: (-3, 0), 2: (-2, 0), 3: (-1, 0)}
G.add_nodes_from(user_data)

# เพิ่มโหนดสำหรับการทำนาย
predictions = ['A', 'B', 'C']
pred_pos = {'A': (1, 1), 'B': (1, 0), 'C': (1, -1)}
G.add_nodes_from(predictions)

# กำหนดตำแหน่งโหนด
pos = {**user_pos, **pred_pos}

# เชื่อมโยงข้อมูลผู้ใช้กับการทำนาย
for pred in predictions:
    G.add_edge(3, pred)  # เชื่อมโยงจากโหนดสุดท้ายของข้อมูลผู้ใช้ไปยังการทำนาย

# วาดโหนด
nx.draw_networkx_nodes(G, pos, nodelist=user_data, node_color='blue', node_size=500)
nx.draw_networkx_nodes(G, pos, nodelist=predictions, node_color='red', node_size=500)

# วาดเส้นเชื่อม
nx.draw_networkx_edges(G, pos)

# วาดป้ายชื่อ
labels = {node: node for node in user_data}
labels.update({node: f'Prediction {node}' for node in predictions})
nx.draw_networkx_labels(G, pos, labels)

# ซ่อนแกน
plt.axis('off')

# แสดงผล
plt.show()
