# IP Manager Model in Django

```mermaid
erDiagram

    GROUP ||--o{IP_Range: has
    GROUP ||--o{Relation: subject
    GROUP ||--o{Relation: object
    GROUP {
        integer id  PK "auto-generated, mandatory"
        string key  UK "mandatory"
        string name UK "mandatory"
        string description 
        string notes
        boolean export "mandatory"
        datetime created "auto-generated, mandatory"
        datetime modified "auto-generated, mandatory"
        }
    IP_Range {
        int group FK "mandatory"
        string value "mandatory"
        int id PK "auto-generated, mandatory"
        datetime created "auto-generated, mandatory"
        datetime modified "auto-generated, mandatory"
            }
    Relation {
        integer id PK "auto-generated, mandatory"
        integer subject FK "mandatory"
        integer object FK "mandatory"
        integer relation "mandatory"
        datetime created "auto-generated, mandatory"
        datetime modified "auto-generated, mandatory"
            }
```
## Additional Information


### Group

* The key and name fields are indexed, which means that they make it easy for lookup.

### IPRange

* Group and value are composite keys

### Relation

* subject and object are composite foreign keys
