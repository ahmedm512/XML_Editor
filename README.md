# XML_Editor


Background 



XML (eXtensible Markup Language) is a format to represent
data. In this project we will work with XML files. This project is a Python
based project using the GUI you can select the XML file and check errors in
this file like if a missing “<” or “ >” and solve this error, check the
consistency like any missing open or closed tags and not matched tags and print
all the errors to the user. Have a Prettifying the XML file option, it set the
indentation to make the file well formatted. Convert the XML file to JSON file
option, JavaScript Object Notation (JSON) is a format to represent data JSON is
less verbose and faster. Have a minifying option. Because of  the newline and spaces increase the XML file
size. This option to delete the spaces and newlines to compress the file. In
the XML file, You can know the number of synsets and the user can enter a word
to know the definition of this word. To finalize the project we studied first
the XML notation and a lot about data structure specially tree and stack . 



implementation details

this project is a python-based project the GUI made by
Python Tkinter. Next we will explain each feature and how we implemented it.



1.      
  
  
   
   
   
   
   
   
   
   
   
   
   
   
  
  
  
 
  
  
 


 
 
Parsing XML: 

first we takes the input file from the GUI and get the input line by line, if
line is empty, the program will delete this line. Then lines passed to function
get_type. It will check open tags, closed tags and body. When it find a tag, it
appends to list called types an element of type dict with the keys (type-
nametag-line number- attr- has body- body) 



 part of get_type function  that used in second picture   part of code 
to show how we make the type list



 



 



 



 



 



2.      Check validation

in XML validation function it takes types and loop for each tag in types if it
finds an open tag, it will push it to stack. If it is a close tag, it will
check if the tag name is in the stack, if it exist, pop the open tag from the
stack. Else, returns XML is not valid. If a body exist, check if the stack is
not empty, else, returns XML is not valid.




 
  



Output
that XML is valid



 



 



 




 

 




part of the function check validation              how we print in GUI



 



 



3.      Error check

in error check module it takes lines and check if line doesn’t end with “>
“, it appends the element in list of errors it takes line number and the error.
check if line doesn’t start with “< “, it appends the element in list of
errors it takes line number and the error. Then we loop for each tag in types,
if it’s a self-closing tag, we check if open stack is not empty, else append
error in validate list. Check if tag is open tag we append this tag in open
tags stack.

if tag is close tag we append to close tag stack. Check if open tag has a close
tag. Else, append error in validate list. then Check if the closed tag has an
open tag. Else append error in validate list. This module return validate list
and error list to print it using the GUI.




 



 




Screenshots from error check module and what we return.






 
 
 




Screenshot
from GUI                                              
how we print errors in the GUI







 



4.      Convert to JSON: 

to implement this method we use the idea of trees , we create a class called
node with two attributes : data and an empty list called children now each node
of this tree has a number of children , now we need to insert these nodes.

we have a list of all tags types in a list called types ,at the beginning  we loop in this list till we find our first
opening tag and we make it our root and we push it to a stack .

in the next iteration if the tag type is also opening tag we insert it to our
tree by passing it’s data and it’s parent which is the top of the stack, after
inserting this new node we push it to the stack.



If we find
a closing tag and it’s name is similar to the top of the stack we pop the top
of the stack, if it has a different a name so this xml is not valid and an
error occurs .



Now we have
the xml file represented as a tree and we can traverse the tree after
converting each node to the equivalent json (print the tag name
between double quote then print it’s attributes and body ) using a method
called PrintTree in Node class.


 

 




Example of
the tree implemented                            
create our tree












 
 
 




The JSON
file generated for synset                             XML code for this
synset



 



 



 



Other
example with big file


 
 
 




 



5.      Number of synsets
in the file:
using our tree we look for nodes that have children and all it’s children are
leaves(not parents to any nodes) , we start searching with our root and a
counter set to zero to return the number of synsets.



If the node
has no children we return 0 if it has we loop in it’s children to check if they
all leaves if so we return 1 if not we return 0 then we move to the next node
and do the same thing as before .



At the end
of this operation we return a counter that holds the number of synsets in our
xml file.



This method
is named synset_no in class node



c
 
 



              count number of synset



 




 




              Printing number of synset in GUI



 




 




              The XML file and the number of
synsets



 



6.     
 Definition of a word:
using our tree we search for the tag that it’s body holds this word if we find
this node we now know that the definition we are looking for is included in
this synset so we start searching in it’s siblings till we find a node that
holds a tag named def then print it’s body.

This method is named definition in class node




 




The function that get the definition




 




Example of getting word
definition 



7.      Prettify:

here we have a list called prettify initialized by zero. Then we loop for each
tag in types. if tag is open tag we add 1 in the prettify list at index equal
line number of tag. If tag is close tag subtract 1  in the prettify list at index equal line
number. The number “1” refer to indentation for each level. The function pretty
check the validation of the XML file using validation module. If valid we loop
on lines and prettify, the value in prettify list equal indentation for each line
then we print the XML file.




 
 
 




Before
prettifing                                                                         After
prettifing




 




Code that
makes prettifing 



 



8.   
Minify:



This function
compresses XML documents. It removes new lines \n, deletes spaces and
tabs to make XML take least amount of space.

it’s simple, here we have a list of lines, we loop for each line and print all
in the same line.




 
 



              Code that make minifying




 




After minifying




 




Before minifying



Complexity of operations

 











 
  
  Operation


  
  
  complexity


  
 
 
  
  Parsing
  XML:


  
  
  O(
   
  )


  
 
 
  
  Check
  consistency


  
  
  O(
   
  )


  
 
 
  
  Error
  check


  
  
  O(
   
  )


  
 
 
  
  Convert
  to JSON


  
  
  O(
   
  )


  
 
 
  
  Number
  of synsets


  
  
  O(n)


  
 
 
  
  Definition of a word:


  
  
  O(n)


  
 
 
  
  Prettify:


  
  
  O(
   
  )


  
 
 
  
  Minify:


  
  
  O(n)


  
 



 



Refrences: 

[1] Tkinter GUI Application Development HOTSHOT by Bhaskar
Chaudhary  



[2] Data Structures and Algorithms Using Python by Rance D.
Necaise 



[3] Python Crash Course: A Hands-On, Project-Based
Introduction to Programming by Eric Matthes



[4]
Learning XML, Second Edition Second Edition by Erik T. Ray
