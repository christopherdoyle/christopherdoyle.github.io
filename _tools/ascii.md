---
layout: default
title: ASCII
---

<style>
    *, * > * {
        box-sizing: border-box;
    }

    body {
        margin: 0 auto;
        padding: 1rem;
        min-width: 1500px;
        max-width: 100%;
    }

    table.ascii {
        border-collapse: collapse;
        border-color: var(--on-background-color);
        font-family: monospace;
        margin: 2rem 0;
    }
    table.ascii > thead {
        border-bottom: 2px solid;
    }
    table.ascii > tbody > tr:nth-child(8n) {
        border-bottom: 1px solid;
    }
    table.ascii colgroup {
        border: 1px solid;
    }
    table.ascii th, table.ascii td {
        padding: .5rem 1rem;
    }
    table.ascii th {
        font-weight: bold;
        text-align: center;
    }
    table.ascii td {
        font-weight: normal;
        white-space: nowrap;
    }
    table.ascii td.non-printable {
        font-style: italic;
    }
    table.ascii > tbody > tr > td:nth-child(3n - 2) {
        text-align: center;
    }
    table.ascii > tbody > tr > td:nth-child(3n - 1) {
        text-align: center;
    }
    table.ascii > tbody > tr > td:nth-child(3n) {
        text-align: right;
    }
    table.ascii caption {
        caption-side: bottom;
        padding: 1.5rem;
    }
    table.ascii td.digit {
        background-color: lightpink;
        color: #111;
    }
    table.ascii td.shift-digit {
        background-color: lightsalmon;
        color: #111;
    }
    table.ascii td.big-alpha {
        background-color: lightgreen;
        color: #111;
    }
    table.ascii td.little-alpha {
        background-color: lightblue;
        color: #111;
    }
    table.ascii td.special {
        background-color: lightgoldenrodyellow;
        color: #111;
    }
</style>

