# ERD For Ruby version of IPManager

```mermaid
    erDiagram
    Group ||--o{ IPRange : has
    Relation o{--|| Group : subject
    Relation o{--|| Group : object

    Group {
        integer id PK "auto-generated, mandatory"
        string key UK "mandatory"
        string name UK "mandatory"
        string description
        string notes
        boolean export "default = false, mandatory" 
        datetime created_at "auto-generated, mandatory"
        datetime updated_at "auto-generated, mandatory"
    }

    IPRange {
        integer id PK "auto-generated, mandatory"
        integer group_id FK "mandatory"
        string value "mandatory"
        datetime created_at "auto-generated, mandatory"
        datetime updated_at "auto-generated, mandatory"
    }

    Relation {
        integer id PK "auto-generated, mandatory"
        integer subject_id FK "mandatory"
        integer object_id FK "mandatory"
        integer relation "mandatory"
        datetime created_at "auto-generated, mandatory"
        datetime updated_at "auto-generated, mandatory"
    }
    
```
## Additional Information

* All of the datetime fields, such as created_at and updated_at, should have a
    precision of 6 and they are non-null.

### Group

* The key and name fields are indexed, which means that they make it easy for lookup.

### IPRange

* The group_id field is indexed.
* The combination of the group_id and value fields is indexed and unique.

### Relation

* The subject_id and object_id fields are indexed.
