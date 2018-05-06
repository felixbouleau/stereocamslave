//
// raspberry pi cameras mount
//
// copyright 2014 Sebastien Roy
// Licence: Public domain
//

/* [General] */

// Reduce the diameter of the pegs (units are 0.01mm, so for 0.1mm enter 10)
tolerance=0; // [0:100]

camera_width = 21;
num_cameras = 4;
margins = 2;
full_rig_width = (camera_width * num_cameras) + (margins * (num_cameras - 1));

// to stop customizer
module nop() { }


module centercube(sz) {
	translate(sz/-2) cube(sz);
}

//
// peg: radius of the peg cylinder. Normally 1mm
//
module camera(peg=1.0) {
	// pegs
	translate([-full_rig_width,-12.5,0]/2) cylinder(r=peg,h=3,$fn=32);
	translate([(-full_rig_width + (camera_width*2)),-12.5,0]/2) cylinder(r=peg,h=3,$fn=32);
	translate([-full_rig_width,12.5,0]/2) cylinder(r=peg,h=3,$fn=32);
	translate([(-full_rig_width + (camera_width*2)),12.5,0]/2) cylinder(r=peg,h=3,$fn=32);
	// peg holders
	hull() {
	translate([-full_rig_width,-12.5,-4]/2) centercube([2,2,4]);
	translate([-full_rig_width,12.5,-4]/2) centercube([2,2,4]);
	}
	hull() {
	translate([(-full_rig_width + (camera_width*2)),-12.5,-4]/2) centercube([2,2,4]);
	translate([(-full_rig_width + (camera_width*2)),12.5,-4]/2) centercube([2,2,4]);
	}
	// base
	hull() {
	translate([-full_rig_width,12.5,-10]/2) centercube([2,2,2]);
	translate([full_rig_width,12.5,-10]/2) centercube([2,2,2]);
    translate([full_rig_width,-12.5,-10]/2) centercube([2,2,2]);
    translate([-full_rig_width,-12.5,-10]/2) centercube([2,2,2]);
	}
	

}

// call with the radius of the peg
camera(1-tolerance/200);

