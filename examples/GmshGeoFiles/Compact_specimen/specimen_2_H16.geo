// -----------------------------------------------------------------------------
//
// Gmsh GEO: Reference
// ===================
//
// -----------------------------------------------------------------------------
//
// Use the following line to generate the mesh:
// gmsh specimen_2_H16.geo -2 -o specimen_2_H16.msh
//
//      *------------------------------------* -
//      |                                    | |
//      |  _  /-----\                        | |
//      |  | |       |                       | |
//    - | D| |       |                       | |
//    | |  | |       |      /--\             | | hg
//    | |  -  \-----/      | a  |            | | 
//  h1| |                   \--/             | |
//    | |      (0,0)                /--\     | |
//    -  --------*------           | b  |    | -
//    | |                           \--/     | |
//  h1| |                 /--\               | | 
//    | |  _  /-----\    | c  |              | |
//    | |  | |       |    \--/               | | hg
//    - | D| |       |                       | |
//      |  | |       |                       | |
//      |  -  \-----/                        | |
//      |                                    | |
//      *------------------------------------* -
//                |--a--|
//      |---c-----|-------------b------------|       
//
// +---------------+---------------+
// | Parameter     | Value         |
// +===============+===============+
// | $hg$          | $0.6 b$       |
// +---------------+---------------+
// | $h1$          | $0.275 b$     |
// +---------------+---------------+
// | $D$           | $0.25 b$      |
// +---------------+---------------+
// | $c$           | $0.25 b$      |
// +---------------+---------------+
// | $D_a$         | $b/2$         |
// +---------------+---------------+
// | $D_b$         | $b/2$         |
// +---------------+---------------+
// | $D_c$         | $b/2$         |
// +---------------+---------------+

H = 1.6;
b  = 40.0;

// Mesh size parameters
// --------------------
h      = (0.02)*b;    // mesh size far from the crack
hcrack = (0.002)*b; //mesh size near crack

// Parameters for the geometry
// ---------------------------
// All the parameters are defined in terms of the base length "b"
// Change the value of "b" to scale the geometry
hg = (0.6)*b;
a  = (0.2)*b;
h1 = (0.275)*b;
c  = (0.25)*b;
D  = (0.25)*b; 

// Define the parameters for the circles
Da = (0.2)*b;    // Diameter of the "a" circle
xa = b-(0.55)*b; // X coordinate of the center of the "a" circle
ha = (0.25)*b;   // Y coordinate of the center of the "a" circle

Db = (0.1)*b;    // Diameter of the "a" circle
xb = b-(0.25)*b; // X coordinate of the center of the "b" circle
hb = 0.0;        // Y coordinate of the center of the "b" circle

Dc = (0.2)*b;    // Diameter of the "c" circle
xc = b-(3/8)*b;  // X coordinate of the center of the "c" circle
hc = -(0.25)*b;  // Y coordinate of the center of the "c" circle


//           |                       
//           |                       
//   -       |   *                   
//   |       | / |                   
//   |  -    *   |                   
//  j|  |        |                   
//   | f|  -     *---------------*\          
//   |  | l|                       \         
//   -  -  - |---|             30º  \  (a,H)
//             k            -.-.-.-. *  
//                                  /  
//                                 /       
//               *---------------*/          
//               |*                  
//           *   |                   
//           | \ |                   
//           |   *                   
//           |                       
//           | 
f = (0.06375)*b;
j = (0.08875)*b;
k = (0.04250)*b;
l = (0.00375)*b;

angle_deg = 30;
angle_rad = angle_deg * Pi / 180;
tan30 = Tan(angle_rad);
g = a - (l/tan30);

SetFactory("OpenCASCADE");

// ------------------------------------------------------
// ------------------------------------------------------
// A)Geometry Definition: 1)Points 
//                        2)Lines 
//                        3)Curve 
//                        4)Surface 

// ------------------------------------------------------
// A1)Points Definitions: 
//              
//         P4*----------------------*P3
//           |                      |
//           |                      |
//           |                      |
//           |   *P6                |
//           | / |                  |
//         P5*   |                  |
//               |P7     P8         |
//               *-------*\         |
//                         \        |
//                          *P9     |
//                         /        |
//               *-------*/         |
//               |*P11  P10         |
//        P13*   |                  |
//           | \ |                  |
//           |   *P12               |
//           |                      |
//           |                      |
//           |                      |
//           |                      |
//         P1*---------------------*P2
//             
//    |Y
//    |
//    ---X        
//     

//           --Coordinates--
//Points:    -------X,------Y,--Z,
Point(1)   = {     -c,    -hg,  0,  h};
Point(2)   = {      b,    -hg,  0,  h};
Point(3)   = {      b,     hg,  0,  h};
Point(4)   = {     -c,     hg,  0,  h};
Point(5)   = {     -c,    H+f,  0,  h};
Point(6)   = {   -c+k,    H+j,  0,  h};
Point(7)   = {   -c+k,    H+l,  0,  h};
Point(8)   = {      g,    H+l,  0,  h};
Point(9)   = {      a,      H,  0,  h};
Point(10)  = {      g,    H-l,  0,  h};
Point(11)  = {   -c+k,    H-l,  0,  h};
Point(12)  = {   -c+k,    H-j,  0,  h};
Point(13)  = {     -c,    H-f,  0,  h};


