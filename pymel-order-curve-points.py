from pymel.all import *
import sets
import os
from os.path import expanduser
import subprocess

# config variables

#IMPORTANT: ADJUST REPO_REL_PATH TO PUT OUTPUT FILES IN THE RIGHT PLACE

repo_rel_path = os.path.join("mygit","pymel-svg-hack") # path from user home folder
point_order_file = os.path.join("data", "ordered-mouth-points.dat")

home = expanduser("~")
repo_full_path = os.path.join( home, repo_rel_path )
point_order_file_full_path = os.path.join( repo_full_path, point_order_file )
generate_pdf_full_path = os.path.join( repo_full_path, "bin", "generate-pdfs" )

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
string_for_mel = "{\"" + "\",\"".join(map(str, ordered_output_array)) + "\"}"
print "string for mel is:\n" + string_for_mel
print os.getcwd()
print point_order_file_full_path

string_for_file = "\n".join(map(str, ordered_output_array))+"\n"

# f = open( point_order_file_full_path, 'w' )
filename = point_order_file_full_path
dir = os.path.dirname(filename)
if not os.path.exists(dir):
    os.makedirs(dir)
with open(filename, 'w') as f:
  print "writing point order to " + filename
  f.write(string_for_file)

# Algorithm:
# select a vertex (A, the first one), add it to the ordered result list (result_list)
# seek a neighbor (B) that is a member of the vertex set. Add it to the ordered result list, and remove it from the vertex set
# seek a neihbor of B that is a member of the vertex set, and not a member of the ordered result list
# iterate until vertex set is empty

# mel.eval("""

# MEL SCRIPT HERE ...

# %s

# """
# % string_for_mel

# )

