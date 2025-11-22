import {
  Badge,
  Text,
  TextField,
  Button,
  Dialog,
  Flex,
} from "@radix-ui/themes";
import { useState, useMemo, useEffect } from "react";
import "./List.css";
import ObjectDetails from "../ObjectDetails/ObjectDetails";
import { Pencil2Icon, PlusIcon, TrashIcon } from "@radix-ui/react-icons";
import { CrudDialog, DeleteDialog, DialogField, DialogItem } from "../Dialog/Dialog";

export interface ListItem {
  Id?: number;
  Name?: string;
  Value?: string;
  Description?: string;
  Source?: string;
  count?: number;
  attribute_unique_name?: string;
  attribute_name?: string;
  attribute_id?: number;
  Deleted?: boolean;
}

interface ListProps {
  items: ListItem[];
  selected?: number | null;
  onSelect?: (id: number, clicked?: boolean) => void;
  routPath?: string;
  displayField?: "Name" | "Value" | "attribute_name" | "attribute_unique_name";
  idField?: "Id" | "attribute_id";
  showDetails?: boolean;
  title?: string;
  count?: number;
  showDescriptions?: boolean;
  showObjectDetails?: boolean;
  onValueSelect?: (id: number) => void;
  selectedValue?: number | null;
  modelConstraints?: any[];
  crud?: boolean;
  header?: boolean;
  showConstraints?: boolean;
  onCreate?: (params: any) => Promise<void>;
  onEdit?: (id: number, params: any) => Promise<void>;
  onDelete?: (id: number) => Promise<void>;
  createFields?: DialogField[];
  onCreateSuccess?: () => Promise<void>;
  onRestoreItem?: (id: number) => Promise<void>;
  onConstraintClick?: (
    id: number,
    name: string,
    constraintId?: number
  ) => Promise<void>;
}