// ------------------------------------------------------
// A2)Lines Definition             
Line(1) = {1, 2};  //L1:from P1 to P2: P1*--L1-->*P2
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 5};
Line(5) = {5, 6};
Line(6) = {6, 7};
Line(7) = {7, 8};
Line(8) = {8, 9};
Line(9) = {9, 10};
Line(10) = {10, 11};
Line(11) = {11, 12};
Line(12) = {12, 13};
Line(13) = {13, 1};

// ------------------------------------------------------
// A3)Curve Definition
//
Curve Loop(5) = {1,2,3,4,5,6,7,8,9,10,11,12,13};  //C5: through lines L1,L2,...,L7

// The following curves represent the circles and arcs in the geometry
//
//      *------------------------------------* 
//      |                                    | 
//      |     /-----\                        | 
//      |    |       |                       | 
//      | P16*  *P14 *P15    a               | 
//      |    |       |      /--\             |  
//      |     \-----/  P22*|*P20|*P21        |  
//      |                   \--/     b       | 
//      |      (0,0)                /--\     | 
//       --------*------       P25*|*P23|*P24| 
//      |                  c        \--/     | 
//      |                  /--\              |  
//      |     /-----\ P28*|*P26|*P27         | 
//      |    |       |     \--/              |  
//      | P19*  *P17 *P18                    | 
//      |    |       |                       | 
//      |     \-----/                        | 
//      |                                    | 
//      *------------------------------------* 

// Top circle -------------------------------------------------
Point(14) = {       0, h1, 0, h};   // Center of the circle
Point(15) = { (D)*0.5, h1, 0, h};   // Start point
Point(16) = {(-D)*0.5, h1, 0, h};   // End point of the first arc

Circle(100) = {15, 14, 16};  // First half of the circle
Circle(101) = {16, 14, 15};  // Second half of the circle

Curve Loop(200) = {100, 101};

// Bottom circle -----------------------------------------------
//
Point(17) = {        0, -h1, 0, h};   // Center of the circle
Point(18) = {  (D)*0.5, -h1, 0, h};   // Start point
Point(19) = { (-D)*0.5, -h1, 0, h};   // End point of the first arc

Circle(102) = {18, 17, 19};  // First half of the circle
Circle(103) = {19, 17, 18};  // Second half of the circle

Curve Loop(201) = {102, 103};


// Extra circle A -----------------------------------------------

// Define points
Point(20)  = {          xa,  ha, 0, h};  // Center of the circle
Point(21)  = { xa+(Da*0.5),  ha, 0, h};  // Start point
Point(22) =  { xa-(Da*0.5),  ha, 0, h};  // End point of the first arc

// Define arcs
Circle(104) = {21, 20, 22};  // First half of the circle
Circle(105) = {22, 20, 21};  // First half of the circle

// Combine arcs into a closed loop
Curve Loop(202) = {104, 105};


// Extra circle b -----------------------------------------------
// Define points
Point(23)  = {          xb,  hb, 0, h};  // Center of the circle
Point(24)  = { xb+(Db*0.5),  hb, 0, h};  // Start point
Point(25) =  { xb-(Db*0.5),  hb, 0, h};  // End point of the first arc

// Define arcs
Circle(106) = {24, 23, 25};  // First half of the circle
Circle(107) = {25, 23, 24};  // First half of the circle

// Combine arcs into a closed loop
Curve Loop(203) = {106, 107};


// Extra circle C -----------------------------------------------
// Define points
Point(26)  = {          xc,  hc, 0, h};  // Center of the circle
Point(27)  = { xc+(Dc*0.5),  hc, 0, h};  // Start point
Point(28) =  { xc-(Dc*0.5),  hc, 0, h};  // End point of the first arc

// Define arcs
Circle(108) = {27, 26, 28};  // First half of the circle
Circle(109) = {28, 26, 27};  // First half of the circle

// Combine arcs into a closed loop
Curve Loop(204) = {108, 109};

// ------------------------------------------------------
// A4)Surface Definition
//
//        *----------*
//        |          |
//        *  \       |
//            *  S6  | 
//        *  /       | 
//        |          |
//        *----------*
//         
Plane Surface(6) = {5, 200, 201, 202, 203, 204};  // Subtract circle loops the main surface
Recombine Surface {6};

// Extrude the Surfaces to Create the Volumes
// Extrude {0.0, 0.0, thickness}{Surface{6};}

// ------------------------------------------------------
// ------------------------------------------------------
// B)Mesh Generation: 1)Mesh size Box1 
//                    2)Mesh size Box2
//                    3)Mesh min(Box1,Box2)
//                    3)Extrude Mesh 
//                    4)Mesh Algorithm  


// ------------------------------------------------------
// B1) Mesh size Box1
//
//        *----------------* 
//        |  / - \         |  
//        |  |   | (Field[6])  
//        |  \ - /         |
//         -----------     | 
//        |                |
//        |                |
//        |                |
//        *----------------*

