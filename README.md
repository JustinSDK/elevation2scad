# elevation2scad

Generate OpenSCAD source code from elevation data. I don't provide code for getting elevation data because providers might have their own license. You need to write your own for getting that.

Save your elevation data into `elevations.dat` with the format `longitude  latitude  elevation` and order by `[longitude, latitude].`

After `elevations.dat` is ready, run `python genscad.py`. Use [OpenSCAD](https://www.openscad.org/) to open the generated `evelation.scad` which requires my library [dotSCAD](https://github.com/JustinSDK/dotSCAD). 

You can use the `gen_surface_from` function to generate data for [`surface`](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#Surface). Just uncomment the line in `genscad.py`.

	if __name__ == "__main__":
	    ymin, yinc, thickness, scale = 21.750, 0.015, -1, 100
	    # generate elevation.scad
	    # gen_scad_from('elevations.dat', ymin, yinc, thickness, scale = scale)
	    
	    # generate surface.dat
	    gen_surface_from('elevations.dat', ymin, yinc)

After generating `surface.dat`, write `surface.scad` containing the following.

    surface(file = "surface.dat", center = true, convexity = 5);

The model shown below is [Taiwan](https://www.google.com.tw/maps/place/%E5%8F%B0%E7%81%A3/@23.6558232,120.3439706,8.04z/data=!4m5!3m4!1s0x346ef3065c07572f:0xe711f004bf9c5469!8m2!3d23.69781!4d120.960515), generated from data that latitude from 21.75 to 25.500 and longitude from 119.900 to 122.100.

![Taiwan](images/Taiwan.JPG)