const List: React.FC<ListProps> = ({
  items,
  selected,
  onSelect,
  displayField = "Name",
  idField = "Id",
  showDetails = false,
  title,
  createFields = [],
  showDescriptions = false,
  crud = false,
  header = true,
  showObjectDetails = false,
  showConstraints = false,
  onCreate,
  onEdit,
  onDelete,
  onCreateSuccess,
  modelConstraints = [],
  onConstraintClick,
}) => {
  const [selectedItem, setSelectedItem] = useState<number | null>(null);
  const [count, setCount] = useState<number>(items.length);
  const [filterText, setFilterText] = useState("");
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [itemToDelete, setItemToDelete] = useState<number | null>(null);
  const [isEditMode, setIsEditMode] = useState(false);
  const [itemToEdit, setItemToEdit] = useState<DialogItem | null>(null);

  const filteredItems = useMemo(() => {
    if (!filterText) return items;
    const filtered = items.filter((item) => {
      const fieldValue = item[displayField];
      return fieldValue
        ?.toString()
        .toLowerCase()
        .includes(filterText.toLowerCase());
    });
    return filtered;
  }, [items, filterText, displayField]);

  const handleEditClick = (e: React.MouseEvent, item: ListItem) => {
    e.stopPropagation();
    setItemToEdit(item);
    setIsEditMode(true);
    setIsCreateDialogOpen(true);
  };

  const handleDeleteClick = (e: React.MouseEvent, id: number) => {
    e.stopPropagation();
    setItemToDelete(id);
  };

  const handleDeleteConfirm = async () => {
    if (!itemToDelete || !onDelete) return;
    await onDelete(itemToDelete);
  };

  const handleSelection = (item: ListItem, clicked?: boolean) => {
    setSelectedItem(item[idField] ?? null);
    if (onSelect) {
      onSelect(item[idField]!, clicked);
    }
  };

  const handleDialogOpenChange = (open: boolean) => {
    setIsCreateDialogOpen(open);
    if (!open) {
      setIsEditMode(false);
      setItemToEdit(null);
    }
  };

  useEffect(() => {
    setCount(items.length);
  }, [items]);

  useEffect(() => {
    if (selected !== undefined && selected !== null && items.length > 0) {
      const numberSelected =
        typeof selected === "number" ? selected : Number(selected);
      const item = items.find((item) => item[idField] === numberSelected);

      if (item) {
        handleSelection(item);
      }

      setTimeout(() => {
        const element = document.querySelector(
          `[data-list-item-id="${title
            ?.toLowerCase()
            ?.replace(/\s+/g, "_")}-${selected}"]`
        );

        if (element) {
          element.scrollIntoView({
            behavior: "smooth",
            block: "nearest",
            inline: "start",
          });
        }
      }, 100);
    } else if (selected === null) {
      setSelectedItem(null);
    }
  }, [selected, items]);

  const renderListItem = (item: ListItem) => {
    const isSelected = selected === item[idField];
    const hasConstraint = modelConstraints.some(
      (c) => c.ElementId === item[idField]
    );
    const itemId = item[idField];
    const itemName = item[displayField];

    if (!itemId) return null;

    return (
      <div
        key={itemId}
        className={`list-item ${isSelected ? "selected" : ""}`}
        onClick={() => onSelect?.(itemId, true)}
        data-list-item-id={`${title
          ?.toLowerCase()
          ?.replace(/\s+/g, "_")}-${itemId}`}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          {showConstraints && (
            <Button
              data-constraint-id={`${
                modelConstraints.find((c) => c.ElementId === itemId)?.Id || 0
              }`}
              variant={hasConstraint ? "solid" : "outline"}
              color={hasConstraint ? "blue" : "gray"}
              onClick={(e) => {
                e.stopPropagation();
                if (onConstraintClick && itemName) {
                  const dataId = (e.target as HTMLElement).getAttribute(
                    "data-constraint-id"
                  );
                  if (dataId) {
                    onConstraintClick(itemId, itemName, parseInt(dataId));
                  } else {
                    onConstraintClick(itemId, itemName);
                  }
                }
              }}
              style={{ minWidth: "32px", padding: "0 8px" }}
            >
              C
            </Button>
          )}
          <div className="item-label">{itemName}</div>
          {isSelected && crud && (
            <div style={{ marginLeft: "auto", display: "flex", gap: "4px" }}>
              <Button
                size="1"
                variant="ghost"
                onClick={(e) => handleEditClick(e, item)}
              >
                <Pencil2Icon />
              </Button>
              <Button
                size="1"
                variant="ghost"
                color="red"
                onClick={(e) => handleDeleteClick(e, itemId)}
              >
                <TrashIcon />
              </Button>
            </div>
          )}
        </div>
        {showDescriptions && item.Description && (
          <div style={{ fontSize: "0.8em", color: "gray" }}>
            {item.Description}
          </div>
        )}
        {showObjectDetails && item[idField] === selected && (
          <ObjectDetails object={item} excludeKeys={[]} />
        )}
      </div>
    );
  };

  return (
    <>
      <Dialog.Root>
        <div
          className={`list-container ${title
            ?.toLocaleLowerCase()
            .replace(/\s+/g, "_")}-list`}
        >
          {header && (
            <div className="list-header">
              <Flex justify="between" align="center">
                {title && (
                  <Text size="2" weight="bold">
                    {title}
                    {count !== undefined && (
                      <Badge
                        size="1"
                        variant="solid"
                        color="blue"
                        style={{ marginLeft: "8px" }}
                      >
                        {count}
                      </Badge>
                    )}
                  </Text>
                )}
                {crud && (
                  <Dialog.Trigger>
                    <Button 
                      size="1" 
                      style={{ marginLeft: "10px" }}
                      onClick={() => setIsCreateDialogOpen(true)}
                    >
                      <PlusIcon />
                    </Button>
                  </Dialog.Trigger>
                )}
              </Flex>
              <TextField.Root
                size="2"
                style={{ marginTop: "8px" }}
                placeholder="Type to filter"
                value={filterText}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                  setFilterText(e.target.value)
                }
              />
            </div>
          )}
          <div className="list-items">
            {filteredItems?.map((item) => renderListItem(item))}
          </div>
        </div>
      </Dialog.Root>

      <CrudDialog
        isOpen={isCreateDialogOpen}
        onOpenChange={handleDialogOpenChange}
        title={title || ""}
        fields={createFields}
        isEditMode={isEditMode}
        itemToEdit={itemToEdit}
        onCreate={onCreate}
        onEdit={onEdit}
        onCreateSuccess={onCreateSuccess}
      />

      <DeleteDialog
        isOpen={!!itemToDelete}
        onClose={() => setItemToDelete(null)}
        title={title || ""}
        onConfirm={handleDeleteConfirm}
      />
    </>
  );
};

export default List;
