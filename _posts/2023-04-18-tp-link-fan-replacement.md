---
title: TP-Link POE Switch Fan Replacement
date: 2023-04-18
---

<style>
article h1 {
  color: #653024;
  text-shadow: 5px 5px 0 #e6ceb5;
  transition: all linear 500ms;
}
article h1:hover {
  cursor: pointer;
  text-shadow: -5px -5px 0 #e6ceb5;
  transition: text-shadow linear 500ms;
}

@media (prefers-color-scheme: dark) {
    article h1 {
      color: #e6ceb5;
      text-shadow: 5px 5px 0 #653024;
    }
    article h1:hover {
        text-shadow: -5px -5px 0 #653024;
    }
}
</style>

The [TP-Link TL-SG2210MP](https://www.tp-link.com/uk/business-networking/omada-sdn-switch/tl-sg2210mp/)
is a relatively inexpensive 10-Port Gigabit POE+ Switch, which I picked up for
about 177GBP.
It's not really designed for home use, and the fan is...horrible.
It's loud, but more importantly incredibly whiny.

Luckily, I own a screwdriver.<span class="marginnote">There is a large exposed
power supply unit at the other side of the device to the fan, likely don't touch this?</span>

![TP-Link switch insides](/assets/images/2023-04-18_switch-original-insides.jpg)

The fan inside my unit is a [SUNON
MF40201V3-1000C-F99](http://www.sunon-fan.com/product/MF40201V3-1000C-F99.html).
According to the linked product page it pushes 6.3 CFM at a static pressure of
0.11in h2o.
A replacement fan would ideally hit these specs with a lower noise level.

I replaced the fan with a [Noctua NF-A4x20
FLX](https://noctua.at/en/nf-a4x20-flx/specification) which pushes 9.4 m3/h,
about 5.5 CFM, at a static pressure of 2.26 mm h2o, about 0.09 in h2o.
This is a little lower than the SUNON, but I'm bargaining that the provided fan
is designed to handle a workload of up to 8 POE devices drawing a total of
150W, of which I will use a fraction.

Replacing the fan is straightforward, except that they glued the fan header in.
Usually this is so that it does not come loose in shipping, but usually it is
easy to remove hot-glue gun glue, whereas this is more like PVA?

![GLUE](/assets/images/2023-04-18_glue.jpg "Remove carefully!")

I carefully scraped off the glue with a screwdriver and replaced in the Noctua
fan. The fan is the same depth and the existing screws worked fine.

![Noctua](/assets/images/2023-04-18_noctua.jpg "Sexy sexy brown and tan")

## Fan noise

As a rough measure, I used a free smartphone app:

<span class="marginnote">The switch has a loud full RPM spin up when it is
first started up. These numbers are <em>after</em> that.</span>

| | Noise (dB) |
|------------------|----|
| Base noise level | 36 |
| Stock fan        | 49 |
| Noctua fan       | 38 |


This is great!
Subjectively, the Noctua fan is barely audible, and has no high-pitched whine.


## Temperatures

There are no temperature sensors on the TP-Link, at least none that are exposed
in the web interface or SSH interface.
It was cool to the touch before the replacement, and it is cool to the touch
now.
Given the low load I am applying, this is expected.
