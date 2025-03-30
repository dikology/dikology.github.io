---
type: basic
id: 0211
tags:
  - dsa
created: March 30
modified: March 30
---

**Front:** what is a hash table?

**Back:**
A hash table (commonly referred to as hash map) a data structure that implements an associative array abstract data type, a structure that can map keys to values. A hash table uses a hash function on an element to compute an index, also called a hash code, into an array of buckets or slots, from which the desired value can be found. During lookup, the key is hashed and the resulting hash indicates where the corresponding value is stored.

Hashing is the most common example of a space-time tradeoff. Instead of linearly searching an array every time to determine if an element is present, which takes O(n) time, we can traverse the array once and hash all the elements into a hash table. Determining if the element is present is a simple matter of hashing the element and seeing if it exists in the hash table, which is O(1) on average.

In the case of hash collisions, there are a number of collision resolution techniques that can be used. You will unlikely be asked about details of collision resolution techniques in interviews,

Separate chaining - A linked list is used for each value, so that it stores all the collided items.
Open addressing - All entry records are stored in the bucket array itself. When a new entry has to be inserted, the buckets are examined, starting with the hashed-to slot and proceeding in some probe sequence, until an unoccupied slot is found

- Remember it is a reference to where it is saved in space // this means they are orderless

[[data structures and algorithms]]