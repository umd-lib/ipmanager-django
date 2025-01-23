# Documentation for the IP Containment Check Method Re-Implementation

## Flowchart

This diagram depicts the high-level sequence of steps that the code performs
when a user asks to check if a single IP address is in a specific group.

```mermaid
    flowchart TD
        Start --> user_input --> check1 --> convert --> call_collect --> create_sets --> loop1 --> populate_internal --> loop2 --> check_relation
        check_relation-- Yes --> modify_included --> call_collect
        check_relation --> return_collect --> return_check1 --> End
        check_relation-- No --> modify_excluded --> call_collect
        
        user_input[User enters a single IP address, a string, as the ip parameter for the check API view. A reference to the specific group object is provided.]
        check1[The code calls the group's contains method, passing the IP address to the method and a reference to group as the current group.]
        convert[The IP address is converted into a Cidr object.]
        call_collect[Call the collect method on the current group.]
        create_sets[Create 3 empty CidrSets: included, excluded, and internal.]
        loop1[Loop through each IPRange in the list of IPRanges belonging to the current group.]
        populate_internal[Add each IPRange's value as a Cidr object to the internal set.]
        loop2[Loop through each Relation in the list of Relations where the subject attribute matches the current group.]
        check_relation{Is the current Relation an INCLUSION relation?}
        modify_included[Call the collect method on the relation's object group, and add that to the current group's included set.]
        modify_excluded[Call the collect method on the relation's object group, and add that to the current group's excluded set.]
        return_collect[Return the CidrSet created from union of internal and included sets minus everything from the external set.]
        return_check1[Perform the containment check of the Cidr object of the IP address and the CidrSet returned from the collect method.]
```