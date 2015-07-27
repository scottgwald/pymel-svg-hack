from pymel.core import *

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
  string $folderPath = "/Users/scottgwald/mygit/pymel-svg-hack/maya-output/";  
  // get the currently selected point
  string $dumpList[] = [%s]
  string $dumpList[] = `ls -sl`;
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

mel_ui_fn="""
global proc myMouthScript() {
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
}
"""	

mel.eval(mel_screenSpace)
mel.eval(mel_ui)
# mel.myMouthScript()

