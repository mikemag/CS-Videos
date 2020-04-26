# CS Education Videos using Manim

This is the source for my CS education videos intended to explain various CS 
concepts to high school students visually. 
I hope to illustrate concepts and algorithms that might benefit from some 
visuals and animation, to better help students understand.

I'm putting the videos up on my YouTube channel here: [youtube.com/TheMikemag](youtube.com/TheMikemag)

I hope to keep these short (bite-sized, or is it byte-sized?) and largely silent.

These videos are built using [Manim](https://github.com/3b1b/manim), 
created by Grant Sanderson of [3blue1brown](https://www.3blue1brown.com/) for 
his series of mathematics videos [https://www.youtube.com/channel/UCYO_jab_esuFRV4b17AJtAw](https://www.youtube.com/channel/UCYO_jab_esuFRV4b17AJtAw) 

## Manim Fork

These videos require my slightly-modified fork of manim. Specifically, the
`csvideos` branch: [https://github.com/mikemag/manim/commits/csvideos](https://github.com/mikemag/manim/commits/csvideos)

The key differences are:
1. Fixed BraceLabel
1. Respecting fill colors when reading SVGs. This allows Pygments to color 
source code.
1. Updated TeX template to include Pygments styles and such.

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

Best on Manim:

* The best source of info to-date: https://github.com/Elteoremadebeethoven/AnimationsWithManim
  * She also runs a [r/mainm on Reddit](https://www.reddit.com/r/manim/) and a [Manim Discord](https://discordapp.com/invite/mMRrZQW).
* I also like to check out the projects under from_3b1b/active for examples
* Active Manim development is taking place on the shaders branch, and that's where you can find the source to his
current videos, but the API in the shaders branch is in flux and has been quite buggy in my experience, so I've been
sticking with the master branch.

On TeX/LaTeX:

Manim assumes you know LaTeX, but many may be new to this. Overleaf has a really nice [guide and knowledgebase](https://www.overleaf.com/learn/latex/Main_Page)
for it that I've been using to refresh my memory **a lot**. I've never used their tool
but this reference site is excellent.

Finally, random Manim projects for examples:

* https://talkingphysics.wordpress.com/2019/01/08/getting-started-animating-with-manim-and-python-3-7/
* https://github.com/cpvrlab/SLProject/tree/rasterization-animation/rasterization-animation
* https://github.com/pedrovhb/manim/blob/master/animacoes_pedro/bfs.py
* https://github.com/cpvrlab/SLProject/blob/rasterization-animation/rasterization-animation/pixel_screen.py
* https://www.reddit.com/r/manim/comments/f9h098/just_created_my_first_animation_with_manim/

## License

The content of the videos and presentations, and the code in this directory which generate the 
visuals for these, are copyright by [Michael Magruder](https://github.com/mikemag) and 
licensed under a 
[Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

The general purpose animation code found in the csanim subdirectory, on the other hand, 
is licensed under the MIT license except as
otherwise noted. See the LICENSE file in that directory for details.

