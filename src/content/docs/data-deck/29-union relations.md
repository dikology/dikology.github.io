---
type: basic
id: 0229
title: Union Relations
description: This macro combines via `union all` an array of [Relations](https://docs.getdbt.com/docs/writing-code-in-dbt/class-reference/#relation), even when columns have differing orders in each Relation, and/or some columns are missing from some relations. Any columns exclusive to a subset of these relations will be filled with `null` where not present. A new column (`_dbt_source_relation`) is also added to indicate the source for each record.
tags:
  - dbt
created: January 10
modified: March 30
---

**Front:**
This macro combines via `union all` an array of [Relations](https://docs.getdbt.com/docs/writing-code-in-dbt/class-reference/#relation), even when columns have differing orders in each Relation, and/or some columns are missing from some relations. Any columns exclusive to a subset of these relations will be filled with `null` where not present. A new column (`_dbt_source_relation`) is also added to indicate the source for each record.

**Back:**

```
{{ dbt_utils.union_relations(
    relations=[ref('my_model'), source('my_source', 'my_table')],
    exclude=["_loaded_at"]
) }}
```

[[dbt]]