Field[6] = Attractor;
Field[6].EdgesList = {101};

// Define a Threshold field to control mesh size near the attractor
Field[66] = Threshold;
Field[66].InField = 6;         // Use the Attractor field
Field[66].SizeMin = hcrack;    // Minimum mesh size near the attractor
Field[66].SizeMax = h;         // Maximum mesh size far from the attractor
Field[66].DistMin = 0.00;      // Distance from the attractor where SizeMin is applied
Field[66].DistMax = 0.25;       // Distance from the attractor where SizeMax is applied


// ------------------------------------------------------
// B2) Mesh size Box2
//
//        *----------------* 
//        |                |
//        |                |
//        |                |
//         -----------     | 
//        |  / - \         |  
//        |  |   | (Field[7])  
//        |  \ - /         |
//        *----------------*
Field[7] = Attractor;
Field[7].EdgesList = {102};

// Define a Threshold field to control mesh size near the attractor
Field[77] = Threshold;
Field[77].InField = 7;         // Use the Attractor field
Field[77].SizeMin = hcrack;    // Minimum mesh size near the attractor
Field[77].SizeMax = h;         // Maximum mesh size far from the attractor
Field[77].DistMin = 0.00;      // Distance from the attractor where SizeMin is applied
Field[77].DistMax = 0.25;      // Distance from the attractor where SizeMax is applied

// ------------------------------------------------------
// B3) Mesh size Box3
//
//        *----------------* 
//        |                | 
//        |                |
//        |                |
//        *     -----------|
//             | (Field[8])|
//        *     -----------| 
//        |                |
//        |                |
//        |                |
//        *----------------*
Field[8]      =    Box;
Field[8].VIn  = hcrack;
Field[8].VOut =      h;

Field[8].XMin =  g-0.02*b;
Field[8].XMax =  xa -(0.5)*Db;
Field[8].YMin =  H - 0.8;
Field[8].YMax =  3.0;


Field[88]      =    Box;
Field[88].VIn  = hcrack;
Field[88].VOut =      h;

Field[88].XMin =  xa -(1.0)*Db;
Field[88].XMax =  xa +(0.75)*Db;
Field[88].YMin =  H - 0.8;
Field[88].YMax =  ha -(0.2)*Da;


// ------------------------------------------------------
// B2) Mesh size Box2
Field[9] = Attractor;
Field[9].EdgesList = {104};

// Define a Threshold field to control mesh size near the attractor
Field[99] = Threshold;
Field[99].InField = 9;        // Use the Attractor field
Field[99].SizeMin = hcrack;   // Minimum mesh size near the attractor
Field[99].SizeMax = h;        // Maximum mesh size far from the attractor
Field[99].DistMin = 0.00;     // Distance from the attractor where SizeMin is applied
Field[99].DistMax = 0.25;      // Distance from the attractor where SizeMax is applied

// ------------------------------------------------------
// B2) Mesh size Box2
Field[10] = Attractor;
Field[10].EdgesList = {106, 107};

// Define a Threshold field to control mesh size near the attractor
Field[100] = Threshold;
Field[100].InField = 10;        // Use the Attractor field
Field[100].SizeMin = hcrack;   // Minimum mesh size near the attractor
Field[100].SizeMax = h;        // Maximum mesh size far from the attractor
Field[100].DistMin = 0.00;     // Distance from the attractor where SizeMin is applied
Field[100].DistMax = 0.25;      // Distance from the attractor where SizeMax is applied

// ------------------------------------------------------
// B2) Mesh size Box2
Field[11] = Attractor;
Field[11].EdgesList = {108, 109};

// Define a Threshold field to control mesh size near the attractor
Field[101] = Threshold;
Field[101].InField = 11;        // Use the Attractor field
Field[101].SizeMin = hcrack;   // Minimum mesh size near the attractor
Field[101].SizeMax = h;        // Maximum mesh size far from the attractor
Field[101].DistMin = 0.00;     // Distance from the attractor where SizeMin is applied
Field[101].DistMax = 0.25;     // Distance from the attractor where SizeMax is applied



// ------------------------------------------------------
// B3) Mesh min(Box1,Box2)
Field[14] = Min;
// Field[14].FieldsList = {8, 66, 77, 99, 100, 101};
Field[14].FieldsList = {8,88, 66, 77, 99};
Background Field = 14;


// ------------------------------------------------------
// B5)Mesh Algorithm
Geometry.Tolerance = 1e-12;
Mesh.Algorithm = 8;                    // Frontal-Delaunay for quads
Mesh.RecombineAll = 1;                 // Recombine all surfaces
Mesh.SubdivisionAlgorithm = 1;         // All quads subdivision
Mesh.RecombinationAlgorithm = 1;       // Simple recombination
// ------------------------------------------------------
// Physical groups definition
//         

Physical Surface("surface", 202) = {6};

Physical Curve("circle_top_top", 204) = {101};
Physical Curve("circle_top_bottom", 205) = {100};

Physical Curve("circle_bottom_top", 206) = {103};
Physical Curve("circle_bottom_bottom", 203) = {102};

Physical Curve("top_circle", 210) = {101, 100};
