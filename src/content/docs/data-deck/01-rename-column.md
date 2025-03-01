---
created: February 17
modified: February 17
title: Rename a Column
description: rename a column in SQL
type: basic
id: 0201
---
**Front:**
How to Rename a Column in SQL

**Back:**
To keep your database organized, you might need to change the names of the columns. To rename a column in SQL, you can use the ALTER TABLE statement with the RENAME COLUMN clause.

Here is the basic syntax:

```
ALTER TABLE table_name 
RENAME COLUMN old_column_name TO new_column_name;
```

For example, suppose you have a table called “tv\_show” with a column named “genre”. To rename this column to “category”, you would use the following SQL statement:

```
ALTER TABLE tv_show 
RENAME COLUMN genre TO category;
```

After executing this query, the column previously known as “genre” will now be called category. Note that renaming a column will not change the data stored in that column, but it will change the column’s name in the table schema.

If renaming doesn’t solve your problem, you can add a new column or [drop a column](https://www.coginiti.co/tutorials/beginner/drop-column/) from your table.