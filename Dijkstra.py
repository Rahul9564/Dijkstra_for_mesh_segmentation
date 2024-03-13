#!/usr/bin/env python
# coding: utf-8

# In[3]:


import trimesh
import networkx as nx
import numpy as np
#from mayavi import mlab
import os
os.environ['ETS_TOOLKIT'] = 'qt5' 


def load_mesh(file_path):
    return trimesh.load(file_path)

def mesh_to_graph(mesh):
    # Extract vertices and faces from the mesh
    vertices = mesh.vertices
    faces = mesh.faces

    # Create a graph from vertices and faces
    graph = nx.Graph()

    # Add vertices to the graph
    for i, vertex in enumerate(vertices):
        graph.add_node(i, pos=(vertex[0], vertex[1], vertex[2]))

    # Add edges to the graph based on the mesh faces
    for face in faces:
        graph.add_edge(face[0], face[1], weight=1)
        graph.add_edge(face[1], face[2], weight=1)
        graph.add_edge(face[2], face[0], weight=1)

    return graph

def dijkstra_shortest_path(graph, start_node, end_node):
    try:
        path = nx.shortest_path(graph, source=start_node, target=end_node, weight='weight')
        return path
    except nx.NetworkXNoPath:
        return None

# Example usage
file_path = '/data/home/user_rs/rahul22CS91F02/scan_046.obj'  # Replace with the path to your mesh file
mesh = load_mesh(file_path)

# Convert the mesh to a graph
graph = mesh_to_graph(mesh)
print(graph)
vertices = mesh.vertices

given_nodes = []
#given vertices
given_vert = ([ -44.9838, 53.37507, -14.29581 ],
              [ -21.65583, 65.84303, 12.7275 ],
              [ 2.776328, 62.87806, -7.086862 ],
              [ 24.89668, 60.23461, 5.530046 ],
              [ 23.20444, 2.602311, 33.34484 ],
              [ -43.62744, -19.65581, -11.93513 ],
              [ 14.4169, -114.1634, -48.76259 ])

#finding the vertex number of given vertices
for j in range(len(given_vert)):
    for i in range(len(vertices)):
        if int(given_vert[j][0]) == int(vertices[i][0]) and int(given_vert[j][1]) == int(vertices[i][1]) and int(given_vert[j][2]) == int(vertices[i][2]):
            given_nodes.append(i)
            break
                
print(given_nodes)
cluster_assignments = {}


#clustering each vertices
for i in range(len(mesh.vertices)):
    start_node = i
    path = 99999
    for j in range(len(given_nodes)):
        end_node = given_nodes[j]
        shortest_path = dijkstra_shortest_path(graph, start_node, end_node)
        if (i%5000==0):
            print(i)
            print(j)
        if len(shortest_path) < path:
            cluster_assignments[i] = j
            path = len(shortest_path)
            
            
#storing the vertices according to their cluster and also storing the labels
vert = []
lbl = []
for cluster_id in range(len(set(cluster_assignments.values()))):
    cluster_vertices = []
    # Get the vertices in the cluster
    cluster_vertices = [vertices[i] for i in range(len(vertices)) if cluster_assignments[i] == cluster_id]
    for i in range(len(cluster_vertices)):
          lbl.append(cluster_id)
    vert.append(cluster_vertices)
    
    
    
#saving the labels in text format
with open('/data/home/user_rs/rahul22CS91F02/others/labels.txt', 'w') as f:
      for item in lbl:
        f.write("%s\n" % item)
        
#saving the vertices
with open('/data/home/user_rs/rahul22CS91F02/others/vertices.txt', 'w') as f:
    for i in range(len(vert)):
        for j in range(len(vert[i])):
            f.write(f'{vert[i][j][0]} {vert[i][j][1]} {vert[i][j][2]}\n')
# # Choose start and end vertices (nodes) for the path
# start_node = 0
# end_node = len(mesh.vertices) - 1

# Find the shortest path using Dijkstra's algorithm
# shortest_path = dijkstra_shortest_path(graph, start_node, end_node)
####print(cluster_assignments)
# Create a Mayavi scene
#mlab.figure(bgcolor=(1, 1, 1), fgcolor=(0, 0, 0), size=(800, 600))

# Plot the 3D mesh
#mesh_actor = mlab.triangular_mesh(mesh.vertices[:, 0], mesh.vertices[:, 1], mesh.vertices[:, 2], mesh.faces, color=(0.7, 0.7, 0.7), opacity=0.5)

# Highlight the shortest path
# if shortest_path:
#     path_vertices = np.array([graph.nodes[node]['pos'] for node in shortest_path])
#     mlab.points3d(path_vertices[:, 0], path_vertices[:, 1], path_vertices[:, 2], color=(1, 0, 0), scale_factor=0.1)

# Show the Mayavi scene
#mlab.show()

# Create a new mesh for each cluster
# segmented_meshes = []
# vertices = mesh.vertices
# for cluster_id in range(len(set(cluster_assignments.values()))):
#     # Get the vertices in the cluster
#     cluster_vertices = [vertices[i] for i in range(len(vertices)) if cluster_assignments[i] == cluster_id]
#     #print(cluster_vertices)
#     #print((set(cluster_assignments.values())))
# #     chosen_faces = []
# #     for face in mesh.faces:
# #         #if np.all(vertex_index in cluster_vertices for vertex_index in face):
# #         if np.all(np.isin(face, cluster_vertices)):
# #             chosen_faces.append(face)
#     #print(cluster_vertices)
# #     print('Rahul')
# #     print(cluster_vertices)
# #     print('Barman')
#     # Create a new mesh from the cluster vertices
#     segmented_mesh = trimesh.Trimesh(vertices=cluster_vertices, faces=chosen_faces)

#     # Add the new mesh to the list of segmented meshes
#     segmented_meshes.append(segmented_mesh)
#     print(segmented_meshes)

# # Save the segmented meshes
# for i, segmented_mesh in enumerate(segmented_meshes):
#     segmented_mesh.export('/data/home/user_rs/rahul22CS91F02/others/segmented_mesh_{}.obj'.format(i))



