# Command line syntax

*@command* *argument1* *argument2* *...*

## Arguments

A single argument normally ends at the next space.

    @cmdone these are all different arguments

To create an argument containing spaces, the argument must be placed within quotations.

    @cmdone "this is a single argument"

### Span command arguments across multiple lines

The arguments for a single command normally end at the end of a line. However, by placing a backslash at the end of the line, the following line can also be used to specify arguments for the same command.

    @cmdone these are arguments for cmdone \
        these are more arguments for cmdone

### Referencing string variables

String variables can be referenced by using a dollar sign followed by curly brackets.

    @cmdone ${strvar}

At runtime, variable references are substituted by their corresponding values.

    # The variable name is strvar
    # The variable value is variabletext
    @var strvar variabletext

    # Here is a command that references the variable
    @cmdone ${strvar}

    # At runtime, the variable reference will be substituted by it's corresponding value
    # @cmdone variabletext

### Calling string functions

String functions can be called by using a dollar sign followed by parentheses. They essentially follow the same syntax as commands. However, they must be ended by a closing parenthesis.

    @cmdone $(func funcarg1 funcarg2)

To create an argument that contains a closing parenthesis, simply place the argument within quotes.

    @cmdone $(func "Not ) closed")

### Escape sequences

The backslash is used for escape sequences:
* \\n Newline
* \\t Horizontal Tab
* \\\\ Backslash
* \\" Double Quote
* \\b Backspace
* \\r Carriage Return
* \\a Audible Bell
* \\0 Null character
* \\$ Dollar sign
* \\# Hash symbol

The following escape sequences are for unicode characters
* \\xXX 8-bit unicode character (where XX is the hex value)
* \\uXXXX 16-bit unicode character (where XXXX is the hex value)

## Comments

A hash symbol indicates the start of a comment. When a comment is detected, the rest of the line is ignored.

    # Comment

    @cmdone argument # Comment after command

However, hash symbols within quoted arguments are not interpreted as comments.

    @cmdone "this # is not the start of a comment"

# What Can Be Done

## Printing to console

@print *message*

Prints a message to the console
* message: Message to print

Example:

    @print Hello world!

## Setting variables

@var *name* *value*

Sets the value of a variable
* name: Variable name
* value: Variable value

Example:

    @var pi 3.141592

## Creating files

@open *path*

Opens a file for writing. NOTE: Only one file can be open at a time
* path: Path of output file

@line *data*

Writes a single line to the currently open.
* data: Line data

@close

Closes the file that is currently open.

Example:

    @open ./sample.txt
    @line This is line 1
    @line This is line 2
    @line This is line 3
    @close