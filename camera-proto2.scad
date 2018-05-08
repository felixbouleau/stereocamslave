//
// raspberry pi cameras mount
//
// copyright 2014 Sebastien Roy
// Licence: Public domain
//

/* [General] */

// Reduce the diameter of the pegs (units are 0.01mm, so for 0.1mm enter 10)
tolerance=0; // [0:100]

camera_width = 42;
num_cameras = 4;
margins = 21;
full_rig_width = (camera_width * num_cameras) + (margins * (num_cameras - 1));

// to stop customizer
module nop() { }


module centercube(sz) {
	translate(sz/-2) cube(sz);
}

//
// peg: radius of the peg cylinder. Normally 1mm
//
module base() {
	// base
	hull() {
	translate([0,12.5,-10]/2) centercube([2,2,2]);
	translate([full_rig_width,12.5,-10]/2) centercube([2,2,2]);
    translate([full_rig_width,-12.5,-10]/2) centercube([2,2,2]);
    translate([0,-12.5,-10]/2) centercube([2,2,2]);
	}
	

}

module pegs(camera_index, peg=1.0) {
    // One row of pegs
    
    first_row_x = 0 + ((camera_index-1) * camera_width) + ((camera_index-1) * margins);
    second_row_x = (first_row_x + camera_width);
    
    translate([first_row_x,-12.5,0]/2) cylinder(r=peg,h=3,$fn=32);
    translate([first_row_x,12.5,0]/2) cylinder(r=peg,h=3,$fn=32);
    
    translate([second_row_x,-12.5, 0]/2) cylinder(r=peg,h=3,$fn=32);
    translate([second_row_x,12.5,0]/2) cylinder(r=peg,h=3,$fn=32);
    
    hull() {
	translate([first_row_x,-12.5,-4]/2) centercube([2,2,4]);
	translate([first_row_x,12.5,-4]/2) centercube([2,2,4]);
	}
    
    hull() {
	translate([second_row_x,-12.5,-4]/2) centercube([2,2,4]);
	translate([second_row_x,12.5,-4]/2) centercube([2,2,4]);
	}
}
// call with the radius of the peg
base(1-tolerance/200);
for (a =[1:(num_cameras)])pegs(a, 1-tolerance/200);

