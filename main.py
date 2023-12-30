import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

MAX = 10
INFINITY = 1000

w = [[0] * MAX for _ in range(MAX)]
n_size = 0
p = [0] * MAX

def in_dat():
    global n_size
    st.title("Multi-Stage Graph")

    n_size = st.text_input("Enter the number of nodes", value="2")
    n_size = int(n_size)
    
    for i in range(n_size):
        w[i][i] = 0
        for j in range(i + 1, n_size):
            w[i][j] = st.number_input(f"Enter the weight of edge '{chr(65 + i)}' to '{chr(65 + j)}'", value=0)
            w[j][i] = 0

def dis_dat():
    st.header("The Path Adjacency Matrix")

    # Menggunakan HTML untuk kontrol tata letak
    matrix_html = "<table>"
    for i in range(n_size):
        matrix_html += "<tr>"
        for j in range(n_size):
            matrix_html += f"<td style='padding: 10px;'>{w[i][j]}</td>"
        matrix_html += "</tr>"
    matrix_html += "</table>"

    # Menampilkan matriks menggunakan HTML
    st.write(matrix_html, unsafe_allow_html=True)

def findshort(sr, dst):
    if sr == dst:
        return 0
    else:
        ret = -1
        min_val = INFINITY
        tdst = 0
        for i in range(n_size):
            if w[sr][i] != 0:
                ret = 0
                tdst = w[sr][i] + findshort(i, dst)
                if min_val > tdst:
                    min_val = tdst
                    p[sr] = i
        if ret == -1:
            return INFINITY
        else:
            return min_val
        
def MSG():
    global n_size
    global p
    st.subheader("Find Shortest Path")
    user_input = st.text_input("Enter the source and destination node (e.g., A B): ")
    
    if user_input:
        try:
            s, d = user_input.split()
            si = ord(s.upper()) - 65
            di = ord(d.upper()) - 65
            dist = findshort(si, di)
            if dist >= INFINITY:
                st.error(f"\nThe shortest distance between '{s}' and '{d}' can't be computed")
            else:
                st.success(f"\nThe shortest distance between '{s}' and '{d}': {dist}")

                # Menampilkan shortest path menggunakan HTML
                path_html = f"<p>The shortest path: {s}"
                while si != di:
                    path_html += f" {chr(65 + p[si])}"
                    si = p[si]
                path_html += "</p>"

                # Menampilkan HTML
                st.markdown(path_html, unsafe_allow_html=True)
                st.write("\nProcess complete.")

                # Membuat grafik
                G = nx.Graph()
                for i in range(n_size):
                    for j in range(n_size):
                        if w[i][j] != 0:
                            G.add_edge(chr(65 + i), chr(65 + j), weight=w[i][j])

                # Menentukan posisi node pada grafik
                pos = nx.spring_layout(G)

                # Menambahkan label bobot pada setiap edge
                edge_labels = {(chr(65 + i), chr(65 + j)): w[i][j] for i in range(n_size) for j in range(n_size) if w[i][j] != 0}

                # Menampilkan grafik
                st.pyplot(draw_graph(G, pos, edge_labels))
        except ValueError:
            st.error("Please enter valid source and destination nodes.")
    else:
        st.error("Please enter valid source and destination nodes.")

def draw_graph(G, pos, edge_labels):
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Graph Visualization")
    return plt

if __name__ == "__main__":
    in_dat()
    dis_dat()
    MSG()