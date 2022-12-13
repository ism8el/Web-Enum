# Web-Enum

This python script is a website recognition script that has several functions:
* It detects misconfigurations on websites.
* He scans the website to discover its tree structure.
* It displays the status code of the pages.
* It tries to bypass 403 (Forbidden) pages using many patterns.

The script is entirely in python and is very easy to use in addition to being fast and light.

You can also customize the following elements:

* Customize cookies.
* Customize the User Agent.

## Usage

>chmod +x web-enum.py\
>./web-enum.py http://example.fr/

or

>python3 web-enum.py http://example.fr/


By default the script ignores files in png, jpg, svg, jpeg, ico, css, js, pdf, txt, gif, etc...\
If you still want to list them, use the "all" argument


>chmod +x web-enum.py\
>./web-enum.py http://example.fr/ all

or

>python3 web-enum.py http://example.fr/ all

## Screenshots
![](https://github.com/ism8el/Web-Enum/blob/main/web-enum.png)
