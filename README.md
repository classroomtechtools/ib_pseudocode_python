# IB DP Computer Science Pseudocode

Write pseudocode in repl.it. Execute it as Python. Learn Paper 1, learn computational thinking.

## Quickstart

### Executing code

- Navigate to the [base repl](https://repl.it/@adammorris/InputPseudocode).
- Create a new file called "new" (this will also fork the repl and make it yours)
- Enter pseudocode (for example `output "Hello World"`)
- In the interpreter, enter `execute('new')` and the code in the file `new.pseudo` executes
- In the interpreter, enter `transpile('new')` and it outputs the code that would be executed

### Why use it

Practice writing pseudocode by actually running it, ensuring that it works. It also could be a way to learn Python.

The IB Pseudocode (formally specified [here](https://ib.compscihub.net/wp-content/uploads/2015/04/IB-Pseudocode-rules-more.pdf)) is actually quite close to Python; it only takes about 200 lines of Python code to convert (transpile) it.  This is why it might be a general purpose way to get your feet wet into programming.

## Handling Data Structures

It is common for the IB, and for other programming classes, to specify a datastructure that you are going to work with. For example:

1. Add 10 items to your list called `MYLIST`
2. You have an list of names called `STUDENTS` that contain 20 string values
3. You have a list called `WHOLENUMBERS` of 100 random integers from 1 to 100 (inclusive)
4. You have a collection of names called `ANGELS` that have an unknown number of values

In the actual paper, when giving answers, you won't have to "create" these objects. You can write code as if they are already set up correctly. However, if you want to actually code with them, we need to create a way to be able to make them in our environment (repl.it website), even though we don't have to in the target environment (the actual exam). 

A link to the [specified datastructures](https://computersciencewiki.org/images/c/c6/IB-Pseudocode-rules.pdf)

### Creating and Using Lists, Collections (SL + HL)

For example, in **#1** above, you need some way of creating a list called `MYLIST` that I can call `addItem` in order to add the items. In this case, we just need to use this:

```MYLIST = List()```

And then you can do this later in your program:

```MYLIST[0] = "First element"```

In Python, that wouldn't work, but that's exactly how you're supposed to write in IB Pseudocode. The provided `List` classes sorts that out for you.

In example **#2** above, you could do this:

```
STUDENTS = List()
STUDENTS[0] = "Aaron"
STUDENTS[1] = "Adam"
...
```

and so on, but that would be painful. Instead, wouldn't it be great if we could just make a new file and type the names we need on twenty lines? You can do that:

```
STUDENTS = List.from_file('students.txt')
```

Make a new file inside the repl and type a name per line. This kind of code is known as a *convenience function*, or also a *constructor*. It creates the data type for you, based on parameters you give it.

For **#4** above, you do it with another convenience function:

```
WHOLENUMBERS = List.from_x_integers(100, min=1, max=100)
```

Finally, #5 needs a different data type, known as a Collection:

``` ANGELS = Collection() ```

The same sort of convenience functions are available to you.


### Stacks and Queues (HL)

```
MYSTACK = Stack()
MYSTACK = Stack.from_array([1, 2])
```

```
MYQUEUE = Queue()
MYQUEUE = Queue.from_array([1, 2])
```

## Implementation Details

If you are curious how this all works:

- The repo is written as a command line utility 
- The repl downloads the repo if not present
- The repl executes everything through the command line on the server
- The transpiling is just a bunch of regex

Why did I do it that way?

- Since it downloads the repo from github, it's portable: I can improve it and all projects that use it will reap the benefits.
- I can use this technique in further ways
