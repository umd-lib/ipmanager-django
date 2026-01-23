from djangosaml2.backends import Saml2Backend

def group_names(attributes: dict) -> set[str]:
    return {g.lower() for g in attributes.get('eduPersonEntitlement', ())}

class ModifiedSaml2Backend(Saml2Backend):
    
    def is_authorized(
        self,
        attributes: dict,
        attribute_mapping: dict,
        idp_entityid: str,
        assertion_info: dict,
        **kwargs,
    ) -> bool:
            return 'ipmanager-administrator' in group_names(attributes) or 'ipmanager-user' in group_names(attributes)
    
    
