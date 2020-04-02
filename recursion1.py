from manimlib.imports import *


class Recursion1Intro(Scene):
    def construct(self):
        title = TextMobject('Recursion').scale(1.5).to_edge(TOP)
        subtitle = TextMobject('\\textit{An introduction}').next_to(title, DOWN)
        self.play(ShowCreation(title))
        self.play(FadeInFromDown(subtitle))
        self.wait()

        # Why?
        # Foundational part of CS
        # Lots of useful, important algorithms are most easily written recursively
        # Lots of data is recursive, and working on it with recursive algorithm is natural and easy
        # And it's on the AP exam!! :)


class FunctionCallsReview(Scene):
    def construct(self):
        # - Review: function calls
        # - What it looks like when you call a function
        # - Where variables live and the call stack
        # - We all know how to call other functions, but take a moment to think about where the arguments and locals
        #   for each function call live, and what the call stack looks like.
        # - Do a simple main() -> foo() -> bar() from the call stack video, but modify to use fewer variables.
        pass


class RecursiveCalls(Scene):
    def construct(self):
        # Recursive calls
        # When you call a function from itself.
        # Show a simple one that calls itself or returns based on a simple condition and single value.
        # - Let's say you have a function that only works for positive integers, and you want to let someone call it
        #   with a negative number and convert it for them automatically.
        # - Int foo(int a) { if (a < 0) { int b = foo(a * -1); return b } return sqrt(a);} and call it from main()
        #   with foo(-4)
        # - Show the call stack, step thru it and update the vars.
        # - See and highlight the recursive call.
        pass


class BrokenRecursiveCalls(Scene):
    def construct(self):
        # - Now modify foo to int foo(int a) { if (a <= 0) { return foo(a * -1); } return sqrt(a); } and call it with
        #   foo(0).
        # - Start stepping through this and see the stack start to grow forever.
        # - When will this program end? Never?
        # - Well, the stack is finite, so eventually you get a SO. Use the Java SO exception and show it hit and stop.
        # - This is the most common mistake in recursion: an incorrect or missing base case leads to infinite recursion
        #   and SO.
        # - Second most common mistake: failing to reduce the input on the recursive call.
        #   - Maybe these mistakes are better illustrated elsewhere?
        pass


class Power1(Scene):
    def construct(self):
        # - So, that works, but it's a silly recursive function that doesn't do anything useful. Let's do something
        #   interesting.
        # - Compute x^n recursively
        # - Show the real equation for this.
        #   - x + x + x + …, n times in total. You could do that with a for loop!
        #   - It's also x * x^(n-1) and x^0 is 1. This is a recursive definition: f(x, n) = x * f(x, n-1) for n > 0,
        #     1 otherwise.
        #   - Check my def and make sure it's reasonable.
        # - Start with power1() since it's so simple.
        # - Show it, run it for (2, 3) or so, show the result.
        pass


class Anatomy(Scene):
    def construct(self):
        # Look at power1() and highlight parts of it. Anatomy of a recursive function.
        # Always has two parts: base case and recursive step.
        # Base cases
        #   - All of these have a base case that ends the recursion and returns.
        #   - Computed directly from the inputs.
        #   - Base cases are often some variant of emptiness. Power1() is a good example, with n == 0.
        #     What if you returned x for n == 1?
        # The recursive step is some variant of decompose/reduce, call, recombine/compute.
        #   - Recursive case: compute the result with the help of one or more recursive calls to the same function.
        #     In this case, the data is reduced in some way in either size, complexity, or both.
        #   - In this case, reducing n by 1 each time.
        pass


class Power2(Scene):
    def construct(self):
        # Now look at power2()
        # Why make the change? Well, now it makes half the calls it would have made.
        # Who cares? Well, a couple of reasons:
        #   - It's faster if you do half the work.
        #   - Each call takes up room on the call stack, and it's finite, so this will work for larger inputs.
        #   - Show the number of recursive calls is log(n) instead of n.
        #     - Graph 'em real quick… should be easy with manim.
        pass


class Power3(Scene):
    def construct(self):
        # Bother to do power3()?
        pass


class Fibonacci(Scene):
    def construct(self):
        # Now do Fibonacci.
        # Two calls instead of one.
        # Refresher on what the equation is and why it's useful.
        # Trace a short call, and track the history of the calls to the side.
        #   - Then run thru a longer one, tracking the history and showing a bushy tree.
        #   - Simplify the call stack as it runs and focus on the growing call history tree.
        #   - Afterwords, explain how most recursive algorithms are shown like this in books and elsewhere, and
        #     encourage them to study the picture and see how it relates to the code.
        #   - Leave this as the final image of the video.
        pass
