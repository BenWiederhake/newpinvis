# newpinvis

There are only 10K PINs, and humans are terrible at being unpredictable. This website showcases this graphically, and even generates “secure” PINs on-demand!

This project is heavily inspired by a [blog post on the same topic](http://datagenetics.com/blog/september32012/index.html) by datagenetics (Nick Berry?), and couldn't work without the data from [Have I Been Pwned](https://haveibeenpwned.com/Passwords).

The main results are:
- Don't use 1234, 1111, 0000, 1342, 1212, 2222, 4444, 1122, 1986, 2020, or any quadruplet.
- The top 3 PINs alone cover 11.7%! That means more than once in nine trials, a random bank card can be successfully used with one of these PINs.
- In fact, don't use anything that looks like a recent year (down to 1919!), or a valid MMDD or DDMM date.
- Before this blog post, 6754 and 7571 were the two least-often used PINs. Don't use them just because you read them here, duh.
- Also, striking your fingers along the pad is a bad idea (0258, 0786, etc.)
- Taking the inverse of this distribution is a very robust way to generate a PIN that won't likely be tried very early.
- Go ahead and [check it out!](https://benwiederhake.github.io/newpinvis/) Just explore the lovely diagram, I'm sure you will find something that I didn't, simply because there is Just! So! Much!
- Also, I learned *again* that generating ten thousand DOM nodes doesn't really work well. Sorry.

## TODO

* More performant. I think the tooltips could be generated on the fly using JavaScript, which *should* help a lot with the extreme lag.
* Automatic deployments. It's basically ready for it.
* Take over the world, and convince banks to generate PINs using a more secure distribution, so that noone accidentally receives a card with the PIN 1234. Also, convince them to blacklist 1234 and perhaps the entire top 10.

## TODONT

* All of this is a bit light-hearted. I'm sure I'm not the first to ever look into this topic, and I'm sure there's so much more to know and learn about it than I discovered in an afternoon. So let's not turn this into a BigSeriousProject™.
* There is absolutely no way I will ever take responsibility if you decide to use this PIN generator and something goes wrong. I *believe* you can trust it, but *you* shouldn't believe it, just because some random guy on the internet tells you.

## Contribute

Feel free to dive in! [Open an issue](https://github.com/BenWiederhake/newpinvis/issues/new) or submit PRs.
