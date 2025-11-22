CREATE TABLE identity_mappings (
  mapping_id VARCHAR(36) NOT NULL,                    
  lif_organization_id VARCHAR(255) NOT NULL,
  lif_organization_person_id VARCHAR(255) NOT NULL,                                                   
  target_system_id VARCHAR(255) NOT NULL,
  target_system_person_id_type VARCHAR(100) NOT NULL,                                      
  target_system_person_id VARCHAR(255) NOT NULL,                                      
  PRIMARY KEY (mapping_id),
  CONSTRAINT uq_identity_mapping UNIQUE(lif_organization_id, lif_organization_person_id, target_system_id, target_system_person_id_type)                                   
);
