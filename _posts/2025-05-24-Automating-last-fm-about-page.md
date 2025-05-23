---
title: "Automatically updating the 'about' page with my last.fm top listen"
date: 2025-05-23
---

I "scrobble" all of my listens to [last.fm](https://www.last.fm/), which for some reason still exists.
You can automatically link Spotify to last.fm to have all of your listens synced there --- and for some reason this feature still exists.
This is quite nice, because Spotify have deigned that your stats are only available once a year ---und exactly vonce a year--- in a specially curated selection of statistics.
I thought it would be fun to put my top track of the month on the [about page](/about), and this proved quite easy to automate with a github workflow.

## The script

The python script is [here](https://github.com/christopherdoyle/christopherdoyle.github.io/blob/main/code/last-fm-sync/main.py), it's pretty dumb because I started writing something generalized and then got bored and specialised for this task.
You run it, it reads an API key and a username from the env, and it spits out the top track details into...

## _config.yml

Jekyll blog engine has a nice little YAML config file, and we can reference the variables within from any of the markdown pages.
In particular, the config can contain this:

```yaml
top_track:
  artist: Dire Straits
  name: On Every Street
  playcount: 33
```

and the `about.md` can contain this:

{% raw %}
```markdown
* My most listened track this month is {{ site.top_track.name }} by {{ site.top_track.artist }} ({{ site.top_track.playcount }} listens)
```
{% endraw %}

It wouldn't have been hard to `sed` the about page directly, but this is much cleaner.
We can read the YAML file into a python object, update it, and write it back.
I didn't bother making this stable, so it can create some unnecessary churn to the YAML file in the diff, but I don't really care.
Once Jekyll build runs, the about page is updated with the new values of the variables.

## GH workflow

The workflow is straightforward, it just checks out the code, installs the python deps, run the script, then gits the changes into a branch and opens a PR.
I'd like to review the PR to start with and make sure it is sensible, and also nuke the PR when it has a truly embarrassing track, but it should be possible to automatically merge this, or otherwise push directly to main.
The only potential problem I see pushing to main is getting GH actions to be happy running the Jekyll build so that the site actually updates.
