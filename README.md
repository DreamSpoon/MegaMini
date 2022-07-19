# MegaMini addon for Blender
"Solar system in a box" addon: using 'forced perspective' to create 'condensed space' for viewing large objects that are separated by very large distances, at correct scale (e.g. planets, moons, stars). Also, a "pocket" system model is incorporated to allow for extra scaling possibilities.

Works best with spherical objects.

"Forced perspective is a technique which employs optical illusion to make an object appear farther away, closer, larger or smaller than it actually is. It manipulates human visual perception through the use of scaled objects and the correlation between them and the vantage point of the spectator or camera."
- https://en.wikipedia.org/wiki/Forced_perspective

TODO: Use images in the explanation. YouTube video also coming soon, this is hard to explain with words...

## Install Addon in Blender
1) Start Blender
2) Go to User Preferences -> Addons -> Install addon from file
3) Choose MegaMini.zip file you downloaded (available for download from 'Releases' section of this website)

Done! The addon is now installed, but **you need to enable it by clicking the checkbox beside it's name**, in the addons window.

## Overview
The addon uses the "forced perspective" illusion, combined with a "proxy-actual" system.
The "proxy-actual" system allows for placing objects at very large distances apart, using proxies to relate a small "proxy" space to a large "actual" space.

Example:
  - a "place" is created at the center, objects are added to the place (in Blender speak, the objects are "parented" to the place)
  - the "observer" is moved 10,000 units away and a new "place" is created
  - when the observer is moved, the original "place" is moved away and scaled ("forced perspective" aspect of rig)
  - the new "place" has objects added (i.e. parented to the "place")
  - the "observer" can now be moved between "places", and the objects will always look like they are the right size - even though they are actually much closer together
  - the distance between "places" is compressed, and the "observer" is used to determine the scale of each "place"
  - when the "observer" is positioned exactly at the same location as the "place", then the place be full scale (i.e. one-to-one scale)

Blender "Drivers" make this possible:
- two systems are connected with drivers, so that a "scaled" system's movements drive an "actual" system's movements:
  1) Proxy Field
  2) Actual
- "Proxy Field" system is the "pocket" version of the "Actual" system
- drivers are used to connect the Scaled system to the Actual system, so that a scaling factor is applied
  - e.g. if scale = 1000, then movement of objects in the Proxy (scaled) system will cause movements 1000x as much in the Actual system
    - if "Proxy Place" moves left 15 meters, then actual "Place" moves left 15,000 meters
- user can choose the scale for each rig separately, but the scale should not be changed after creating the systems
  - except with addon - TODO

## Light and Shadow Notes
Due to automatic changes in object positions and scales, shadows between objects may be "wrong".
Possible solutions include, but are not limited to:
  - use of the "Sun" type of light can help overcome the problem
    - good where objects have common light source, but don't need to shadow each other
	- e.g. moon and planets, without eclipse
	  - an eclipse might be "baked" onto an object, see next
  - baked (pre-rendered) "shadow maps"
    - too complicated a subject to list all the details here, so here is just one link:
      - [Baking Textures, Light, and Shadows | Blender 2.82 Quarantine Series 1-12](https://www.youtube.com/watch?v=Eio01Yl3G1E)
      - and baked shadow maps can be used in Cycles:
        - modify original Material Shader of object (make a backup copy first):
          - use Texture Image node with original texture (e.g. 8k map of Moon),
          - attach original Texture Image node (Color socket) to Emission shader node (Color socket),
          - use Texture Image node with baked shadow map texture,
		  - attach baked shadow map Texture Image (Color socket) to Emission shader node (Strength socket),
          - attach Emission Shader output to Material Output
  - multiple render passes (compositor work required)
    - may require multiple scenes, composited together

## MegaMini Rig Notes
- rename "Place"/"ProxyPlace" bones to organize the rig as needed
  - MegaMini Rig armature bone names can be modified, and it will not "break" the rig - i.e. drivers will still work
- a 'Proxy Place Focus' can be used to manually adjust the scale of a place
  - thus negating the 'forced perspective' of the object, and the individual place (and not the entire rig) will return to 1:1 scale
  - do this by moving the "ProxyPlaceFocus" bone to the same location as the "ProxyObserver" bone
    - this can be animated by adding a "Copy Location" bone constraint to the "ProxyPlaceFocus" bone, to copy the location of the "ProxyObserver" bone
	  - first, select the "ProxyPlaceFocus" bone related to the place that needs to be 1:1 scale
	  - set "target object" to same MegaMini Rig
	    - e.g. if the bones being used are in object "MegaMiniRig.003", then set set "target object" of "Copy Location" bone constraint to "MegaMiniRig.003"
	  - set "target bone" to "ProxyObserver"
    - bone names may vary, depending on the order in which places are added to the MegaMini Rig, and if the user renamed bones

The scale of each "place" can be individually adjusted, with the distance automatically adjusting to account for the scale difference.
i.e. "place" have it's scale set manually and the MegaMini Rig will automatically vary the distance to account for the scale of that "place".
  - to do the manual adjustment, go to the custom property of the "Place" bone, i.e.
    - enter Pose mode
	- select the "Place" bone
	- look in "Bone" settings panel
	    - Custom Properties sub-panel
		  - mega_mini_bone_scl_mult
    - increase the "mega_mini_bone_scl_mult" value to make the "place" larger
	  - "place" will move farther away from observer, to compensate for larger scale
	- decrease the "mega_mini_bone_scl_mult" value to make the "place" smaller
	  - "place" will move closer away from observer, to compensate for smaller scale

The "forced perspective" effect for all objects in an armature can be easily disabled by setting the MegaMini Rig object's custom property "mega_mini_fp_power" to the value 0 (zero).
The default setting of "mega_mini_fp_power" is 0.5 (square root), which results in objects shrinking very fast as they move away from the observer.
  - good for very large spaces
    - e.g. Solar System

Setting "mega_mini_fp_power" to 0.25, or less, results in objects shrinking as they move very far away from the observer - but the "forced perspective" effect comes on in a less dramatic fashion - i.e. less "warping" of space.
  - better suited to "earth satellite scale"
    - e.g. giant space ships parked in Earth's orbit
