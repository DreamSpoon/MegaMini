# MegaMini addon for Blender
"Solar system in a box" addon: using 'forced perspective' to create 'condensed space' for viewing large objects that are separated by very large distances, at correct scale (e.g. planets, moons, stars). Also, a "pocket" system model is incorporated to allow for extra scaling possibilities.

Works best with spherical objects.

"Forced perspective is a technique which employs optical illusion to make an object appear farther away, closer, larger or smaller than it actually is. It manipulates human visual perception through the use of scaled objects and the correlation between them and the vantage point of the spectator or camera."
https://en.wikipedia.org/wiki/Forced_perspective

TODO: Use images in the explanation. YouTube video also coming soon, this is hard to explain with words...

## Install Addon in Blender
1) Start Blender
2) Go to User Preferences -> Addons -> Install addon from file
3) Choose MegaMini.zip file you downloaded (available for download from 'Releases' section of this website)

Done! The addon is now installed, but **you need to enable it by clicking the checkbox beside it's name**, in the addons window.

## Notes (work in progress)
The addon uses the "forced perspective" illusion, combined with a "scaled-actual" double system.
The "scaled-actual" system allows for placing objects at very large distances apart.

Example:
  - a "place" is created at the center, objects are added to the place (in Blender speak, the objects are "parented" to the place)
  - the "observer" is moved 10,000 units away and a new "place" is created
  - when the observer is moved, the original "place" is moved away and scaled ("forced perspective" aspect of rig)
  - the new "place" has objects added (i.e. parented to the "place")
  - the "observer" can now be moved between "places", and the objects will always look like they are the right size - even though they are actually much closer together
  - the distance between "places" is compressed, and the "observer" is used to determine the scale of each "place"
  - when the "observer" is positioned exactly at the same location as the "place", then the place be full scale (i.e. one-to-one scale)

Following the "solar system in a box" analogy:
- two systems are connected with drivers, so that a "scaled" system's movements drive an "actual" system's movements:
  1) Scaled Window
  2) Actual Window
- "Scaled Window" system is the "pocket" version of the "Actual Window" system
- drivers are used to connect the Scaled system to the Actual system, so that a scaling factor is applied
  - e.g. if scale = 1000, then movement of objects in the Scaled system will cause movements 1000x as much in the Actual system
    - if "Scaled" Object A moves left 15 meters, then "Actual" Object A moves left 15,000 meters
- user can choose the scale for each rig separately, but the scale should not be changed after creating the systems

## Other Notes
- a 'Scaled Focus' can be used to manually adjust the scale of an object
  - thus negating the 'forced perspective' of the object, and the object will return to 1:1 scale
  - do this by moving the "Scaled Focus" bone to the same location as the "Scaled Observer" bone
    - this is easiest to accomplish by adding a "Copy Location" bone constraint to the "Scaled Focus" bone
	- set "target" of "Copy Location" bone constraint to "Scaled Observer" bone, of the same armature
	  - first, set "target object"
	  - second, set "target bone" to "Scaled Observer"

The scale of objects (i.e. the scale of the "place") can be individually adjusted, with the distance automatically adjusting to account for the scale difference.
i.e. an object can have it's scale set manually and the MegaMini Rig will automatically vary the distance to account for the scale.
  - to do the manual adjustment, go to the custom property of the "ActualProxy" bone, i.e.
    - enter Pose mode
	- select the "ActualProxy" bone
	- look in "Bone" settings panel
	    - Custom Properties sub-panel
		  - mega_mini_bone_scl_mult
