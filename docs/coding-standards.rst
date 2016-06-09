===========================================
Coding Standards to Accommodate Obfuscating
===========================================
Some changes to coding style must be made for the obfuscator to work.

1. Start doc strings with a triple quote AND text; do not start a doc string with a standalone triple quote. Doc strings CAN terminate with a standalone triple quote. For example,
    use::

        """My doc string."""

    or::

        """My doc string.

        This is what this function does.
        """

    not::

        """
        My doc string.
        """

    Both double- and single-quotes are accepted for the triple quotes.

    Doc strings with standalone triple quotes (as in the last example) are copied in to the obfuscated program without change.

    To assign a multi-line string to a variable, use a triple-quoted string. For example::

        myvar = """I want this
        whole string to be assigned to myvar,
        line breaks and all."""

2. Use the platform directives "# {+<platform>}" (to begin a block) and "# {-<platform>}" (to end a block) to include code specifically for a platform. Code in the block will be copied and obfuscated only for the specified platform of when no platform is specified. For example,
    use::

        # {+android}
        if android_level == 3:
            process.quit()
        # {-android}

    to include the two android-specific code lines in the android build and to exclude them from ios builds.
3. Put Kivy code in separate .kv files; don't embed the Kivy language code within the .py files. That is, don't use Builder.load_string, since strings are not obfuscated. The .kv extension is used to direct those Kivy language lines to a separate parser with rules specifically for Kivy, so those files can be obfuscated too.
4. Make sure every method has an executable line (even if it's just **pass**). For example, a Python program with a method that has only comments will load fine on a Mac, but will not load in iOS; and in this case, iOS gives no clue as to why the program fails to load.