mel_screenSpace="""
// Get a matrix
proc matrix screenSpaceGetMatrix(string $attr){
  float $v[]=`getAttr $attr`;
  matrix $mat[4][4]=<<$v[0], $v[1], $v[2], $v[3];
             $v[4], $v[5], $v[6], $v[7];
             $v[8], $v[9], $v[10], $v[11];
             $v[12], $v[13], $v[14], $v[15]>>;
 return $mat;
}

// Multiply the vector v by the 4x4 matrix m, this is probably
// already in mel but I cant find it.
proc vector screenSpaceVecMult(vector $v, matrix $m){
  matrix $v1[1][4]=<<$v.x, $v.y, $v.z, 1>>;
  matrix $v2[1][4]=$v1*$m;
  return <<$v2[0][0], $v2[0][1],  $v2[0][2]>>;
};

global proc int screenSpace(string $sCam)
{
  string $folderPath = "/Users/scottgwald/mygit/pymel-svg-hack/data/";
  // get the currently selected point
  string $dumpList[] = %s;
  // string $dumpList[] = {"Head_MeshShape.vtx[5486]", "Head_MeshShape.vtx[1865]", "Head_MeshShape.vtx[1864]"};
  // string $dumpList[] = `ls -sl`;
  int $argc = size($dumpList);

  // string orderedListFromPython = [Head_MeshShape.vtx[1723],Head_MeshShape.vtx...]

  // if ($argc != 1)
  // {
  //   confirmDialog -t "screenSpace Usage" -m "Select a point or a single object to use";
  //   return -1;
  // }

  // string $name = $dumpList[0];
  // string $pointWsFile=`fileDialog -m 1 -dfn ($name+".xml") -dm "*.xml"`;
  // print ("Well-formated file name: " + $pointWsFile + "\\n"); 
  // example /Users/LiliVanili/svghacking/testes-0943.xml

  print ("There are " + $argc + " points selected.\\n");
  int $f;
  for ($f=0;$f<=($argc-1);$f++) {
    string $name = $dumpList[$f];
    string $dumpPt = $name;
    print ("Point number " + $f + ". Name is " + $name + ".\\n");

    int $camW = `getAttr defaultResolution.width`;
    int $camH = `getAttr defaultResolution.height`;
    float $dar = `getAttr defaultResolution.deviceAspectRatio`;
    float $car = `camera -q -ar $sCam`;
    float $chfv = `getAttr ($sCam+"Shape.horizontalFilmAperture")`;
    if ($car != $dar) {
      setAttr ($sCam+"Shape.verticalFilmAperture") ($chfv/$dar);
    }

    // Find the frame range
    float $fs = `playbackOptions -q -min`;
    float $fe = `playbackOptions -q -max`;
    string $verify = "Will create tracking data for " + $name + "\\n" +
                     "For the frame range of " + $fs + "-" + $fe + "\\n" +
                     "The camera used will be "+$sCam+"\\nResolution:"+$camW+"x"+$camH+"\\n";

    // if (`confirmDialog -t "screenSpace Verify" -m $verify -b "Dump" -b "Cancel"` == "Cancel")
    //   return -2;

    print ("Dumping selection...\\n");

    // //string $pointWsFile = $name+"_screenSpace.txt";
    // string $pointWsFile = `fileDialog -m 1 -dfn ($name+".xml") -dm "*.xml"`;
    // print ("Well-formated file name: " + $pointWsFile + "\\n");

    string $pointWsFile = $folderPath + $name + ".xml";
    print ("Trying to open file: " + $pointWsFile +".\\n");

    int $outFileId = fopen($pointWsFile,"w");

    if ($outFileId == 0) {
      print ("Could not open output file " + $pointWsFile);
      return -1;
    }

    string $line;

    int $f;
    float $tx[],$ty[],$tz[];
    for ($f=$fs;$f<=$fe;$f++)
    {
      currentTime $f;

      // get world space position of the point and make a vector
      float $ptPosWs[] = `xform -q -ws -t $dumpPt`;
      vector $ptVecWs = <<$ptPosWs[0],$ptPosWs[1],$ptPosWs[2]>>;

      // Grab the worldInverseMatrix from cam
      matrix $cam_mat[4][4] = screenSpaceGetMatrix($sCam+".worldInverseMatrix");

      // Multiply the point by that matrix
      vector $ptVecCs = screenSpaceVecMult($ptVecWs,$cam_mat);

      // Adjust the point's position for the camera perspective'
      float $hfv = `camera -q -hfv $sCam`;
      float $ptx = (($ptVecCs.x/(-$ptVecCs.z))/tand($hfv/2))/2.0+.5;
      float $vfv = `camera -q -vfv $sCam`;
      float $pty = (($ptVecCs.y/(-$ptVecCs.z))/tand($vfv/2))/2.0+.5;

      float $ptz = $ptVecCs.z;

      $line = ($ptx*$camW) + " " + ((1-$pty)*$camH) + " \\n";
      fprint $outFileId $line;
    }

    fclose $outFileId;
  }

  string $files = system( "cd %s && bin/generate-pdfs data/ordered-mouth-points.dat" );

  print ($files);

  return 1;
  // }
}
"""

mel_ui="""
// Make UI
string $myWin = `window -widthHeight 600 300 -title "Maya2ToonBoom"`;
columnLayout -adjustableColumn true;
text -label "First select the object, then select one camera below.\\nProceed when ready";
separator -height 10 -style "double";
// List cameras
string $myCams[] = `listCameras -p`;
int $numCam = size($myCams);
// Build list
$myList = `textScrollList -height 200 -numberOfRows 1 -allowMultiSelection false`;
int $i;
for ($i = 0; $i < $numCam; $i++) {
  textScrollList -edit -append $myCams[$i] $myList;
}
textScrollList -edit -selectIndexedItem 1 $myList;
separator -height 10 -style "single";
// OK button
$myButton = `button -label "OK" -height 50 -align "center"`;
button -edit -command ("string $cSelection[1] = `textScrollList -query -selectItem $myList`; screenSpace $cSelection[0];") $myButton;
showWindow $myWin;
"""

mel.eval(mel_screenSpace % (string_for_mel, repo_full_path))
mel.eval(mel_ui)

