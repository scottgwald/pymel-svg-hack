from pymel.all import *
import sets

mesh_vertices = ls(selection=True)
print len(mesh_vertices)
print mesh_vertices

vertex_set = sets.Set();
print "Initial size of vertex_set " + str(vertex_set.__len__())
vertex_array = [];

for vert_range in mesh_vertices:
	print vert_range
	for vert in vert_range:
		print "Adding vertex " + str(vert) + " to vertex set."
		starting_size = vertex_set.__len__()
		print "starting_size is " + str(starting_size)
		vertex_set.add(vert)
		vertex_array.append(vert)
		if starting_size == vertex_set.__len__():
			print "Looks like vertex " + str(vert) + "was already in the set!!"
		# print vert
		# print "connected vertices: " + vert.connectedVertices()

print "size of vertex set " + str(vertex_set.__len__())
print vertex_set
print "length of vertex array is " + str(len(vertex_array))
print vertex_array

ordered_output_array = []

#first_vertex = vertex_set.pop()
#ordered_output_array.append(first_vertex)

current_vertex = vertex_set.pop()
ordered_output_array.append(current_vertex)

while vertex_set.__len__() > 0:
	neighbors_range = current_vertex.connectedVertices()
	neighbors = []
	for neighbor in neighbors_range:
		neighbors.append(neighbor)
	neighbor_vertex = neighbors.pop()
	while not vertex_set.__contains__(neighbor_vertex):
		neighbor_vertex = neighbors.pop()
	ordered_output_array.append(neighbor_vertex)
	print "Found neighbor " + neighbor_vertex + " of current vertex " + current_vertex + "."
	current_vertex = neighbor_vertex;
	vertex_set.remove(current_vertex)

print ordered_output_array
string_for_mel = ",".join(map(str, ordered_output_array))
print "string for mel is:\n" + string_for_mel

# Algorithm:
# select a vertex (A, the first one), add it to the ordered result list (result_list)
# seek a neighbor (B) that is a member of the vertex set. Add it to the ordered result list, and remove it from the vertex set
# seek a neihbor of B that is a member of the vertex set, and not a member of the ordered result list
# iterate until vertex set is empty

# mel.eval("""

MEL SCRIPT HERE ...

%s

"""
% string_for_mel

)