<table class="ascii">
    <caption>ASCII table</caption>
    <colgroup><col class="dec"/><col class="hex"/><col class="char"/></colgroup>
    <colgroup><col class="dec"/><col class="hex"/><col class="char"/></colgroup>
    <colgroup><col class="dec"/><col class="hex"/><col class="char"/></colgroup>
    <colgroup><col class="dec"/><col class="hex"/><col class="char"/></colgroup>
    <thead>
    <tr>
        <th>Dec</th><th>Hex</th><th>Chr</th>
        <th>Dec</th><th>Hex</th><th>Chr</th>
        <th>Dec</th><th>Hex</th><th>Chr</th>
        <th>Dec</th><th>Hex</th><th>Chr</th>
    </tr>
    </thead>
    <tbody>
        <tr>
            <td class="special">0</td><td class="special">00</td><td class="special non-printable">[NULL]</td>
            <td class="special">32</td><td class="special">20</td><td class="special non-printable">[SPACE]</td>
            <td>64</td> <td>40</td><td>@</td>
            <td>96</td><td>60</td><td>`</td>
        </tr>
        <tr>
            <td class="special">1</td><td class="special">01</td><td class="special non-printable">[START OF HEADING]</td>
            <td class="shift-digit">33</td><td class="shift-digit">21</td><td class="shift-digit">!</td>
            <td class="big-alpha">65</td><td class="big-alpha">41</td><td class="big-alpha">A</td>
            <td class="little-alpha">97</td><td class="little-alpha">61</td><td class="little-alpha">a</td>
        </tr>
        <tr>
            <td class="special">2</td><td class="special">02</td><td class="special non-printable">[START OF TEXT]</td>
            <td class="shift-digit">34</td><td class="shift-digit">22</td><td class="shift-digit">"</td>
            <td class="big-alpha">66</td><td class="big-alpha">42</td><td class="big-alpha">B</td>
            <td class="little-alpha">98</td><td class="little-alpha">62</td><td class="little-alpha">b</td>
        </tr>
        <tr>
            <td class="special">3</td><td class="special">03</td><td class="special non-printable">[END OF TEXT]</td>
            <td class="shift-digit">35</td><td class="shift-digit">23</td><td class="shift-digit">#</td>
            <td class="big-alpha">67</td><td class="big-alpha">43</td><td class="big-alpha">C</td>
            <td class="little-alpha">99</td><td class="little-alpha">63</td><td class="little-alpha">c</td>
        </tr>
        <tr>
            <td class="special">4</td><td class="special">04</td><td class="special non-printable">[END OF TRANSMISSION]</td>
            <td class="shift-digit">36</td><td class="shift-digit">24</td><td class="shift-digit">$</td>
            <td class="big-alpha">68</td><td class="big-alpha">44</td><td class="big-alpha">D</td>
            <td class="little-alpha">100</td><td class="little-alpha">64</td><td class="little-alpha">d</td>
        </tr>
        <tr>
            <td class="special">5</td><td class="special">05</td><td class="special non-printable">[ENQUIRY]</td>
            <td class="shift-digit">37</td><td class="shift-digit">25</td><td class="shift-digit">%</td>
            <td class="big-alpha">69</td><td class="big-alpha">45</td><td class="big-alpha">E</td>
            <td class="little-alpha">101</td><td class="little-alpha">65</td><td class="little-alpha">e</td>
        </tr>
        <tr>
            <td class="special">6</td><td class="special">06</td><td class="special non-printable">[ACKNOWLEDGE]</td>
            <td class="shift-digit">38</td><td class="shift-digit">26</td><td class="shift-digit">&amp;</td>
            <td class="big-alpha">70</td><td class="big-alpha">46</td><td class="big-alpha">F</td>
            <td class="little-alpha">102</td><td class="little-alpha">66</td><td class="little-alpha">f</td>
        </tr>
        <tr>
            <td class="special">7</td><td class="special">07</td><td class="special non-printable">[BELL]</td>
            <td class="shift-digit">39</td><td class="shift-digit">27</td><td class="shift-digit">'</td>
            <td class="big-alpha">71</td><td class="big-alpha">47</td><td class="big-alpha">G</td>
            <td class="little-alpha">103</td><td class="little-alpha">67</td><td class="little-alpha">g</td>
       </tr>
        <tr>
            <td class="special">8</td><td class="special">08</td><td class="special non-printable">[BACKSPACE]</td>
            <td class="shift-digit">40</td><td class="shift-digit">28</td><td class="shift-digit">(</td>
            <td class="big-alpha">72</td><td class="big-alpha">48</td><td class="big-alpha">H</td>
            <td class="little-alpha">104</td><td class="little-alpha">68</td><td class="little-alpha">h</td>
       </tr>
        <tr>
            <td class="special">9</td><td class="special">09</td><td class="special non-printable">[HORIZONTAL TAB]</td>
            <td class="shift-digit">41</td><td class="shift-digit">29</td><td class="shift-digit">)</td>
            <td class="big-alpha">73</td><td class="big-alpha">49</td><td class="big-alpha">I</td>
            <td class="little-alpha">105</td><td class="little-alpha">69</td><td class="little-alpha">i</td>
       </tr>
        <tr>
            <td class="special">10</td><td class="special">0A</td><td class="special non-printable">[LINE FEED]</td>
            <td>42</td><td>2A</td><td>*</td>
            <td class="big-alpha">74</td><td class="big-alpha">4A</td><td class="big-alpha">J</td>
            <td class="little-alpha">106</td><td class="little-alpha">6A</td><td class="little-alpha">j</td>
       </tr>
        <tr>
            <td class="special">11</td><td class="special">0B</td><td class="special non-printable">[VERTICAL TAB]</td>
            <td>43</td><td>2B</td><td>+</td>
            <td class="big-alpha">75</td><td class="big-alpha">4B</td><td class="big-alpha">K</td>
            <td class="little-alpha">107</td><td class="little-alpha">6B</td><td class="little-alpha">k</td>
       </tr>
        <tr>
            <td class="special">12</td><td class="special">0C</td><td class="special non-printable">[FORM FEED]</td>
            <td>44</td><td>2C</td><td>,</td>
            <td class="big-alpha">76</td><td class="big-alpha">4C</td><td class="big-alpha">L</td>
            <td class="little-alpha">108</td><td class="little-alpha">6C</td><td class="little-alpha">l</td>
       </tr>
        <tr>
            <td class="special">13</td><td class="special">0D</td><td class="special non-printable">[CARRIAGE RETURN]</td>
            <td>45</td><td>2D</td><td>-</td>
            <td class="big-alpha">77</td><td class="big-alpha">4D</td><td class="big-alpha">M</td>
            <td class="little-alpha">109</td><td class="little-alpha">6D</td><td class="little-alpha">m</td>
       </tr>
        <tr>
            <td class="special">14</td><td class="special">0E</td><td class="special non-printable">[SHIFT OUT]</td>
            <td>46</td><td>2E</td><td>.</td>
            <td class="big-alpha">78</td><td class="big-alpha">4E</td><td class="big-alpha">N</td>
            <td class="little-alpha">110</td><td class="little-alpha">6E</td><td class="little-alpha">n</td>
       </tr>
        <tr>
            <td class="special">15</td><td class="special">0F</td><td class="special non-printable">[SHIFT IN]</td>
            <td>47</td><td>2F</td><td>/</td>
            <td class="big-alpha">79</td><td class="big-alpha">4F</td><td class="big-alpha">O</td>
            <td class="little-alpha">111</td><td class="little-alpha">6F</td><td class="little-alpha">o</td>
       </tr>
        <tr>
            <td class="special">16</td><td class="special">10</td><td class="special non-printable">[DATA LINK ESCAPE]</td>
            <td class="digit">48</td><td class="digit">30</td><td class="digit">0</td>
            <td class="big-alpha">80</td><td class="big-alpha">50</td><td class="big-alpha">P</td>
            <td class="little-alpha">112</td><td class="little-alpha">70</td><td class="little-alpha">p</td>
       </tr>
        <tr>
            <td class="special">17</td><td class="special">11</td><td class="special non-printable">[DEVICE CONTROL 1]</td>
            <td class="digit">49</td><td class="digit">31</td><td class="digit">1</td>
            <td class="big-alpha">81</td><td class="big-alpha">51</td><td class="big-alpha">Q</td>
            <td class="little-alpha">113</td><td class="little-alpha">71</td><td class="little-alpha">q</td>
       </tr>
        <tr>
            <td class="special">18</td><td class="special">12</td><td class="special non-printable">[DEVICE CONTROL 2]</td>
            <td class="digit">50</td><td class="digit">32</td><td class="digit">2</td>
            <td class="big-alpha">82</td><td class="big-alpha">52</td><td class="big-alpha">R</td>
            <td class="little-alpha">114</td><td class="little-alpha">72</td><td class="little-alpha">r</td>
       </tr>
        <tr>
            <td class="special">19</td><td class="special">13</td><td class="special non-printable">[DEVICE CONTROL 3]</td>
            <td class="digit">51</td><td class="digit">33</td><td class="digit">3</td>
            <td class="big-alpha">83</td><td class="big-alpha">53</td><td class="big-alpha">S</td>
            <td class="little-alpha">115</td><td class="little-alpha">73</td><td class="little-alpha">s</td>
       </tr>
        <tr>
            <td class="special">20</td><td class="special">14</td><td class="special non-printable">[DEVICE CONTROL 4]</td>
            <td class="digit">52</td><td class="digit">34</td><td class="digit">4</td>
            <td class="big-alpha">84</td><td class="big-alpha">54</td><td class="big-alpha">T</td>
            <td class="little-alpha">116</td><td class="little-alpha">74</td><td class="little-alpha">t</td>
       </tr>
        <tr>
            <td class="special">21</td><td class="special">15</td><td class="special non-printable">[NEGATIVE ACKNOWLEDGE]</td>
            <td class="digit">53</td><td class="digit">35</td><td class="digit">5</td>
            <td class="big-alpha">85</td><td class="big-alpha">55</td><td class="big-alpha">U</td>
            <td class="little-alpha">117</td><td class="little-alpha">75</td><td class="little-alpha">u</td>
       </tr>
        <tr>
            <td class="special">22</td><td class="special">16</td><td class="special non-printable">[SYNCHRONOUS IDLE]</td>
            <td class="digit">54</td><td class="digit">36</td><td class="digit">6</td>
            <td class="big-alpha">86</td><td class="big-alpha">56</td><td class="big-alpha">V</td>
            <td class="little-alpha">118</td><td class="little-alpha">76</td><td class="little-alpha">v</td>
       </tr>
        <tr>
            <td class="special">23</td><td class="special">17</td><td class="special non-printable">[END OF TRANS. BLOCK]</td>
            <td class="digit">55</td><td class="digit">37</td><td class="digit">7</td>
            <td class="big-alpha">87</td><td class="big-alpha">57</td><td class="big-alpha">W</td>
            <td class="little-alpha">119</td><td class="little-alpha">77</td><td class="little-alpha">w</td>
       </tr>
        <tr>
            <td class="special">24</td><td class="special">18</td><td class="special non-printable">[CANCEL]</td>
            <td class="digit">56</td><td class="digit">38</td><td class="digit">8</td>
            <td class="big-alpha">88</td><td class="big-alpha">58</td><td class="big-alpha">X</td>
            <td class="little-alpha">120</td><td class="little-alpha">78</td><td class="little-alpha">x</td>
       </tr>
        <tr>
            <td class="special">25</td><td class="special">19</td><td class="special non-printable">[END OF MEDIUM]</td>
            <td class="digit">57</td><td class="digit">39</td><td class="digit">9</td>
            <td class="big-alpha">89</td><td class="big-alpha">59</td><td class="big-alpha">Y</td>
            <td class="little-alpha">121</td><td class="little-alpha">79</td><td class="little-alpha">y</td>
       </tr>
        <tr>
            <td class="special">26</td><td class="special">1A</td><td class="special non-printable">[SUBSTITUTE]</td>
            <td>58</td><td>3A</td><td>:</td>
            <td class="big-alpha">90</td><td class="big-alpha">5A</td><td class="big-alpha">Z</td>
            <td class="little-alpha">122</td><td class="little-alpha">7A</td><td class="little-alpha">z</td>
       </tr>
        <tr>
            <td class="special">27</td><td class="special">1B</td><td class="special non-printable">[ESCAPE]</td>
            <td>59</td><td>3B</td><td>;</td>
            <td>91</td><td>5B</td><td>[</td>
            <td>123</td><td>7B</td><td>{</td>
       </tr>
        <tr>
            <td class="special">28</td><td class="special">1C</td><td class="special non-printable">[FILE SEPARATOR]</td>
            <td>60</td><td>3C</td><td>&lt;</td>
            <td>92</td><td>5C</td><td>\</td>
            <td>124</td><td>7C</td><td>|</td>
       </tr>
        <tr>
            <td class="special">29</td><td class="special">1D</td><td class="special non-printable">[GROUP SEPARATOR]</td>
            <td>61</td><td>3D</td><td>=</td>
            <td>93</td><td>5D</td><td>]</td>
            <td>125</td><td>7D</td><td>}</td>
       </tr>
        <tr>
            <td class="special">30</td><td class="special">1E</td><td class="special non-printable">[RECORD SEPARATOR]</td>
            <td>62</td><td>3E</td><td>&gt;</td>
            <td>94</td><td>5E</td><td>^</td>
            <td>126</td><td>7E</td><td>~</td>
       </tr>
        <tr>
            <td class="special">31</td><td class="special">1F</td><td class="special non-printable">[UNIT SEPARATOR]</td>
            <td>63</td><td>3F</td><td>?</td>
            <td>95</td><td>5F</td><td>_</td>
            <td class="special">127</td><td class="special">7F</td><td class="special non-printable">[DEL]</td>
       </tr>
    </tbody>
</table>
