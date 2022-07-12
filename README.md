# MegaMini addon for Blender
"Solar system in a box": using 'forced perspective' to create 'condensed space' for viewing large objects that are separated by very large distances, at correct scale (e.g. planets, moons, stars).

Works best with spheres, but a 'mega focus' can be used to manually adjust the scale of an object - thus negating the 'forced perspective' of the object, and the object will return to 1:1 scale.

"Forced perspective is a technique which employs optical illusion to make an object appear farther away, closer, larger or smaller than it actually is. It manipulates human visual perception through the use of scaled objects and the correlation between them and the vantage point of the spectator or camera."

https://en.wikipedia.org/wiki/Forced_perspective

Following the "solar system in a box" analogy:
- two systems are used, mega and mini
  1) "Mini" system is the "pocket" version of the "Mini" system
  2) "Meag" system is full size, i.e. scale = 1
- the "Mini" system is a scaled down version of the "Mega" system
- user can choose the scale, but the scale should not be changed after creating the systems
  - scale is currently stored in the "Observer", and the "Mega-Mini Proxy", as a custom property
  - changing scale would require manually changing custom properties in these objects
    - TODO code a solution