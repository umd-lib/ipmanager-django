# ERD For Ruby version of IPManager

```mermaid
    erDiagram
    Groups ||--o{ IPRanges : has
    Relations o{--|| Groups : subject
    Relations o{--|| Groups : object

    Groups {
        integer id PK "auto-generated"
        string key UK "mandatory"
        string name UK "mandatory"
        string description
        string notes
        boolean export "default = false, mandatory" 
        datetime created_at "auto-generated, mandatory"
        datetime updated_at "auto-generated, mandatory"
    }

    IPRanges {
        integer group_id PK,FK 
        string value PK
        datetime created_at "auto-generated, mandatory"
        datetime updated_at "auto-generated, mandatory"
    }

    Relations {
        integer subject_id PK, FK
        integer object_id PK, FK
        integer relation "mandatory"
        datetime created_at "auto-generated, mandatory"
        datetime updated_at "auto-generated, mandatory"
    }
    
```
## Additional Information
* All of the datetime fields, such as created_at and updated_at, should have a precision of 6 and they are non-null.
### Groups
* The key and name fields are indexed, which means that they make it easy for lookup.