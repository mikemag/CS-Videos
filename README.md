# CS Education Videos using Manim

This is the start of some CS education videos illustrating concepts and algorithms that might benefit from some 
visuals and animation to better help students understand.

These are built using [Manim](https://github.com/3b1b/manim), created by Grant Sanderson of 
[3blue1brown](https://www.3blue1brown.com/) for his series of mathematics videos.

## Videos

I'll add links to completed videos as I publish them.

## Early Development

This is my first attempt building a video like this, and one using Manim. I consider everything here so far
a prototype, early beta, etc. Take it all with a grain of salt.

I do hope to factor out the useful classes for core concepts into a reusable library for others.

## Setup

My raw notes from getting this setup locally on a MacBook pro running macOS Catalina 10.15.3. I used MacPorts for 
most of this since a lot of packages were missing under Conda.  

Installation instructions followed: https://repperiumsci.blogspot.com/2019/12/my-adventures-with-manim-part_22.html                                                                

```
sudo port install cairo
sudo port install pkgconfig
sudo port install py-virtualenv
sudo port select --set virtualenv virtualenv38
sudo port install sox
sudo port install ffmpeg
Downloaded and installed BasicTeX
sudo tlmgr update --self
sudo tlmgr install standalone preview doublestroke relsize fundus-calligra wasysym physics dvisvgm.x86_64-darwin dvisvgm rsfs wasy cm-super
python3 -m venv ManimEnv
cd ManimEnv
source bin/activate
pip install colour data decorator ffmpeg funcsigs future latex numpy opencv-python Pillow progressbar pycairo pydub scipy shutilwhich six sox tempdir tqdm

source ManimEnv/activate
cd ManimEnv/manim
python manim.py example_scenes.py
```                                        

## Useful Resources

Useful tutorials, example projects, etc.

* https://github.com/Elteoremadebeethoven/AnimationsWithManim
* https://talkingphysics.wordpress.com/2019/01/08/getting-started-animating-with-manim-and-python-3-7/
* https://github.com/cpvrlab/SLProject/tree/rasterization-animation/rasterization-animation
* https://github.com/pedrovhb/manim/blob/master/animacoes_pedro/bfs.py
* https://github.com/cpvrlab/SLProject/blob/rasterization-animation/rasterization-animation/pixel_screen.py
* https://www.reddit.com/r/manim/comments/f9h098/just_created_my_first_animation_with_manim/
* https://www.overleaf.com/learn/latex/Code_listing

## License

Everything here is licensed under the MIT license except as
otherwise noted. See the LICENSE file in this directory for details.
