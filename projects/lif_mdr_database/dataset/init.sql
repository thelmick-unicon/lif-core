
DROP TYPE IF EXISTS public.datamodeltype;
DROP TYPE IF EXISTS public.constrainttype;
DROP TYPE IF EXISTS public.transformationltype;
DROP TYPE IF EXISTS public.expressionlanguagetype;
DROP TYPE IF EXISTS public.attributetype;
DROP TYPE IF EXISTS public.elementtype;
DROP TYPE IF EXISTS public.accesstype;
DROP TYPE IF EXISTS public.statetype;
DROP TYPE IF EXISTS public.datamodelelementtype;

CREATE TYPE public.datamodeltype AS ENUM
    ('BaseLIF', 'OrgLIF', 'SourceSchema', 'PartnerLIF');
	
CREATE TYPE public.constrainttype AS ENUM
    ('IntValueRange', 'DoubleValueRange', 'Length', 'MaxValue', 'MinValue');

CREATE TYPE public.transformationltype AS ENUM
    ('Copy', 'Expression');

CREATE TYPE public.expressionlanguagetype AS ENUM
    ('Python', 'Perl', 'C#', 'SQL', 'LIF_Pseudo_Code');

CREATE TYPE public.attributetype AS ENUM
    ('Source', 'Target');

CREATE TYPE public.elementtype AS ENUM
    ('Attribute', 'Entity','Constraint', 'Transformation');

CREATE TYPE public.accesstype AS ENUM
    ('Private', 'Public','Internal', 'Restricted');

CREATE TYPE public.statetype AS ENUM 
('Published', 'Draft', 'Work_In_Progress', 'Active', 'Inactive');

CREATE TYPE public.datamodelelementtype AS ENUM
    ('Attribute', 'Entity', 'ValueSet', 'ValueSetValues', 'TransformationsGroup', 'Transformations');

drop table if exists "Attributes" Cascade;
drop table if exists "ValueSets" Cascade;
drop table if exists "ValueSetValueMapping" Cascade;
drop table if exists "ValueSetValues" Cascade;
drop table if exists "Constraints" Cascade;
drop table if exists "DataModels" Cascade;
drop table if exists "Entities" Cascade;
drop table if exists "EntityAssociation" Cascade;
drop table if exists "EntityAttributeAssociation" Cascade;
drop table if exists "ExtInclusionsFromBaseDM" Cascade;
drop table if exists "ExtMappedValueSet" Cascade;
drop table if exists "TransformationsGroup" Cascade;
drop table if exists "TransformationAttributes" Cascade;
drop table if exists "Transformations" Cascade;
drop table if exists "DataModelConstraints" Cascade;


