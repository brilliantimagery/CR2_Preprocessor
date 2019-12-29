# CR2 Preprocessor
Moves, batch process, and compresses [dual-iso](https://www.magiclantern.fm/forum/?topic=7139.0) cr2 raw image files.

## Installation
See [Brilliant Imagery](http://www.brilliantimagery.org/) for more info and binaries (versions of the software that you can just double click to run rather than setup) (hopefully it'll be up by the time you see this).

If you don't already have `pipenv`, install it. Note, it shouldn't be installed into a vertual environment.

```
$ pip install pipenv
```

Clone the reposatory to a working directory.

```
$ git clone https://github.com/brilliantimagery/CR2_Preprocessor.git
```

From the top level within the project, create the virtual environment and install the dependencies.

```
$ pipenv install
```

[Adobe DNG Converter](https://helpx.adobe.com/photoshop/using/adobe-dng-converter.html) also needs to be installed and the location of the "Adobe DNG Converter.exe" file needs to be known. It may be at "C:/Program Files (x86)/Adobe/Adobe DNG Converter.exe".

## Run the App

From the top level within the project, start the virtual environment.

```
$ pipenv shell
```

Start the app.

```
$ python run.py
```

Set the location of the "Adobe DNG Converter.exe" file.

Set the location of the files that are to be converted.

Set the location of where the output file are to be saved to.

## Testing
Being a small stop-gap project, there isn't currently any testing. If people start using it, that'll likely change.

## Apple Support
I have Windows computers so I support them. If you have an Mac and would like to help bring support to them, let me know!

## Included Dependencies
[cr2hdr](https://magiclantern.fm/), [dcraw](https://www.dechifro.org/dcraw/), and [exiftool](https://exiftool.org/) are all included dependencies. See their respective sites for more info, and thank you for your work.
