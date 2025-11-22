import React, { useCallback, useEffect, useState } from "react";
import { Box, Button, Card, Dialog, Flex, Select, TextField, Text } from '@radix-ui/themes';
import { getTransformationsForGroup, TransformationGroupPaginatedResponse } from "../../services/transformationsService";
import EditableFormula from "../EditableFormula/EditableFormula";

interface EditTransformationGroupProps {
    groupId: number;
    onChange?: (data: any) => void;
}

const EditTransformationGroup: React.FC<EditTransformationGroupProps> = ({ groupId, onChange }) => {
    const [group, setGroup] = useState<any>();
    const [editData, setEditData] = useState<any>();
    const [isDirty, setIsDirty] = useState(false);
    
    useEffect(() => {
        const fetchGroup = async () => {
            if (!groupId) return null;

            const transformationsResponse = await getTransformationsForGroup(
                Number(groupId),
                true,
                1,
                1 // I don't need the transformations here, just the group...
            ) as TransformationGroupPaginatedResponse;

            if (!transformationsResponse) {
                console.error('Error fetching data');
                return null;
            }

            setGroup(transformationsResponse.data);
        };
        fetchGroup();
    }, [groupId]);

    useEffect(() => {
        // we *only* want the fields that we have input for in here:
        const editData = {
            Name: group?.Name,
            Description: group?.Description,
            Notes: group?.Notes,
            Tags: group?.Tags,
            Contributor: group?.Contributor,
            ContributorOrganization: group?.ContributorOrganization,
            CreationDate: group?.CreationDate,
            ActivationDate: group?.ActivationDate,
            DeprecationDate: group?.DeprecationDate
        };
        setEditData(editData);
    }, [group]);

    useEffect(() => {
        if (isDirty && onChange) {
            onChange(editData);
        }
    }, [editData, onChange, isDirty]);

    const handleEditField = useCallback((field: string, value: any) => {
        setEditData({ ...editData, [field]: value });
        setIsDirty(true);
    }, [editData]);

    return (
        <Flex gap="2" align="start" direction="column">
            <Text as="div" size="1" color="gray">Name:</Text>
            <TextField.Root
                defaultValue={editData?.Name}
                onChange={(e) => handleEditField('Name', e.target.value)} />
            <Text as="div" size="1" color="gray">Description:</Text>
            <EditableFormula
                formula={editData?.Description}
                onFormulaChange={(formula) => handleEditField('Description', formula)} />
            <Text as="div" size="1" color="gray">Notes:</Text>
            <EditableFormula
                formula={editData?.Notes}
                onFormulaChange={(formula) => handleEditField('Notes', formula)} />
            <Text as="div" size="1" color="gray">Tags:</Text>
            <TextField.Root
                defaultValue={editData?.Tags}
                onChange={(e) => handleEditField('Tags', e.target.value)} />
            <Text as="div" size="1" color="gray">Contributor:</Text>
            <TextField.Root
                defaultValue={editData?.Contributor}
                onChange={(e) => handleEditField('Contributor', e.target.value)} />
            <Text as="div" size="1" color="gray">Contributor Organization:</Text>
            <TextField.Root
                defaultValue={editData?.ContributorOrganization}
                onChange={(e) => handleEditField('ContributorOrganization', e.target.value)} />
            <Text as="div" size="1" color="gray">Creation Date:</Text>
            <TextField.Root
                type="datetime-local"
                defaultValue={editData?.CreationDate?.slice(0, 16)}
                onChange={(e) => handleEditField('CreationDate', e.target.value)} />
            <Text as="div" size="1" color="gray">Activation Date:</Text>
            <TextField.Root
                type="datetime-local"
                defaultValue={editData?.ActivationDate?.slice(0, 16)}
                onChange={(e) => handleEditField('ActivationDate', e.target.value)} />
            <Text as="div" size="1" color="gray">Deprecation Date:</Text>
            <TextField.Root
                type="datetime-local"
                defaultValue={editData?.DeprecationDate?.slice(0, 16)}
                onChange={(e) => handleEditField('DeprecationDate', e.target.value)} />
        </Flex>
    );
};

export default EditTransformationGroup;