CREATE TABLE IF NOT EXISTS public."DataModels"
(
    "Id" bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "Name" character varying COLLATE pg_catalog."default" NOT NULL,
    "Description" text COLLATE pg_catalog."default",
    "UseConsiderations" text COLLATE pg_catalog."default",
    "Type" datamodeltype NOT NULL,
    "BaseDataModelId" bigint,
    "Notes" text COLLATE pg_catalog."default",
    "DataModelVersion" character varying COLLATE pg_catalog."default",
    "CreationDate" timestamp with time zone,
    "ActivationDate" timestamp with time zone,
    "DeprecationDate" timestamp with time zone,
    "Contributor" character varying COLLATE pg_catalog."default",
    "ContributorOrganization" character varying COLLATE pg_catalog."default",
    "Deleted" bool DEFAULT false NULL,
    "State" statetype DEFAULT 'Draft',
    "Tags" text COLLATE pg_catalog."default",
    CONSTRAINT "DataModels_pkey" PRIMARY KEY ("Id"),
    CONSTRAINT "unique_name_version" UNIQUE ("Name", "DataModelVersion"),
    CONSTRAINT "Fk_BaseDataModelId" FOREIGN KEY ("BaseDataModelId")
        REFERENCES public."DataModels" ("Id") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS public."Entities"
(
    "Id" bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "Name" character varying COLLATE pg_catalog."default" NOT NULL,
    "UniqueName" character varying COLLATE pg_catalog."default" NOT NULL,
    "Description" text COLLATE pg_catalog."default",
    "UseConsiderations" text COLLATE pg_catalog."default",
    "Required" character varying COLLATE pg_catalog."default",
    "Array" character varying COLLATE pg_catalog."default",
    "SourceModel" character varying COLLATE pg_catalog."default",
    "DataModelId" bigint NOT NULL,
    "Notes" text COLLATE pg_catalog."default",
    "CreationDate" timestamp with time zone,
    "ActivationDate" timestamp with time zone,
    "DeprecationDate" timestamp with time zone,
    "Contributor" character varying COLLATE pg_catalog."default",
    "ContributorOrganization" character varying COLLATE pg_catalog."default",
    "Extension" BOOLEAN NOT NULL DEFAULT FALSE,
    "ExtensionNotes" character varying COLLATE pg_catalog."default",
    "Deleted" bool DEFAULT false NULL,
    "Tags" text COLLATE pg_catalog."default",
    CONSTRAINT "Entities_pkey" PRIMARY KEY ("Id"),
    CONSTRAINT "Fk_DataModelId" FOREIGN KEY ("DataModelId")
        REFERENCES public."DataModels" ("Id") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS public."EntityAssociation"
(
    "Id" bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "ParentEntityId" bigint NOT NULL,
    "ChildEntityId" bigint NOT NULL,
    "Relationship" text COLLATE pg_catalog."default",
    "Placement" text COLLATE pg_catalog."default",
    "Notes" text COLLATE pg_catalog."default",
    "CreationDate" timestamp with time zone,
    "ActivationDate" timestamp with time zone,
    "DeprecationDate" timestamp with time zone,
    "Contributor" character varying COLLATE pg_catalog."default",
    "ContributorOrganization" character varying COLLATE pg_catalog."default",
    "Deleted" bool DEFAULT false NULL,
    "Extension" BOOLEAN NOT NULL DEFAULT FALSE,
    "ExtensionNotes" character varying COLLATE pg_catalog."default",
    "ExtendedByDataModelId" bigint,
    CONSTRAINT "EntityAssociation_pkey" PRIMARY KEY ("Id"),
    CONSTRAINT "Fk_ChildEntityId" FOREIGN KEY ("ChildEntityId")
        REFERENCES public."Entities" ("Id") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Fk_ParentEntityId" FOREIGN KEY ("ParentEntityId")
        REFERENCES public."Entities" ("Id") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS public."ValueSets"
(
    "Id" bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "Name" character varying COLLATE pg_catalog."default" NOT NULL,
    "Description" text COLLATE pg_catalog."default",
    "UseConsiderations" text COLLATE pg_catalog."default",
    "DataModelId" bigint NOT NULL,
    "Notes" text COLLATE pg_catalog."default",
    "CreationDate" timestamp with time zone,
    "ActivationDate" timestamp with time zone,
    "DeprecationDate" timestamp with time zone,
    "Contributor" character varying COLLATE pg_catalog."default",
    "ContributorOrganization" character varying COLLATE pg_catalog."default",
    "Extension" BOOLEAN NOT NULL DEFAULT FALSE,
    "ExtensionNotes" character varying COLLATE pg_catalog."default",
    "Deleted" bool DEFAULT false NULL,
    "Tags" text COLLATE pg_catalog."default",
    CONSTRAINT "ValueSets_pkey" PRIMARY KEY ("Id"),
    CONSTRAINT "Fk_DataModelId" FOREIGN KEY ("DataModelId")
        REFERENCES public."DataModels" ("Id") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS public."ValueSetValues"
(
    "Id" bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "ValueSetId" bigint NOT NULL,
    "Description" text COLLATE pg_catalog."default",
    "UseConsiderations" text COLLATE pg_catalog."default",
    "Value" character varying COLLATE pg_catalog."default" NOT NULL,
    "ValueName" text COLLATE pg_catalog."default",
    "OriginalValueId" bigint,
    "Source" character varying COLLATE pg_catalog."default",
    "Notes" text COLLATE pg_catalog."default",
    "CreationDate" timestamp with time zone,
    "ActivationDate" timestamp with time zone,
    "DeprecationDate" timestamp with time zone,
    "Contributor" character varying COLLATE pg_catalog."default",
    "ContributorOrganization" character varying COLLATE pg_catalog."default",
    "Extension" BOOLEAN NOT NULL DEFAULT FALSE,
    "ExtensionNotes" character varying COLLATE pg_catalog."default",
    "Deleted" bool DEFAULT false NULL,
    "DataModelId" bigint NOT NULL,
    CONSTRAINT "ValueSetValues_pkey" PRIMARY KEY ("Id"),
    CONSTRAINT "Fk_OriginalValueId" FOREIGN KEY ("OriginalValueId")
        REFERENCES public."ValueSetValues" ("Id") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Fk_ValueSetId" FOREIGN KEY ("ValueSetId")
        REFERENCES public."ValueSets" ("Id") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Fk_DataModelId" FOREIGN KEY ("DataModelId")
        REFERENCES public."DataModels" ("Id") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS public."Attributes"
(
    "Id" bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "Name" character varying COLLATE pg_catalog."default" NOT NULL,
    "UniqueName" character varying COLLATE pg_catalog."default" NOT NULL,
    "Description" text COLLATE pg_catalog."default",
    "UseConsiderations" text COLLATE pg_catalog."default",
    "DataModelId" bigint NOT NULL,
    "DataType" character varying COLLATE pg_catalog."default",
    "ValueSetId" bigint,
    "Required" character varying COLLATE pg_catalog."default",
    "Array" character varying COLLATE pg_catalog."default",
    "SourceModel" character varying COLLATE pg_catalog."default",
    "Notes" text COLLATE pg_catalog."default",
    "CreationDate" timestamp with time zone,
    "ActivationDate" timestamp with time zone,
    "DeprecationDate" timestamp with time zone,
    "Contributor" character varying COLLATE pg_catalog."default",
    "ContributorOrganization" character varying COLLATE pg_catalog."default",
    "Extension" BOOLEAN NOT NULL DEFAULT FALSE,
    "ExtensionNotes" character varying COLLATE pg_catalog."default",
    "Deleted" bool DEFAULT false NULL,
    "Tags" text COLLATE pg_catalog."default",
    CONSTRAINT "Attributes_pkey" PRIMARY KEY ("Id"),
    CONSTRAINT "Fk_DataModelId" FOREIGN KEY ("DataModelId")
        REFERENCES public."DataModels" ("Id") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "ValueSetId" FOREIGN KEY ("ValueSetId")
        REFERENCES public."ValueSets" ("Id") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS public."EntityAttributeAssociation"
(
    "Id" bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "EntityId" bigint NOT NULL,
    "AttributeId" bigint NOT NULL,
    "Notes" text COLLATE pg_catalog."default",
    "CreationDate" timestamp with time zone,
    "ActivationDate" timestamp with time zone,
    "DeprecationDate" timestamp with time zone,
    "Contributor" character varying COLLATE pg_catalog."default",
    "ContributorOrganization" character varying COLLATE pg_catalog."default",
    "Deleted" bool DEFAULT false NULL,
    CONSTRAINT "EntityAttributeAssociation_pkey" PRIMARY KEY ("Id"),
    CONSTRAINT "Fk_AttributeId" FOREIGN KEY ("AttributeId")
        REFERENCES public."Attributes" ("Id") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Fk_EntityId" FOREIGN KEY ("EntityId")
        REFERENCES public."Entities" ("Id") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS public."Constraints"
(
    "Id" bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "Name" character varying COLLATE pg_catalog."default" NOT NULL,
    "Description" text COLLATE pg_catalog."default",
    "UseConsiderations" text COLLATE pg_catalog."default",
    "ConstraintType" constrainttype NOT NULL,
    "Value" character varying COLLATE pg_catalog."default",
    "AttributeId" bigint NOT NULL,
    "Notes" text COLLATE pg_catalog."default",
    "CreationDate" timestamp with time zone,
    "ActivationDate" timestamp with time zone,
    "DeprecationDate" timestamp with time zone,
    "Contributor" character varying COLLATE pg_catalog."default",
    "ContributorOrganization" character varying COLLATE pg_catalog."default",
    "Deleted" bool DEFAULT false NULL,
    CONSTRAINT "Constraints_pkey" PRIMARY KEY ("Id"),
    CONSTRAINT "Fk_AttributeId" FOREIGN KEY ("AttributeId")
        REFERENCES public."Attributes" ("Id") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS public."TransformationsGroup"
(
    "Id" bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "SourceDataModelId" bigint NOT NULL,
    "TargetDataModelId" bigint NOT NULL,
    "GroupVersion" text COLLATE pg_catalog."default",
    "Name" character varying COLLATE pg_catalog."default" NOT NULL,
    "Description" text COLLATE pg_catalog."default",
    "Notes" text COLLATE pg_catalog."default",
    "CreationDate" timestamp with time zone,
    "ActivationDate" timestamp with time zone,
    "DeprecationDate" timestamp with time zone,
    "Contributor" character varying COLLATE pg_catalog."default",
    "ContributorOrganization" character varying COLLATE pg_catalog."default",
    "Deleted" bool DEFAULT false NULL,
    "Extension" BOOLEAN NOT NULL DEFAULT FALSE,
    "ExtensionNotes" character varying COLLATE pg_catalog."default",
    "Tags" text COLLATE pg_catalog."default",
    CONSTRAINT "Transformations_group__pkey" PRIMARY KEY ("Id"),
    CONSTRAINT "unique_model_id_version" UNIQUE ("SourceDataModelId", "TargetDataModelId","GroupVersion"),
    CONSTRAINT "Fk_SourceDataModelId" FOREIGN KEY ("SourceDataModelId")
        REFERENCES public."DataModels" ("Id") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Fk_TargetDataModelId" FOREIGN KEY ("TargetDataModelId")
        REFERENCES public."DataModels" ("Id") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS public."Transformations"
(
    "Id" bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "TransformationGroupId" bigint NOT NULL,
    "Name" character varying COLLATE pg_catalog."default" NOT NULL,
    "Description" text COLLATE pg_catalog."default",
    "UseConsiderations" text COLLATE pg_catalog."default",
    "Alignment" character varying COLLATE pg_catalog."default",
    "Expression" character varying COLLATE pg_catalog."default",
    "ExpressionLanguage" expressionlanguagetype,
    "InputAttributesCount" integer,
    "OutputAttributesCount" integer,
    "Notes" text COLLATE pg_catalog."default",
    "CreationDate" timestamp with time zone,
    "ActivationDate" timestamp with time zone,
    "DeprecationDate" timestamp with time zone,
    "Contributor" character varying COLLATE pg_catalog."default",
    "ContributorOrganization" character varying COLLATE pg_catalog."default",
    "Deleted" bool DEFAULT false NULL,
    "Extension" BOOLEAN NOT NULL DEFAULT FALSE,
    "ExtensionNotes" character varying COLLATE pg_catalog."default",
    CONSTRAINT "Transformations_pkey" PRIMARY KEY ("Id"),
    CONSTRAINT "Fk_TransformationGroupId" FOREIGN KEY ("TransformationGroupId")
        REFERENCES public."TransformationsGroup" ("Id") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS public."TransformationAttributes"
(
    "Id" bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "AttributeId" bigint NOT NULL,
    "TransformationId" bigint NOT NULL,
    "AttributeType" attributetype NOT NULL,
    "Notes" text COLLATE pg_catalog."default",
    "CreationDate" timestamp with time zone,
    "ActivationDate" timestamp with time zone,
    "DeprecationDate" timestamp with time zone,
    "Contributor" character varying COLLATE pg_catalog."default",
    "ContributorOrganization" character varying COLLATE pg_catalog."default",
    "Deleted" bool DEFAULT false NULL,
    "Extension" BOOLEAN NOT NULL DEFAULT FALSE,
    "ExtensionNotes" character varying COLLATE pg_catalog."default",
    CONSTRAINT "TransformationAttributes_pkey" PRIMARY KEY ("Id"),
    CONSTRAINT "Fk_AttributeId" FOREIGN KEY ("AttributeId")
        REFERENCES public."Attributes" ("Id") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Fk_TransformationId" FOREIGN KEY ("TransformationId")
        REFERENCES public."Transformations" ("Id") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS public."ValueSetValueMapping"
(
    "Id" bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "SourceValueId" bigint NOT NULL,
    "TargetValueId" bigint NOT NULL,
    "Description" text COLLATE pg_catalog."default",
    "UseConsiderations" text COLLATE pg_catalog."default",
    "OriginalValueMappingId" bigint,
    "Notes" text COLLATE pg_catalog."default",
    "CreationDate" timestamp with time zone,
    "ActivationDate" timestamp with time zone,
    "DeprecationDate" timestamp with time zone,
    "Contributor" character varying COLLATE pg_catalog."default",
    "ContributorOrganization" character varying COLLATE pg_catalog."default",
    "Deleted" bool DEFAULT false NULL,
    CONSTRAINT "ValueSetValueMapping_pkey" PRIMARY KEY ("Id"),
    CONSTRAINT "Fk_SourceValueId" FOREIGN KEY ("SourceValueId")
        REFERENCES public."ValueSetValues" ("Id") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Fk_TargetValueId" FOREIGN KEY ("TargetValueId")
        REFERENCES public."ValueSetValues" ("Id") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS public."ExtInclusionsFromBaseDM"
(
    "Id" bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "ExtDataModelId" bigint NOT NULL,
    "ElementType" elementtype NOT NULL,
    "IncludedElementId" bigint NOT NULL,
    "Notes" text COLLATE pg_catalog."default",
    "CreationDate" timestamp with time zone,
    "ActivationDate" timestamp with time zone,
    "DeprecationDate" timestamp with time zone,
    "Contributor" character varying COLLATE pg_catalog."default",
    "ContributorOrganization" character varying COLLATE pg_catalog."default",
    "Deleted" bool DEFAULT false NULL,
    "LevelOfAccess" accesstype NOT NULL DEFAULT 'Private'::accesstype,
    CONSTRAINT "ExtInclusionsFromBaseDM_pkey" PRIMARY KEY ("Id"),
    CONSTRAINT "Fk_ExtDataModelId" FOREIGN KEY ("ExtDataModelId")
        REFERENCES public."DataModels" ("Id") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS public."ExtMappedValueSet"
(
    "Id" bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "ValueSetId" bigint NOT NULL,
    "MappedValueSetId" bigint NOT NULL,
    "Description" text COLLATE pg_catalog."default",
    "UseConsiderations" text COLLATE pg_catalog."default",
    "Notes" text COLLATE pg_catalog."default",
    "CreationDate" timestamp with time zone,
    "ActivationDate" timestamp with time zone,
    "DeprecationDate" timestamp with time zone,
    "Contributor" character varying COLLATE pg_catalog."default",
    "ContributorOrganization" character varying COLLATE pg_catalog."default",
    "Deleted" bool DEFAULT false NULL,
    CONSTRAINT "ExtMappedValueSet_pkey" PRIMARY KEY ("Id"),
    CONSTRAINT "Fk_MappedValueSetId" FOREIGN KEY ("MappedValueSetId")
        REFERENCES public."ValueSets" ("Id") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Fk_ValueSetId" FOREIGN KEY ("ValueSetId")
        REFERENCES public."ValueSets" ("Id") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);


CREATE TABLE public."DataModelConstraints" (
	"Id" int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
    "Name" text NULL,
    "Description" text NULL,
    "ForDataModelId" int8 NOT NULL,
	"ElementType" public."datamodelelementtype" NOT NULL,
	"ElementId" int8 NOT NULL,
    "ConstraintType" text NULL,
	"Notes" text NULL,
	"CreationDate" timestamptz NULL,
	"ActivationDate" timestamptz NULL,
	"DeprecationDate" timestamptz NULL,
	"Contributor" varchar not NULL,
	"ContributorOrganization" varchar not NULL,
	"Deleted" bool DEFAULT false NULL,
	CONSTRAINT "DataModelConstraints_pkey" PRIMARY KEY ("Id"),
	CONSTRAINT "Fk_DataModelId" FOREIGN KEY ("ForDataModelId") REFERENCES public."DataModels"("Id") ON DELETE CASCADE
);


CREATE OR REPLACE VIEW public."V_ValueSetValueMapping"
 AS
 SELECT vssource."DataModelId" AS "SourceDataModelId",
    vsvsource."Value" AS "SourceValue",
    vstarget."DataModelId" AS "TargetDataModelId",
    vsvtarget."Value" AS "TargetValue",
    vsvm."Id",
    vsvm."SourceValueId",
    vsvm."TargetValueId",
    vsvm."Description",
    vsvm."UseConsiderations",
    vsvm."OriginalValueMappingId",
    vsvm."Notes",
    vsvm."CreationDate",
    vsvm."ActivationDate",
    vsvm."DeprecationDate",
    vsvm."Contributor",
    vsvm."ContributorOrganization"
   FROM "ValueSetValueMapping" vsvm
     JOIN "ValueSetValues" vsvsource ON vsvsource."Id" = vsvm."SourceValueId"
     JOIN "ValueSetValues" vsvtarget ON vsvtarget."Id" = vsvm."TargetValueId"
     JOIN "ValueSets" vssource ON vssource."Id" = vsvsource."ValueSetId"
     JOIN "ValueSets" vstarget ON vstarget."Id" = vsvtarget."ValueSetId";

CREATE OR REPLACE VIEW public."ValueIdLookUp"
 AS
 SELECT vs."DataModelId",
    vs."Name" AS "ValueSetName",
    vsval."Id" AS "ValueSetValueId",
    vsval."Value"
   FROM "ValueSets" vs
     JOIN "ValueSetValues" vsval ON vs."Id" = vsval."ValueSetId";

CREATE OR REPLACE PROCEDURE public.deletedatamodelrecords(
	IN datamodel character varying DEFAULT 2)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
	t_name RECORD; 
	max_id INT;
	datamodelid bigint;
	seq_id Varchar(200);
	str Varchar(2000);
    cursor_tables CURSOR FOR SELECT table_name
	FROM information_schema.tables
	WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
	AND table_type = 'BASE TABLE';
BEGIN
	
	EXECUTE 'SELECT MAX("Id") FROM "DataModels" where "Name" = '|| quote_literal(datamodel) Into datamodelid;
   	delete from public."Entities" where "DataModelId" = datamodelid;
	delete from public."Attributes" where "DataModelId" = datamodelid;
	delete from public."ValueSets" where "DataModelId" = datamodelid;
	delete from public."Transformations" where ("SourceDataModelId" = datamodelid or "TargetDataModelId" = datamodelid);
	delete from public."ExtInclusionsFromBaseDM" where "ExtDataModelId" = datamodelid;
	
	
	OPEN cursor_tables;
    
    -- Fetch and process rows
    LOOP
        FETCH cursor_tables INTO t_name;
        EXIT WHEN NOT FOUND; -- Exit loop when no more rows
       	EXECUTE 'SELECT MAX("Id") FROM ' || quote_ident(t_name.table_name) INTO max_id;
		EXECUTE 'SELECT pg_get_serial_sequence(' || quote_literal(quote_ident(t_name.table_name)) || ', ''Id'')' INTO seq_id;
		seq_id = Replace(seq_id,'public.','');
		If max_id is null then 
			max_id = 1; 
		End If;
		If seq_id is not null then
			EXECUTE 'SELECT setval(' || quote_literal(seq_id) || ', ' || max_id + 1 || ', false)';
		End If;	
    END LOOP;
    
    CLOSE cursor_tables;

END; 
$BODY$;
ALTER PROCEDURE public.deletedatamodelrecords(character varying)
    OWNER TO postgres;