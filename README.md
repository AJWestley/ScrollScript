# ScrollScript: A Comprehensive Language Guide

## Introduction

Welcome to ScrollScript, a unique programming language designed with a blend of clear functionality and thematic flair. This guide provides a comprehensive overview of ScrollScript's features, syntax, and operators, enabling you to effectively develop applications within its distinct paradigm.

## Core Concepts

ScrollScript introduces specific terminology to enhance its thematic appeal:
* **Runes**: Variables that store data.
* **Incantations**: Functions that encapsulate reusable blocks of code.
* **Casting**: The process of calling an incantation.
* **Sealed Runes**: Constant variables, immutable after declaration.

## Language Features

### 1. Variables and Constants

ScrollScript provides mechanisms for declaring both mutable variables and immutable constants.

* **Variable Declaration**: Declared using the `rune` keyword.
    ```scrollscript
    rune my_variable = 10;
    rune another_variable; ~~ Declares without initial assignment
    ```
* **Constant Declaration**: Declared using the `sealed rune` keywords. Once declared, their value cannot be changed.
    ```scrollscript
    sealed rune MY_CONSTANT = "immutable_value";
    ```
* **Assignment**: Values are assigned to mutable runes using the `=` operator.
    ```scrollscript
    my_variable = 20;
    ```
* **Deletion**: Runes can be removed from scope using the `dispel` keyword.
    ```scrollscript
    dispel my_variable;
    ```
* **Sealing (Making a Constant)**: An existing mutable rune can be converted into a sealed rune using the `seal` keyword.
    ```scrollscript
    rune dynamic_rune = 5;
    seal dynamic_rune; ~~ dynamic_rune is now constant
    ```

### 2. Operators

ScrollScript offers a rich set of operators for various computations and comparisons.

#### a. Increment and Decrement Operators

* **Simple Increments**: Modify a numerical rune by 1.
    * `++`: Increment by one.
    * `--`: Decrement by one.
    ```scrollscript
    my_number++;
    another_number--;
    ```
* **Compound Increments**: Combine an arithmetic operation with assignment.
    * `+=`: Add and assign.
    * `-=`: Subtract and assign.
    * `*=`: Multiply and assign.
    * `/=`: Divide and assign.
    * `%=`: Modulo and assign.
    * `^=`: Exponentiate and assign.
    * `/+=`: Floor division add and assign.
    * `/-=`: Floor division subtract and assign.
    * `/*=`: Floor division multiply and assign.
    * `//=`: Integer division and assign.
    * `/^=`: Floor division exponentiate and assign.
    * `/%=`: Floor division modulo and assign.
    * `^+=`: Ceiling add and assign.
    * `^-=`: Ceiling subtract and assign.
    * `^*=`: Ceiling multiply and assign.
    * `^/=`: Ceiling divide and assign.
    * `^^=`: Ceiling exponentiate and assign.
    * `~%=`: Ceiling modulo and assign.
    * `~+=`: Round add and assign.
    * `~-=`: Round subtract and assign.
    * `~*=`: Round multiply and assign.
    * `~/=`: Round divide and assign.
    * `~^=`: Round exponentiate and assign.
    * `~%=`: Round modulo and assign.

    ```scrollscript
    total_score += 10;
    result_value /= 2.5;
    floor_result /= 2.5; ~~ Effectively floor(result_value / 2.5)
    ```

#### b. Arithmetic Operators 

* `+`: Addition.
* `-`: Subtraction.
* `*`: Multiplication.
* `/`: Division.
* `%`: Modulo.
* `^`: Exponentiation.
* `//`: Integer Division.
* `/+, /-, /*, //, /%, /^`: Floor-based arithmetic operations (e.g., `/+` performs addition then floors the result).
* `^+, ^-, ^*, ^/, ^%, ^^`: Ceiling-based arithmetic operations (e.g., `^*` performs multiplication then applies ceiling to the result).
* `~+, ~-, ~*, ~/, ~%, ~^`: Rounding-based arithmetic operations (e.g., `~*` performs multiplication then rounds the result).

#### c. Comparison Operators

* `<`: Less than.
* `>`: Greater than.
* `<=`: Less than or equal to.
* `>=`: Greater than or equal to.
* `==`: Equal to.
* `!=`: Not equal to.

#### d. Logical Operators

* `&&` (AND): Logical AND.
* `||` (OR): Logical OR.
* `!` (NOT): Logical NOT.

#### e. Rounding Operators

* `~`: Round to the nearest integer.
* `/`: Floor (round down to the nearest integer).
* `^`: Ceiling (round up to the nearest integer).

### 3. Data Types

ScrollScript supports fundamental data types for numerical, textual, and boolean values.

* **`int`**: Integers.
* **`float`**: Floating-point numbers.
* **`string`**: Textual data.
* **`bool`**: Boolean values, represented by `Truthsung` (true) and `Falsehood` (false).

### 4. Input and Output

* **`reveal` (Print Statement)**: Displays information to the console.
    ```scrollscript
    reveal "Hello, ScrollScript!";
    ```
* **`listen` (Input Statement)**: Reads input from the user. Can be used with an optional prompt.
    ```scrollscript
    rune user_input = listen;
    rune prompted_input = listen "Enter your name: ";
    ```

### 5. Control Flow

Control flow statements dictate the order in which instructions are executed.

