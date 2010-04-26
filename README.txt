ShinyStat
A plugin for Trac that will connect to ShinyMUD's StatSender and display the status of the game server.

-- Running ShinyStat --

Software requirements:
  * setuptools >= 0.6b1
  * Trac 0.11
  * Genshi >= 0.4

Visit http://trac-hacks.org/wiki/EggCookingTutorialTrac0.11 for more information on the software requirements, as well as documentation on creating eggs and plugins for Trac. Visit http://trac.edgewall.org/wiki/TracPlugins for more detailed instructions on installing Trac plugins.

1) First you'll want to change the HOST and PORT number in shinystat/shinystat.py to your game's host and StatSender port number.

2) From the same directory as the setup.py file (the directory this README is in) run the following command: 
	python setup.py bdist_egg
If everything succeeded, several new directories will have been created, including a /dist directory with a .egg file in it.

3) Move the .egg file to your to the /plug of your Trac project environment.

4) Restart your webserver or tracserver.

You should now see the ShinyMUD Stats tab on your Trac page.

-- Notes --
 * Make sure that StatSender is enabled for your version of ShinyMUD, or ShinyStat won't see your game as being online! StatSender can be enabled/disabled from your ShinyMUD config file.