#### a. Conditional Statements

* **`foretell` (If-Elif-Else Statement)**: Executes blocks of code based on conditions.
    * `foretell (condition) { ... }`: The primary conditional block.
    * `shift (condition) { ... }`: Optional "else if" blocks.
    * `resolve { ... }`: Optional "else" block, executed if no preceding condition is met.

    ```scrollscript
    foretell (temperature > 25) {
        reveal "It's hot!";
    } shift (temperature < 10) {
        reveal "It's cold!";
    } resolve {
        reveal "The temperature is moderate.";
    }
    ```
* **`mayhaps` (Maybe Statement)**: Executes a block of code with a specified probability.
    * `mayhaps [(ratio)] { ... }`: The block will execute based on the provided ratio. If no ratio is given, the default is 0.5 (50%).
    * The `ratio` is defined as `INTEGER : INTEGER` (e.g., `1:3` for a 1 in 4 chance).

    ```scrollscript
    mayhaps (1:1) { ~~ 50% chance
        reveal "A coin flip landed heads!";
    }
    mayhaps (1:9) { ~~ 10% chance
        reveal "A rare event occurred!";
    }
    ```

#### b. Loop Statements

* **`cycle (rune var_name start -> end | step)` (For-Range Loop)**: Iterates a variable through a specified numerical range. The `step` is optional and defaults to 1.
    ```scrollscript
    cycle (rune i 1 -> 5) {
        reveal i;
    }
    cycle (rune j 10 -> 0 | 2) {
        reveal j;
    }
    ```
* **`cycle (lest condition)` (While Loop)**: Continuously executes a block as long as the specified `condition` is `Falsehood` (i.e., until the condition becomes `Truthsung`).
    ```scrollscript
    rune counter = 0;
    cycle (lest counter == 3) {
        reveal counter;
        counter++;
    }
    ```
* **`cycle (ad infinitum)` (Infinite Loop)**: Creates a loop that runs indefinitely unless explicitly interrupted.
    ```scrollscript
    cycle (ad infinitum) {
        reveal "Looping forever...";
        ~~ Use 'shatter' to break this loop.
    }
    ```
* **`cycle (rune item in collection)` (Foreach Loop)**: Iterates over each element in a collection (e.g., characters in a string).
    ```scrollscript
    rune my_string = "hello";
    cycle (rune char_val in my_string) {
        reveal char_val;
    }
    ```
* **`shatter` (Break Statement)**: Terminates the innermost loop.
* **`persist` (Continue Statement)**: Skips the rest of the current loop iteration and proceeds to the next.

### 6. Functions (Incantations)

ScrollScript supports user-defined functions, referred to as "incantations."

* **Declaration**: Defined using the `incantation` keyword, followed by the function name, parameters (each preceded by "~"), and a code block.
    ```scrollscript
    incantation greet ~name {
        reveal $"Hello, {name}!";
    }
    ```
* **Calling**: Incantations are invoked using the `cast` keyword, followed by the function name and arguments (surrounded by "~:" and ":~").
    ```scrollscript
    cast greet ~:"Alice":~;
    ```
* **Return Values**: Incantations can return values using the `proclaim` keyword.
    ```scrollscript
    incantation add_numbers ~num1 ~num2 {
        proclaim num1 + num2;
    }
    rune sum_result = cast add_numbers ~:5, 3:~;
    reveal sum_result;
    ```

### 7. Special Features

* **`FROM DAYS OF YORE` (Previous Value)**: Access the previous value of a rune after its last assignment.
    ```scrollscript
    rune x = 10;
    x = 20;
    reveal x from days of yore; ~~ Output: 10
    ```
* **Interpolated Strings**: Embed expressions directly within strings using `$"..."` syntax with `{}` for expressions.
    ```scrollscript
    rune item = "sword";
    rune quantity = 3;
    reveal $"You have {quantity} {item}s.";
    ```
* **`transmute` (Type Casting)**: Convert a value from one data type to another using the `transmute ... as DATA_TYPE` syntax.
    ```scrollscript
    rune my_int = 10;
    rune my_float = transmute my_int -> float;
    ```
* **`measure` (Length Expression)**: Determines the length of a string.
    ```scrollscript
    rune text = "Scroll";
    reveal measure text; ~~ Output: 6
    ```
* **Index Expression**: Access individual characters within a string using the `::` operator and an index.
    ```scrollscript
    rune word = "Magic";
    reveal word::0; ~~ Output: M
    ```

## Keywords Reference

* **Data Types**: `int`, `float`, `string`, `bool` 
* **Variable Management**: `rune`, `dispel`, `sealed`, `seal` 
* **Control Flow**: `foretell`, `shift`, `resolve`, `mayhaps`, `cycle`, `lest`, `betwixt` (for `in` in foreach loops), `ad`, `infinitum`, `shatter`, `persist` 
* **Input/Output**: `reveal`, `listen` 
* **Functions**: `incantation`, `cast`, `reclaim`
* **Other**: `transmute` (for casting), `measure`, `Truthsung` (boolean true), `Falsehood` (boolean false), `FROM DAYS OF YORE` (for previous value) 

## Conclusion

ScrollScript provides a robust set of features for general-purpose programming, wrapped in an engaging, thematic layer. By understanding its core concepts, operators, and control flow mechanisms, you can begin to write powerful and expressive code.